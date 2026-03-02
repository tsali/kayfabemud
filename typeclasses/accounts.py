"""
Kayfabe: Protect the Business — Account typeclass.

BBS users connect via the rlogin bridge which auto-logs them in with a
shared secret password. Their Evennia account is created on first login.

Multi-character support: accounts can have up to MAX_NR_CHARACTERS wrestlers.
AUTO_PUPPET_ON_LOGIN puppets the first character automatically (bridge compat).
If the account has 2+ characters, `charselect` command is available in-game.
"""

from evennia.accounts.accounts import DefaultAccount, DefaultGuest
from evennia.utils import logger


class Account(DefaultAccount):
    """
    Account typeclass for BBS-connected players.

    On first login, AUTO_CREATE_CHARACTER_WITH_ACCOUNT creates a Wrestler.
    The Wrestler's at_post_puppet launches chargen if not yet completed.

    Multi-character: use `charselect` and `charcreate` commands in-game.
    """

    def at_post_login(self, session=None, **kwargs):
        """
        Called after successful login. Ensures the player lands in-game.

        Uses self.characters (Evennia's built-in account<->character list)
        instead of searching by key, which broke when chargen changed the key.
        """
        super().at_post_login(session=session, **kwargs)

        # If we're already puppeting something (AUTO_PUPPET_ON_LOGIN handled it), done.
        if session and self.get_puppet(session):
            return

        # Use the account's character list
        chars = [c for c in self.characters if c.access(self, "puppet")]
        if not chars:
            # No characters — create one (shouldn't happen with AUTO_CREATE, but safety net)
            logger.log_info(f"Account '{self.key}' has no characters; creating one.")
            from evennia.utils.search import search_tag
            start_rooms = search_tag("chargen_limbo", category="chargen")
            start_loc = start_rooms[0] if start_rooms else None

            char, errs = self.create_character(
                key=self.key,
                typeclass="typeclasses.characters.Wrestler",
                location=start_loc,
                home=start_loc,
            )
            if char:
                try:
                    self.puppet_object(session, char)
                except RuntimeError as e:
                    logger.log_err(f"Could not puppet newly created character: {e}")
            else:
                logger.log_err(f"Character creation failed for '{self.key}': {errs}")
            return

        # Puppet the first available character
        char = chars[0]
        try:
            self.puppet_object(session, char)
            logger.log_info(f"Account '{self.key}' auto-puppeted '{char.key}'")
        except RuntimeError as e:
            logger.log_err(f"Account '{self.key}' could not puppet '{char.key}': {e}")


class Guest(DefaultGuest):
    """Guest accounts — disabled."""
    pass
