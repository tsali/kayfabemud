"""
BBS Pepsicola MUD — Account typeclass.

BBS users connect via the rlogin bridge which auto-logs them in with a
shared secret password. Their Evennia account is created on first login.
AUTO_CREATE_CHARACTER_WITH_ACCOUNT = True (default) creates a Character
with the same name. AUTO_PUPPET_ON_LOGIN = True (default) auto-puppets
the character so users land in-game immediately with no OOC menu.
"""

from evennia.accounts.accounts import DefaultAccount, DefaultGuest
from evennia.utils import logger


class Account(DefaultAccount):
    """
    Account typeclass for BBS-connected players.

    Relies on Evennia defaults:
      - AUTO_CREATE_CHARACTER_WITH_ACCOUNT = True  → character created at account creation
      - AUTO_PUPPET_ON_LOGIN = True                → auto-puppeted on login (MULTISESSION_MODE 0)

    The at_post_login hook below handles the edge case where a player's
    character exists but was never saved as _last_puppet (e.g. after a
    server wipe). It finds their character by name and puppets it.
    """

    def at_post_login(self, session=None, **kwargs):
        """
        Called after successful login. Ensures the player lands in-game.
        Falls back to finding the character by account name if _last_puppet is gone.
        """
        super().at_post_login(session=session, **kwargs)

        # If we're already puppeting something, we're done.
        if session and self.get_puppet(session):
            return

        # Try to find a character matching this account name.
        from evennia import search_object
        chars = search_object(self.key, typeclass="typeclasses.characters.Character")
        if chars:
            char = chars[0]
            try:
                self.puppet_object(session, char)
                logger.log_info(f"Account '{self.key}' auto-puppeted character '{char.key}'")
            except RuntimeError as e:
                logger.log_err(f"Account '{self.key}' could not puppet '{char.key}': {e}")
        else:
            # Character doesn't exist yet — create one (shouldn't happen with
            # AUTO_CREATE_CHARACTER_WITH_ACCOUNT=True, but defensive fallback).
            logger.log_info(f"Account '{self.key}' has no character; creating one.")
            char, errs = self.create_character()
            if char:
                try:
                    self.puppet_object(session, char)
                except RuntimeError as e:
                    logger.log_err(f"Could not puppet newly created character: {e}")
            else:
                logger.log_err(f"Character creation failed for '{self.key}': {errs}")


class Guest(DefaultGuest):
    """Guest accounts — disabled by default, not used for BBS connections."""
    pass
