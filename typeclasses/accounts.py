"""
Kayfabe: Protect the Business — Account typeclass.

BBS users connect via the rlogin bridge which auto-logs them in with a
shared secret password. Their Evennia account is created on first login.
"""

from evennia.accounts.accounts import DefaultAccount, DefaultGuest
from evennia.utils import logger


class Account(DefaultAccount):
    """
    Account typeclass for BBS-connected players.

    On first login, AUTO_CREATE_CHARACTER_WITH_ACCOUNT creates a Wrestler.
    The Wrestler's at_post_puppet launches chargen if not yet completed.
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
        from evennia.utils.search import search_object
        chars = search_object(self.key, typeclass="typeclasses.characters.Wrestler")
        if not chars:
            # Fallback: search for old Character typeclass too
            chars = search_object(self.key, typeclass="typeclasses.characters.Character")
        if chars:
            char = chars[0]
            try:
                self.puppet_object(session, char)
                logger.log_info(f"Account '{self.key}' auto-puppeted character '{char.key}'")
            except RuntimeError as e:
                logger.log_err(f"Account '{self.key}' could not puppet '{char.key}': {e}")
        else:
            # Character doesn't exist — create one
            logger.log_info(f"Account '{self.key}' has no character; creating one.")
            from evennia.utils.search import search_tag
            # Find chargen room
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


class Guest(DefaultGuest):
    """Guest accounts — disabled."""
    pass
