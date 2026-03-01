"""
rlogin → Evennia telnet bridge.

Usage:
    python bridge.py <listen_port> <evennia_telnet_port>

Mystic BBS connects via rlogin (RFC 1282). This bridge:
  1. Performs the rlogin handshake to extract the BBS username.
  2. Responds with \x00 (rlogin OK).
  3. Connects to Evennia's telnet port.
  4. Automates login: sends username + shared secret password.
     If account doesn't exist, creates it via Evennia's "create" command.
  5. Bridges the rest of the session bidirectionally.

The shared secret password is BRIDGE_PASSWORD below. It must match
BBS_BRIDGE_PASSWORD in both live and dev settings.py.
"""

import asyncio
import logging
import re
import sys

BRIDGE_PASSWORD = "pepsicola_bbs_secret_2026"

# Evennia telnet negotiation bytes to ignore/strip during login handshake
# IAC = 0xFF; we need to pass these through after login but eat them during
# the prompt-matching phase.
IAC = 0xFF

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [bridge] %(levelname)s %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger("bridge")


def parse_rlogin_header(data: bytes):
    """
    Parse rlogin handshake from the first chunk of data received.
    Returns (client_user, server_user, terminal_speed) or None if incomplete.

    rlogin wire format (from client after TCP connect):
        \x00 <client-user> \x00 <server-user> \x00 <terminal/speed> \x00
    """
    if not data or data[0] != 0:
        return None
    # Find the four \x00-delimited fields
    fields = data[1:].split(b"\x00")
    # fields[0]=client_user, fields[1]=server_user, fields[2]=term/speed
    if len(fields) < 3:
        return None
    client_user = fields[0].decode("ascii", errors="replace").strip()
    server_user = fields[1].decode("ascii", errors="replace").strip()
    return client_user, server_user


async def read_until(reader: asyncio.StreamReader, pattern: bytes, timeout: float = 10.0) -> bytes:
    """
    Read from reader until pattern is found in accumulated data.
    Returns all data accumulated up to and including the pattern.
    Raises asyncio.TimeoutError if timeout exceeded.
    """
    buf = b""
    deadline = asyncio.get_event_loop().time() + timeout
    while True:
        remaining = deadline - asyncio.get_event_loop().time()
        if remaining <= 0:
            raise asyncio.TimeoutError(f"Timed out waiting for {pattern!r}, got: {buf!r}")
        try:
            chunk = await asyncio.wait_for(reader.read(4096), timeout=min(remaining, 1.0))
        except asyncio.TimeoutError:
            continue
        if not chunk:
            raise ConnectionError(f"Connection closed waiting for {pattern!r}, got: {buf!r}")
        buf += chunk
        if pattern in buf:
            return buf


async def strip_iac_then_find(reader: asyncio.StreamReader, pattern: bytes, timeout: float = 15.0) -> bytes:
    """
    Read, stripping Telnet IAC negotiation sequences, until pattern found in clean text.
    Returns the accumulated raw bytes (unstripped) so the full stream is preserved.
    """
    raw_buf = b""
    clean_buf = b""
    deadline = asyncio.get_event_loop().time() + timeout
    i = 0

    while True:
        remaining = deadline - asyncio.get_event_loop().time()
        if remaining <= 0:
            raise asyncio.TimeoutError(
                f"Timed out waiting for {pattern!r}; clean so far: {clean_buf!r}"
            )
        try:
            chunk = await asyncio.wait_for(reader.read(4096), timeout=min(remaining, 1.0))
        except asyncio.TimeoutError:
            continue
        if not chunk:
            raise ConnectionError(
                f"Connection closed; clean buf: {clean_buf!r}"
            )
        raw_buf += chunk

        # Strip IAC sequences from new chunk to update clean_buf
        j = 0
        new_chunk = chunk
        while j < len(new_chunk):
            b = new_chunk[j]
            if b == IAC:
                # IAC + command (2 bytes) or IAC + WILL/WONT/DO/DONT + option (3 bytes)
                if j + 1 < len(new_chunk):
                    cmd = new_chunk[j + 1]
                    if cmd in (0xFB, 0xFC, 0xFD, 0xFE):  # WILL/WONT/DO/DONT
                        j += 3
                    else:
                        j += 2
                else:
                    j += 1  # incomplete, skip
            else:
                clean_buf += bytes([b])
                j += 1

        if pattern in clean_buf:
            return raw_buf


async def bridge_bidirectional(
    bbs_reader: asyncio.StreamReader,
    bbs_writer: asyncio.StreamWriter,
    mud_reader: asyncio.StreamReader,
    mud_writer: asyncio.StreamWriter,
):
    """Forward data between BBS and MUD in both directions until one side closes."""

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
    # Collect data until we have the full header (ends with \x00 after term field)
    header_buf = b""
    try:
        # Read up to 256 bytes to capture the rlogin header
        for _ in range(32):
            chunk = await asyncio.wait_for(bbs_reader.read(256), timeout=5.0)
            if not chunk:
                break
            header_buf += chunk
            # rlogin header: \x00 user1 \x00 user2 \x00 term \x00
            # Count null bytes — need at least 4
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
    # Mystic sends the BBS username as server_user
    bbs_username = server_user if server_user else client_user
    log.info(f"rlogin handshake: client_user={client_user!r} server_user={server_user!r} → username={bbs_username!r}")

    # Respond with \x00 (rlogin accepted)
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

    # --- Step 3: Automate login ---
    # Evennia prompts: "What is your account name?"
    # If account exists: "What is your password?"
    # If not:           "That account was not found. Do you want to create it? [Y]/N"
    #                    (after Y) "What is your new password?" then confirm

    try:
        # Wait for the "account name" prompt (Evennia 5.x says "account name")
        await strip_iac_then_find(mud_reader, b"name", timeout=20.0)
        mud_writer.write((bbs_username + "\n").encode())
        await mud_writer.drain()
        log.debug(f"Sent username: {bbs_username!r}")

        # Collect next prompt — could be password prompt or "not found" message
        response_buf = await strip_iac_then_find(
            mud_reader,
            b"?",  # both "password?" and "create it?" end with ?
            timeout=15.0,
        )
        response_text = response_buf.decode("utf-8", errors="replace").lower()

        if "not found" in response_text or "create" in response_text:
            # Account does not exist — confirm creation
            log.info(f"Account {bbs_username!r} not found; creating new account")
            mud_writer.write(b"y\n")
            await mud_writer.drain()

            # Wait for "new password" prompt
            await strip_iac_then_find(mud_reader, b"password", timeout=10.0)
            mud_writer.write((BRIDGE_PASSWORD + "\n").encode())
            await mud_writer.drain()

            # Wait for password confirmation prompt
            await strip_iac_then_find(mud_reader, b"again", timeout=10.0)
            mud_writer.write((BRIDGE_PASSWORD + "\n").encode())
            await mud_writer.drain()

            log.info(f"Account {bbs_username!r} created")
        else:
            # Account exists — send password
            log.debug(f"Account {bbs_username!r} exists; sending password")
            mud_writer.write((BRIDGE_PASSWORD + "\n").encode())
            await mud_writer.drain()

        log.info(f"Login sequence complete for {bbs_username!r}")

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
