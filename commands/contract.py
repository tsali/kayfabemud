"""
Kayfabe: Protect the Business — Contract commands.

Commands:
    contract - View your current contract
    sign     - Sign a contract with current territory's promoter
"""

from evennia.commands.command import Command


CONTRACT_PAY = {
    0: ("Greenhorn", 20),
    1: ("Jobber", 40),
    2: ("Enhancement", 75),
    3: ("Midcarder", 150),
    4: ("Upper Midcarder", 300),
    5: ("Main Eventer", 600),
    6: ("Champion", 1000),
    7: ("Legend", 1500),
}


class CmdContract(Command):
    """
    View your current contract.

    Usage:
        contract

    Shows contract details including territory, weekly pay,
    and weeks remaining.
    """
    key = "contract"
    locks = "cmd:all()"
    help_category = "Career"

    def func(self):
        caller = self.caller
        contract = caller.db.contract

        if not contract:
            caller.msg(
                "You don't have a contract.\n"
                "Visit a |wPromoter's Office|n and use |wsign|n to get one."
            )
            return

        territory = contract.get("territory", "???")
        weeks = contract.get("weeks_remaining", 0)
        pay = contract.get("weekly_pay", 0)

        msg = (
            f"\n|w{'=' * 44}|n\n"
            f"|w  CONTRACT|n\n"
            f"|w{'=' * 44}|n\n"
            f"  Territory:      |c{territory}|n\n"
            f"  Weekly Pay:     |y${pay}|n\n"
            f"  Weeks Left:     |w{weeks}|n\n"
            f"|w{'=' * 44}|n"
        )
        caller.msg(msg)


class CmdSign(Command):
    """
    Sign a contract with the current territory's promoter.

    Usage:
        sign

    Must be used in a Promoter's Office. Requires promoter trust >= 40.
    Pay is based on your rank. Duration is 4-12 game weeks.
    """
    key = "sign"
    locks = "cmd:all()"
    help_category = "Career"

    def func(self):
        import random
        from typeclasses.rooms import PromoterOffice
        from world.rules import get_promoter_trust

        caller = self.caller

        # Must be in promoter office
        if not isinstance(caller.location, PromoterOffice):
            caller.msg("|rYou need to be in a Promoter's Office to sign a contract.|n")
            return

        # Check existing contract
        if caller.db.contract:
            contract = caller.db.contract
            caller.msg(
                f"|rYou already have a contract with {contract['territory']}.\n"
                f"Wait for it to expire ({contract['weeks_remaining']} weeks left).|n"
            )
            return

        territory = caller.db.territory or ""
        if not territory:
            caller.msg("|rYou're not in a territory.|n")
            return

        # Check trust
        trust = get_promoter_trust(caller, territory)
        if trust < 40:
            caller.msg(
                f"|rThe promoter doesn't trust you enough to offer a contract.\n"
                f"Current trust: {trust}/100 (need 40).|n"
            )
            return

        # Calculate pay based on rank
        rank_idx = caller.db.rank_index or 0
        rank_name, weekly_pay = CONTRACT_PAY.get(rank_idx, ("???", 20))

        # Trust bonus to pay
        if trust >= 80:
            weekly_pay = int(weekly_pay * 1.25)
        elif trust >= 60:
            weekly_pay = int(weekly_pay * 1.1)

        # Duration: 4-12 weeks, higher trust = longer offer
        base_duration = 4
        trust_bonus_weeks = (trust - 40) // 15
        duration = min(12, base_duration + trust_bonus_weeks + random.randint(0, 2))

        import time
        caller.db.contract = {
            "territory": territory,
            "weeks_remaining": duration,
            "weekly_pay": weekly_pay,
            "signed_at": time.time(),
        }

        # Dirt sheet: log contract signing
        from world.dirtsheet import log_event
        log_event("contract", name=caller.key, territory=territory, pay=weekly_pay)

        caller.msg(
            f"\n|g*** CONTRACT SIGNED ***|n\n"
            f"  Territory: |c{territory}|n\n"
            f"  Weekly Pay: |y${weekly_pay}|n\n"
            f"  Duration: |w{duration} weeks|n\n\n"
            f"The promoter shakes your hand. Welcome aboard."
        )
        if caller.location:
            caller.location.msg_contents(
                f"|w{caller.key} has signed a contract with {territory}!|n",
                exclude=[caller],
            )
