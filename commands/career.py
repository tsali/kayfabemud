"""
Kayfabe: Protect the Business — Career commands.

stats  — display character sheet
rank   — show rank progression and career XP
turn   — alignment turn (Face/Heel/Anti-Hero)
titles — show territory titles and current holders
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

        style = caller.db.wrestling_style or "Unknown"
        alignment = caller.db.alignment or "Unknown"
        rank = caller.get_rank()
        rank_color = RANK_COLORS.get(rank, "|w")

        # Alignment coloring
        if alignment == "Face":
            align_str = "|gFace|n"
        elif alignment == "Heel":
            align_str = "|rHeel|n"
        elif alignment == "Anti-Hero":
            align_str = "|yAnti-Hero|n"
        else:
            align_str = alignment

        # Header
        msg = (
            f"\n|w{'=' * 44}|n\n"
            f"|w  {caller.key}|n\n"
            f"|w{'=' * 44}|n\n"
        )

        # Identity
        msg += (
            f"  Real Name:  |c{caller.db.real_name}|n\n"
            f"  Hometown:   |c{caller.db.hometown}|n\n"
            f"  Style:      |c{style}|n\n"
            f"  Alignment:  {align_str}\n"
            f"  Rank:       {rank_color}{rank}|n\n"
            f"  Level:      |w{caller.db.level}|n\n"
        )

        # Territory
        territory = caller.db.territory or "None"
        tier = caller.db.tier or 1
        tier_names = {1: "Backyard", 2: "Training", 3: "Regional", 4: "National"}
        msg += f"  Territory:  |c{territory}|n (Tier {tier} — {tier_names.get(tier, '???')})\n"

        # Stats
        msg += f"\n|w  --- Stats ---{'':>25}|n\n"
        stat_order = ["str", "agi", "tec", "cha", "tou", "psy"]
        for key in stat_order:
            val = caller.get_stat(key)
            name = STAT_NAMES.get(key, key.upper())
            msg += f"  {name:12s} {_stat_bar(val)} {val:>5.1f}\n"

        # Finisher
        msg += f"\n  Finisher:   |c{caller.db.finisher_name}|n ({caller.db.finisher_type})\n"

        # Record
        wins = caller.db.wins or 0
        losses = caller.db.losses or 0
        draws = caller.db.draws or 0
        avg_quality = caller.get_match_quality_avg()
        msg += (
            f"\n|w  --- Record ---{'':>24}|n\n"
            f"  W-L-D:      |g{wins}|n-|r{losses}|n-|y{draws}|n\n"
            f"  Matches:    {caller.db.matches_wrestled or 0}\n"
            f"  Avg Stars:  {'%.1f' % avg_quality}\n"
        )

        # Kayfabe
        kayfabe = caller.db.kayfabe or 50
        if kayfabe >= 70:
            k_color = "|g"
        elif kayfabe >= 40:
            k_color = "|y"
        else:
            k_color = "|r"
        msg += f"  Kayfabe:    {k_color}{kayfabe}|n/100\n"

        if alignment == "Anti-Hero":
            rebel = caller.db.rebel_meter or 0
            msg += f"  Rebel:      |y{rebel}|n/100\n"

        # Economy
        msg += (
            f"\n|w  --- Economy ---{'':>23}|n\n"
            f"  Money:      |y${caller.db.money or 0}|n\n"
            f"  XP:         {caller.db.xp or 0}\n"
        )

        # Manager
        manager = caller.db.manager
        if manager:
            msg += f"  Manager:    |m{manager}|n\n"

        # Gear
        gear_names = ["Street Clothes", "Basic Trunks", "Custom Boots", "Entrance Jacket", "Full Custom Gear"]
        vehicle_names = ["On Foot", "Junker Car", "Reliable Sedan", "Van", "Tour Bus"]
        gear_tier = caller.db.gear_tier or 0
        vehicle_tier = caller.db.vehicle_tier or 0
        msg += f"  Gear:       {gear_names[min(gear_tier, 4)]}\n"
        msg += f"  Vehicle:    {vehicle_names[min(vehicle_tier, 4)]}\n"

        msg += f"|w{'=' * 44}|n\n"

        caller.msg(msg)


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
        from world.rules import TERRITORY_TITLES

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
                # TODO: Look up current holder from NPC data
                msg += f"    {title:40s} |x[Vacant]|n\n"

        msg += f"\n|w{'=' * 50}|n"
        self.caller.msg(msg)
