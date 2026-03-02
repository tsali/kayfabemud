"""
Kayfabe: Protect the Business — Championship commands.

Commands:
    titleshot - Request a title match (must be in PromoterOffice)
"""

from evennia.commands.command import Command


def _get_championship_registry():
    """Get or create the ChampionshipRegistryScript."""
    from evennia.scripts.models import ScriptDB
    try:
        registry = ScriptDB.objects.get(db_key="championship_registry")
        return registry
    except ScriptDB.DoesNotExist:
        from typeclasses.scripts import ChampionshipRegistryScript
        registry = ChampionshipRegistryScript.objects.create(db_key="championship_registry")
        registry.db.title_holders = {}
        registry.db.womens_title_holders = {}
        return registry
    except ScriptDB.MultipleObjectsReturned:
        return ScriptDB.objects.filter(db_key="championship_registry").first()


class CmdTitleShot(Command):
    """
    Request a title match from the promoter.

    Usage:
        titleshot

    Requirements:
        - Must be in a Promoter's Office
        - Rank >= Upper Midcarder (index 4)
        - Promoter trust >= 70
        - Must have a contract with this territory

    If approved, your next match will be a title match against
    the current champion (or for the vacant title).
    """
    key = "titleshot"
    aliases = ["title shot", "titlechallenge"]
    locks = "cmd:all()"
    help_category = "Career"

    def func(self):
        from typeclasses.rooms import PromoterOffice
        from world.rules import get_promoter_trust, TERRITORY_TITLES, TERRITORY_TITLES_WOMENS

        caller = self.caller

        if not isinstance(caller.location, PromoterOffice):
            caller.msg("|rYou need to be in a Promoter's Office to request a title shot.|n")
            return

        territory = caller.db.territory or ""
        if not territory:
            caller.msg("|rYou're not in a territory.|n")
            return

        # Check rank
        rank_idx = caller.db.rank_index or 0
        if rank_idx < 4:
            caller.msg(
                f"|rYou need Upper Midcarder rank (index 4) for a title shot.\n"
                f"Current rank: |w{caller.get_rank()}|r (index {rank_idx}).|n"
            )
            return

        # Check trust
        trust = get_promoter_trust(caller, territory)
        if trust < 70:
            caller.msg(
                f"|rThe promoter doesn't trust you enough for a title match.\n"
                f"Current trust: {trust}/100 (need 70).|n"
            )
            return

        # Check contract
        contract = caller.db.contract
        if not contract or contract.get("territory", "") != territory:
            caller.msg(
                f"|rYou need a contract with {territory} to get a title shot.\n"
                f"Use |wsign|r in this office first.|n"
            )
            return

        # Determine which title
        title_name = TERRITORY_TITLES.get(territory)
        if not title_name:
            caller.msg(f"|rThis territory doesn't have a championship.|n")
            return

        # Check gender for women's title option
        gender = caller.db.gender or "Undisclosed"
        womens_title = TERRITORY_TITLES_WOMENS.get(territory)

        registry = _get_championship_registry()
        holders = registry.db.title_holders or {}
        w_holders = registry.db.womens_title_holders or {}

        # Determine target title based on gender
        if gender == "Female" and womens_title:
            target_title = womens_title
            holder_info = w_holders.get(territory)
            title_type = "womens"
        elif gender in ("Non-Binary", "Undisclosed") and womens_title:
            # Open division: pick whichever is vacant, prefer main
            if not holders.get(territory):
                target_title = title_name
                holder_info = holders.get(territory)
                title_type = "main"
            elif not w_holders.get(territory):
                target_title = womens_title
                holder_info = w_holders.get(territory)
                title_type = "womens"
            else:
                target_title = title_name
                holder_info = holders.get(territory)
                title_type = "main"
        else:
            target_title = title_name
            holder_info = holders.get(territory)
            title_type = "main"

        # Set the title match flag on the player
        caller.db.pending_title_match = {
            "territory": territory,
            "title_name": target_title,
            "title_type": title_type,
        }

        if holder_info:
            champ = holder_info.get("holder", "???")
            defenses = holder_info.get("defenses", 0)
            caller.msg(
                f"\n|Y*** TITLE SHOT GRANTED ***|n\n"
                f"  Title: |c{target_title}|n\n"
                f"  Champion: |c{champ}|n ({defenses} defense{'s' if defenses != 1 else ''})\n\n"
                f"Your next match in this territory will be for the title!\n"
                f"Use |wwrestle|n to start the title match."
            )
        else:
            caller.msg(
                f"\n|Y*** TITLE SHOT GRANTED ***|n\n"
                f"  Title: |c{target_title}|n\n"
                f"  Status: |xVACANT|n\n\n"
                f"The title is vacant! Your next match will crown a new champion.\n"
                f"Use |wwrestle|n to compete for the gold."
            )
