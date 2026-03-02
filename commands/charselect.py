"""
Kayfabe: Protect the Business — Character selection and creation commands.

These are in-game commands available to puppeted characters, allowing
players to switch between wrestlers or create new ones (up to MAX_NR_CHARACTERS).
"""

from evennia import Command
from evennia.utils import logger


class CmdCharSelect(Command):
    """
    Switch to a different wrestler on your account.

    Usage:
      charselect

    Lists all wrestlers on your account and lets you switch to one.
    """

    key = "charselect"
    aliases = ["chars", "characters"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        account = self.caller.account
        if not account:
            self.caller.msg("No account found.")
            return

        chars = [c for c in account.characters if c.access(account, "puppet")]
        if len(chars) <= 1:
            self.caller.msg("You only have one wrestler. Use |wcharcreate|n to make another.")
            return

        # Build the list
        current = self.caller
        msg = "\n|w=== YOUR WRESTLERS ===|n\n\n"
        for i, char in enumerate(chars, 1):
            marker = " |g<-- current|n" if char == current else ""
            if char.db.chargen_complete:
                territory = (char.db.territory or "???").upper()
                tier = char.db.tier or 1
                alignment = char.db.alignment or "?"
                rank = char.get_rank() if hasattr(char, "get_rank") else "?"
                msg += f"  |w{i}|n. |c{char.key}|n ({territory}, Tier {tier}, {alignment}) — {rank}{marker}\n"
            else:
                msg += f"  |w{i}|n. |c{char.key}|n |y(chargen incomplete)|n{marker}\n"

        msg += (
            f"\n  Type |wcharselect <number>|n to switch.\n"
            f"  Type |wcharcreate|n to create a new wrestler.\n"
        )
        self.caller.msg(msg)

        # Check if a number was passed as argument
        args = self.args.strip()
        if args:
            self._switch_to(account, chars, args)

    def _switch_to(self, account, chars, choice):
        try:
            idx = int(choice) - 1
        except ValueError:
            self.caller.msg("|rEnter a number.|n")
            return

        if idx < 0 or idx >= len(chars):
            self.caller.msg(f"|rChoose 1 through {len(chars)}.|n")
            return

        target = chars[idx]
        if target == self.caller:
            self.caller.msg("You're already playing that wrestler.")
            return

        session = self.caller.sessions.get()[0] if self.caller.sessions.get() else None
        if not session:
            self.caller.msg("No active session found.")
            return

        # Unpuppet current, puppet target
        self.caller.msg(f"\nSwitching to |c{target.key}|n...\n")
        try:
            account.unpuppet_object(session)
            account.puppet_object(session, target)
        except RuntimeError as e:
            self.caller.msg(f"|rSwitch failed: {e}|n")
            logger.log_err(f"Character switch failed for {account.key}: {e}")


class CmdCharDelete(Command):
    """
    Delete a wrestler from your account.

    Usage:
      chardelete
      chardelete <number>
      chardelete <number> confirm

    Lists your wrestlers and lets you delete one. You cannot delete
    the wrestler you are currently playing — switch first.
    Requires typing 'chardelete <number> confirm' to actually delete.
    """

    key = "chardelete"
    aliases = ["delchar"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        account = self.caller.account
        if not account:
            self.caller.msg("No account found.")
            return

        chars = [c for c in account.characters if c.access(account, "puppet")]
        if not chars:
            self.caller.msg("You have no wrestlers.")
            return

        args = self.args.strip().split()

        if not args:
            # Show the list
            current = self.caller
            msg = "\n|w=== DELETE A WRESTLER ===|n\n\n"
            for i, char in enumerate(chars, 1):
                marker = " |g<-- current|n" if char == current else ""
                if char.db.chargen_complete:
                    territory = (char.db.territory or "???").upper()
                    msg += f"  |w{i}|n. |c{char.key}|n ({territory}){marker}\n"
                else:
                    msg += f"  |w{i}|n. |c{char.key}|n |y(chargen incomplete)|n{marker}\n"
            msg += (
                f"\n  Type |wchardelete <number>|n to select.\n"
                f"  |rThis is permanent!|n\n"
            )
            self.caller.msg(msg)
            return

        # Parse the number
        try:
            idx = int(args[0]) - 1
        except ValueError:
            self.caller.msg("|rEnter a number.|n")
            return

        if idx < 0 or idx >= len(chars):
            self.caller.msg(f"|rChoose 1 through {len(chars)}.|n")
            return

        target = chars[idx]

        # Can't delete the one you're currently playing
        if target == self.caller:
            self.caller.msg("|rYou can't delete the wrestler you're currently playing. Switch first.|n")
            return

        # Check for confirmation
        if len(args) < 2 or args[1].lower() != "confirm":
            self.caller.msg(
                f"\n|rAre you sure you want to delete |c{target.key}|r?|n\n"
                f"This is |rpermanent|n and cannot be undone.\n\n"
                f"Type |wchardelete {args[0]} confirm|n to delete.\n"
            )
            return

        # Remove from account's character list, then delete
        name = target.key
        account.characters.remove(target)
        target.delete()
        self.caller.msg(f"|r{name} has been deleted.|n")


class CmdCharCreate(Command):
    """
    Create a new wrestler on your account.

    Usage:
      charcreate

    Creates a new wrestler and launches character creation.
    You can have up to 10 wrestlers per account.
    """

    key = "charcreate"
    aliases = ["newwrestler"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        account = self.caller.account
        if not account:
            self.caller.msg("No account found.")
            return

        from django.conf import settings
        max_chars = getattr(settings, "MAX_NR_CHARACTERS", 10)
        chars = [c for c in account.characters if c.access(account, "puppet")]

        if len(chars) >= max_chars:
            self.caller.msg(f"|rYou already have {len(chars)} wrestlers (max {max_chars}).|n")
            return

        # Find chargen limbo room
        from evennia.utils.search import search_tag
        start_rooms = search_tag("chargen_limbo", category="chargen")
        start_loc = start_rooms[0] if start_rooms else None

        # Create the new wrestler
        new_char, errs = account.create_character(
            key=f"{account.key}_{len(chars) + 1}",
            typeclass="typeclasses.characters.Wrestler",
            location=start_loc,
            home=start_loc,
        )
        if not new_char:
            self.caller.msg(f"|rFailed to create wrestler: {errs}|n")
            return

        session = self.caller.sessions.get()[0] if self.caller.sessions.get() else None
        if not session:
            self.caller.msg("No active session found.")
            return

        self.caller.msg(f"\nCreating new wrestler... entering character creation.\n")

        # Unpuppet current, puppet new character (chargen fires via at_post_puppet)
        try:
            account.unpuppet_object(session)
            account.puppet_object(session, new_char)
        except RuntimeError as e:
            self.caller.msg(f"|rFailed to switch to new wrestler: {e}|n")
            logger.log_err(f"Character create/puppet failed for {account.key}: {e}")
