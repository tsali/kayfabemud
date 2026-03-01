"""
rlogin → Evennia telnet bridge.

Usage:
    python bridge.py <listen_port> <evennia_telnet_port>

Mystic BBS connects via rlogin (RFC 1282). This bridge:
  1. Performs the rlogin handshake to extract the BBS username.
  2. Responds with \\x00 (rlogin OK).
  3. Connects to Evennia's telnet port.
  4. Automates login using Evennia 5.x command-based login:
       connect <username> <password>        (existing account)
       create <username> <password> + Y     (new account)
  5. Bridges the session bidirectionally once logged in.

The shared secret password is BRIDGE_PASSWORD below. It must match
BBS_BRIDGE_PASSWORD in both live and dev settings.py.
"""

import asyncio
import logging
import re
import sys

BRIDGE_PASSWORD = "pepsicola_bbs_secret_2026"

IAC = 0xFF

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [bridge] %(levelname)s %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger("bridge")


def parse_rlogin_header(data: bytes):
    """
    Parse rlogin handshake. Wire format:
        \\x00 <client-user> \\x00 <server-user> \\x00 <terminal/speed> \\x00
    Returns (client_user, server_user) or None if incomplete.
    """
    if not data or data[0] != 0:
        return None
    fields = data[1:].split(b"\\x00")  # raw
    fields = data[1:].split(b"\x00")
    if len(fields) < 3:
        return None
    client_user = fields[0].decode("ascii", errors="replace").strip()
    server_user = fields[1].decode("ascii", errors="replace").strip()
    return client_user, server_user


async def read_with_timeout(reader: asyncio.StreamReader, timeout: float = 5.0) -> bytes:
    """Read available data with timeout."""
    try:
        return await asyncio.wait_for(reader.read(4096), timeout=timeout)
    except asyncio.TimeoutError:
        return b""


def strip_ansi_iac(data: bytes) -> str:
    """Strip Telnet IAC sequences and ANSI codes, return clean text."""
    # Strip 3-byte IAC option sequences
    data = re.sub(b"\xff[\xfb-\xfe].", b"", data)
    # Strip 2-byte IAC commands
    data = re.sub(b"\xff.", b"", data)
    # Strip ANSI color/control sequences
    data = re.sub(b"\x1b\\[[^m]*m", b"", data)
    data = re.sub(b"\x1b\\[[^a-zA-Z]*[a-zA-Z]", b"", data)
    return data.decode("utf-8", errors="replace")


async def read_until_quiet(reader: asyncio.StreamReader, quiet_timeout: float = 1.5, max_total: float = 15.0) -> bytes:
    """
    Read from reader until no new data arrives for quiet_timeout seconds,
    or max_total seconds have elapsed.
    Returns all accumulated data.
    """
    buf = b""
    start = asyncio.get_event_loop().time()
    while True:
        elapsed = asyncio.get_event_loop().time() - start
        if elapsed >= max_total:
            break
        try:
            chunk = await asyncio.wait_for(reader.read(4096), timeout=quiet_timeout)
            if not chunk:
                break
            buf += chunk
        except asyncio.TimeoutError:
            # No data for quiet_timeout — we're done
            break
    return buf


async def read_until_pattern(reader: asyncio.StreamReader, pattern: str, timeout: float = 15.0) -> bytes:
    """
    Read from reader (stripping IAC/ANSI) until pattern found in clean text.
    Returns raw accumulated bytes.
    """
    raw_buf = b""
    clean_buf = ""
    deadline = asyncio.get_event_loop().time() + timeout

    while True:
        remaining = deadline - asyncio.get_event_loop().time()
        if remaining <= 0:
            raise asyncio.TimeoutError(f"Timed out waiting for {pattern!r}; got: {clean_buf!r}")
        try:
            chunk = await asyncio.wait_for(reader.read(4096), timeout=min(remaining, 1.0))
        except asyncio.TimeoutError:
            continue
        if not chunk:
            raise ConnectionError(f"Connection closed waiting for {pattern!r}")
        raw_buf += chunk
        clean_buf += strip_ansi_iac(chunk)
        if pattern in clean_buf:
            return raw_buf


async def bridge_bidirectional(
    bbs_reader: asyncio.StreamReader,
    bbs_writer: asyncio.StreamWriter,
    mud_reader: asyncio.StreamReader,
    mud_writer: asyncio.StreamWriter,
):
    """Forward data between BBS client and MUD server bidirectionally."""

    async def forward(src: asyncio.StreamReader, dst: asyncio.StreamWriter, label: str):
        try:
            while True:
                data = await src.read(4096)
                if not data:
                    break
                dst.write(data)
                await dst.drain()
        except (ConnectionResetError, BrokenPipeError, asyncio.IncompleteReadError):
            pass
        except Exception as e:
            log.debug(f"{label} forward error: {e}")
        finally:
            try:
                dst.close()
            except Exception:
                pass

    await asyncio.gather(
        forward(bbs_reader, mud_writer, "bbs→mud"),
        forward(mud_reader, bbs_writer, "mud→bbs"),
        return_exceptions=True,
    )


async def handle_connection(
    bbs_reader: asyncio.StreamReader,
    bbs_writer: asyncio.StreamWriter,
    evennia_host: str,
    evennia_port: int,
):
    peer = bbs_writer.get_extra_info("peername")
    log.info(f"New connection from {peer}")

    # --- Step 1: rlogin handshake ---
    header_buf = b""
    try:
        for _ in range(32):
            chunk = await asyncio.wait_for(bbs_reader.read(256), timeout=5.0)
            if not chunk:
                break
            header_buf += chunk
            if header_buf.count(b"\x00") >= 4:
                break
    except asyncio.TimeoutError:
        log.warning(f"Timeout reading rlogin header from {peer}")
        bbs_writer.close()
        return

    parsed = parse_rlogin_header(header_buf)
    if not parsed:
        log.warning(f"Bad rlogin header from {peer}: {header_buf!r}")
        bbs_writer.close()
        return

    client_user, server_user = parsed
    bbs_username = server_user if server_user else client_user
    log.info(f"rlogin: client={client_user!r} server={server_user!r} → username={bbs_username!r}")

    # Acknowledge rlogin
    bbs_writer.write(b"\x00")
    await bbs_writer.drain()

    # --- Step 2: Connect to Evennia ---
    try:
        mud_reader, mud_writer = await asyncio.wait_for(
            asyncio.open_connection(evennia_host, evennia_port),
            timeout=10.0,
        )
    except Exception as e:
        log.error(f"Cannot connect to Evennia at {evennia_host}:{evennia_port}: {e}")
        bbs_writer.write(b"\r\nEvennia is unavailable. Try again later.\r\n")
        await bbs_writer.drain()
        bbs_writer.close()
        return

    log.info(f"Connected to Evennia at {evennia_host}:{evennia_port}")

    # --- Step 3: Automate login (Evennia 5.x command-based) ---
    # Evennia 5.x shows a welcome banner, no interactive prompts.
    # Login: `connect <user> <pass>` → success shows "You become X."
    # New account: `create <user> <pass>` → confirmation "[Y]/N?" → send Y

    try:
        # Read and discard the welcome banner (wait until quiet)
        banner = await read_until_quiet(mud_reader, quiet_timeout=1.5, max_total=10.0)
        banner_text = strip_ansi_iac(banner)
        log.debug(f"Banner for {bbs_username!r}: {banner_text[:100]!r}")

        # Attempt to connect with existing credentials
        connect_cmd = f"connect {bbs_username} {BRIDGE_PASSWORD}\r\n"
        mud_writer.write(connect_cmd.encode())
        await mud_writer.drain()
        log.debug(f"Sent: connect {bbs_username!r} ***")

        # Read response
        resp_raw = await read_until_quiet(mud_reader, quiet_timeout=2.0, max_total=10.0)
        resp_text = strip_ansi_iac(resp_raw)
        log.debug(f"connect response: {resp_text[:150]!r}")

        if "You become" in resp_text or "logged in" in resp_text.lower():
            # Existing account logged in successfully
            log.info(f"Existing account login OK for {bbs_username!r}")
            # Forward what we've already received to the BBS client
            bbs_writer.write(resp_raw)
            await bbs_writer.drain()

        elif "incorrect" in resp_text.lower() or "not found" in resp_text.lower() or "no account" in resp_text.lower():
            # Account doesn't exist — create it, then connect
            log.info(f"Account {bbs_username!r} not found; creating")
            create_cmd = f"create {bbs_username} {BRIDGE_PASSWORD}\r\n"
            mud_writer.write(create_cmd.encode())
            await mud_writer.drain()

            # Read confirmation prompt: "Is this what you intended? [Y]/N?"
            conf_raw = await read_until_quiet(mud_reader, quiet_timeout=2.0, max_total=10.0)
            conf_text = strip_ansi_iac(conf_raw)
            log.debug(f"create confirmation: {conf_text[:150]!r}")

            if "[Y]" in conf_text or "intended" in conf_text.lower():
                mud_writer.write(b"Y\r\n")
                await mud_writer.drain()
                # Read the create success response
                create_resp_raw = await read_until_quiet(mud_reader, quiet_timeout=2.0, max_total=10.0)
                create_resp_text = strip_ansi_iac(create_resp_raw)
                log.debug(f"create result: {create_resp_text[:100]!r}")

                # Now connect to actually log in (create doesn't log you in automatically)
                mud_writer.write(connect_cmd.encode())
                await mud_writer.drain()
                login_raw = await read_until_quiet(mud_reader, quiet_timeout=2.0, max_total=10.0)
                login_text = strip_ansi_iac(login_raw)
                log.info(f"Account created + connected for {bbs_username!r}: {login_text[:80]!r}")
                # Forward post-login output to BBS client
                bbs_writer.write(login_raw)
                await bbs_writer.drain()
            else:
                # Unexpected response
                log.error(f"Unexpected create response for {bbs_username!r}: {conf_text!r}")
                bbs_writer.write(b"\r\nLogin failed. Please try again.\r\n")
                await bbs_writer.drain()
                mud_writer.close()
                bbs_writer.close()
                return
        else:
            # Unknown response — still bridge (might be already in game, or
            # Evennia version difference). Forward what we got and bridge.
            log.warning(f"Unexpected connect response for {bbs_username!r}: {resp_text[:100]!r}")
            bbs_writer.write(resp_raw)
            await bbs_writer.drain()

    except (asyncio.TimeoutError, ConnectionError) as e:
        log.error(f"Login automation failed for {bbs_username!r}: {e}")
        bbs_writer.write(b"\r\nLogin failed. Please try again.\r\n")
        await bbs_writer.drain()
        mud_writer.close()
        bbs_writer.close()
        return

    # --- Step 4: Bidirectional bridge ---
    log.info(f"Bridging session for {bbs_username!r}")
    await bridge_bidirectional(bbs_reader, bbs_writer, mud_reader, mud_writer)
    log.info(f"Session ended for {bbs_username!r}")


async def main(listen_port: int, evennia_port: int, evennia_host: str = "127.0.0.1"):
    async def handler(reader, writer):
        await handle_connection(reader, writer, evennia_host, evennia_port)

    server = await asyncio.start_server(handler, "0.0.0.0", listen_port)
    addrs = ", ".join(str(s.getsockname()) for s in server.sockets)
    log.info(f"rlogin bridge listening on {addrs} → Evennia {evennia_host}:{evennia_port}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <listen_port> <evennia_port>", file=sys.stderr)
        sys.exit(1)
    listen_port = int(sys.argv[1])
    evennia_port = int(sys.argv[2])
    asyncio.run(main(listen_port, evennia_port))
