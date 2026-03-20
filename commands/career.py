"""
Kayfabe: Protect the Business — Career commands.

stats  — display character sheet
rank   — show rank progression and career XP
turn   — alignment turn (Face/Heel/Anti-Hero)
titles — show territory titles and current holders
shows  — view upcoming show card
"""

from evennia.commands.command import Command


STAT_NAMES = {
    "str": "Strength",
    "agi": "Agility",
    "tec": "Technical",
    "cha": "Charisma",
    "tou": "Toughness",
    "psy": "Psychology",
}

RANK_COLORS = {
    "Greenhorn": "|x",
    "Jobber": "|x",
    "Enhancement": "|w",
    "Midcarder": "|c",
    "Upper Midcarder": "|c",
    "Main Eventer": "|y",
    "Champion": "|Y",
    "Legend": "|R",
}


def _stat_bar(value, width=15):
    """Render a stat bar."""
    filled = min(int(value), width)
    empty = width - filled
    return f"|w{'#' * filled}|x{'.' * empty}|n"


class CmdStats(Command):
    """
    Display your wrestler's character sheet.

    Usage:
      stats

    Shows your ring name, stats, career record, alignment,
    rank, kayfabe score, and current territory.
    """

    key = "stats"
    aliases = ["sheet", "score", "whoami"]
    locks = "cmd:all()"
    help_category = "Career"

    def func(self):
        caller = self.caller
        if not caller.db.chargen_complete:
            caller.msg("You haven't created your wrestler yet.")
            return

        caller.msg(caller.get_stats_display())


class CmdRank(Command):
    """
    Show your rank progression and career milestones.

    Usage:
        rank

    Shows your current rank, career XP, and what's needed for the next rank.
    """
    key = "rank"
    aliases = ["career", "progression"]
    locks = "cmd:all()"
    help_category = "Career"

    def func(self):
        from world.rules import RANK_THRESHOLDS
        caller = self.caller

        if not caller.db.chargen_complete:
            caller.msg("You haven't created your wrestler yet.")
            return

        rank_idx = caller.db.rank_index or 0
        rank = caller.get_rank()
        total_career = (caller.db.wins or 0) * 20 + (caller.db.xp or 0)

        msg = f"\n|w{'=' * 44}|n\n|w  RANK PROGRESSION|n\n|w{'=' * 44}|n\n"
        msg += f"  Current Rank: |c{rank}|n\n"
        msg += f"  Career XP: |y{total_career}|n\n\n"

        for idx in sorted(RANK_THRESHOLDS.keys()):
            rname, threshold = RANK_THRESHOLDS[idx]
            if idx == rank_idx:
                marker = " |g<-- YOU ARE HERE|n"
            elif idx < rank_idx:
                marker = " |x[achieved]|n"
            else:
                marker = ""
            msg += f"  {rname:20s} ({threshold:>6} XP){marker}\n"

        # Next rank info
        next_idx = rank_idx + 1
        if next_idx in RANK_THRESHOLDS:
            next_name, next_threshold = RANK_THRESHOLDS[next_idx]
            remaining = max(0, next_threshold - total_career)
            msg += f"\n  Next rank: |w{next_name}|n — need |y{remaining}|n more career XP"
        else:
            msg += "\n  |YYou have reached the highest rank!|n"

        msg += f"\n|w{'=' * 44}|n"
        caller.msg(msg)


class CmdTurn(Command):
    """
    Turn your alignment — become a Face, Heel, or Anti-Hero.

    Usage:
        turn face
        turn heel
        turn antihero

    Alignment turns are major events in your career.
    Anti-Hero is only available at Midcarder rank (rank index 3) or above.

    A well-timed turn generates massive crowd heat.
    A poorly timed turn (same alignment, or too early for Anti-Hero) is rejected.
    """
    key = "turn"
    aliases = ["alignment"]
    locks = "cmd:all()"
    help_category = "Career"

    def func(self):
        from world.rules import kayfabe_change
        caller = self.caller

        if not caller.db.chargen_complete:
            caller.msg("You haven't created your wrestler yet.")
            return

        args = self.args.strip().lower()
        current = caller.db.alignment or "Face"

        if not args:
            caller.msg(
                f"Current alignment: |w{current}|n\n"
                f"Usage: turn <face|heel|antihero>"
            )
            return

        # Map input to alignment
        target_map = {
            "face": "Face",
            "babyface": "Face",
            "heel": "Heel",
            "antihero": "Anti-Hero",
            "anti-hero": "Anti-Hero",
            "tweener": "Anti-Hero",
        }

        target = target_map.get(args)
        if not target:
            caller.msg(f"|rUnknown alignment. Try: face, heel, antihero|n")
            return

        if target == current:
            caller.msg(f"|rYou're already a {current}.|n")
            return

        # Anti-Hero gate: must be Midcarder (rank 3) or above
        if target == "Anti-Hero":
            rank_idx = caller.db.rank_index or 0
            if rank_idx < 3:
                caller.msg(
                    "|rAnti-Hero alignment requires Midcarder rank or higher.\n"
                    f"You are currently: |w{caller.get_rank()}|r (rank {rank_idx}).\n"
                    "Keep climbing the ranks.|n"
                )
                return

        # Execute the turn
        if current == "Face" and target == "Heel":
            msg = (
                f"\n|r*** HEEL TURN ***\n"
                f"{caller.key} has turned on the fans!\n"
                f"The crowd is STUNNED! Boos rain down from every corner of the arena!|n\n"
            )
            kayfabe_change(caller, 5, "heel turn")
        elif current == "Heel" and target == "Face":
            msg = (
                f"\n|g*** FACE TURN ***\n"
                f"{caller.key} has seen the light!\n"
                f"The crowd ERUPTS with cheers! A new hero is born!|n\n"
            )
            kayfabe_change(caller, 5, "face turn")
        elif target == "Anti-Hero":
            msg = (
                f"\n|y*** ANTI-HERO TURN ***\n"
                f"{caller.key} refuses to play by anyone's rules!\n"
                f"The crowd doesn't know whether to cheer or boo — they just know\n"
                f"they can't take their eyes off this wildcard!|n\n"
            )
            kayfabe_change(caller, 3, "anti-hero turn")
            caller.db.rebel_meter = 50  # Start rebel meter at 50
        elif current == "Anti-Hero":
            direction = "face" if target == "Face" else "heel"
            msg = (
                f"\n|w*** {caller.key} picks a side! ***\n"
                f"The Anti-Hero commits fully to the {direction} path.\n"
                f"The crowd knows exactly where {caller.key} stands now.|n\n"
            )
            kayfabe_change(caller, 2, f"anti-hero to {direction}")
            caller.db.rebel_meter = 0
        else:
            msg = f"\n|w{caller.key} has turned {target}!|n\n"

        caller.db.alignment = target

        # Announce to room
        if caller.location:
            caller.location.msg_contents(msg, exclude=[caller])
        caller.msg(msg)
        caller.msg(f"Your alignment is now: |w{target}|n")


class CmdTitles(Command):
    """
    View territory championships.

    Usage:
        titles

    Shows all territory titles and their current holders (if any).
    """
    key = "titles"
    aliases = ["championships", "belts"]
    locks = "cmd:all()"
    help_category = "Career"

    def func(self):
        from world.rules import TERRITORY_TITLES, TERRITORY_TITLES_WOMENS

        # Try to get championship registry
        holders = {}
        w_holders = {}
        try:
            from evennia.scripts.models import ScriptDB
            registry = ScriptDB.objects.get(db_key="championship_registry")
            holders = registry.db.title_holders or {}
            w_holders = registry.db.womens_title_holders or {}
        except Exception:
            pass

        msg = f"\n|w{'=' * 50}|n\n|w  TERRITORY CHAMPIONSHIPS|n\n|w{'=' * 50}|n\n"

        tier_groups = {
            "Tier 3 — Regional": ["memphis", "midsouth", "midatlantic", "florida",
                                   "georgia", "wccw", "awa", "stampede", "pnw"],
            "Tier 3.5 — Developmental": ["ovw", "fcw", "dsw", "hwa"],
            "Tier 4 — National / International": ["wwf", "wcw", "ecw", "uk", "japan"],
        }

        for tier_name, territories in tier_groups.items():
            msg += f"\n  |c{tier_name}|n\n"
            for terr in territories:
                title = TERRITORY_TITLES.get(terr, "Unknown Title")
                holder_info = holders.get(terr)
                if holder_info:
                    champ = holder_info.get("holder", "???")
                    defenses = holder_info.get("defenses", 0)
                    msg += f"    {title:40s} |Y{champ}|n ({defenses} def.)\n"
                else:
                    msg += f"    {title:40s} |x[Vacant]|n\n"
                # Show women's title if this territory has one
                w_title = TERRITORY_TITLES_WOMENS.get(terr)
                if w_title:
                    w_info = w_holders.get(terr)
                    if w_info:
                        w_champ = w_info.get("holder", "???")
                        w_def = w_info.get("defenses", 0)
                        msg += f"    {w_title:40s} |Y{w_champ}|n ({w_def} def.)\n"
                    else:
                        msg += f"    {w_title:40s} |x[Vacant]|n\n"

        msg += f"\n|w{'=' * 50}|n"
        self.caller.msg(msg)


class CmdShows(Command):
    """
    View upcoming show cards.

    Usage:
        shows           - Show card for your current territory
        shows <territory> - Show card for a specific territory
        showhistory     - View past show results
    """
    key = "shows"
    aliases = ["showcard", "showhistory"]
    locks = "cmd:all()"
    help_category = "Career"

    def func(self):
        from world.shows import format_show_card

        caller = self.caller
        args = self.args.strip().lower()

        # Show history mode
        if self.cmdstring.lower() == "showhistory":
            self._show_history(caller)
            return

        territory = args if args else (caller.db.territory or "")
        if not territory:
            caller.msg("|rYou're not in a territory. Use: shows <territory>|n")
            return

        try:
            from evennia.scripts.models import ScriptDB
            scheduler = ScriptDB.objects.get(db_key="show_scheduler")
            upcoming = scheduler.db.upcoming_shows or {}
        except Exception:
            caller.msg("No shows are currently scheduled.")
            return

        show = upcoming.get(territory)
        if not show:
            caller.msg(f"No upcoming shows in {territory}.")
            return

        caller.msg(format_show_card(show))

    def _show_history(self, caller):
        try:
            from evennia.scripts.models import ScriptDB
            scheduler = ScriptDB.objects.get(db_key="show_scheduler")
            history = scheduler.db.show_history or []
        except Exception:
            caller.msg("No show history available.")
            return

        if not history:
            caller.msg("No past shows recorded yet.")
            return

        msg = f"\n|w{'=' * 50}|n\n|w  SHOW HISTORY|n\n|w{'=' * 50}|n\n"
        for show in reversed(history[-10:]):
            msg += f"  |c{show.get('name', '???')}|n ({show.get('territory', '???')})\n"
            for match in show.get("matches", [])[:3]:
                msg += f"    {match['wrestler_a']} vs {match['wrestler_b']}\n"
            if len(show.get("matches", [])) > 3:
                msg += f"    ... and {len(show['matches']) - 3} more matches\n"
            msg += "\n"
        msg += f"|w{'=' * 50}|n"
        caller.msg(msg)
