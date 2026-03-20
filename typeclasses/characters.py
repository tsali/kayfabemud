"""
Kayfabe: Protect the Business — Wrestler Character typeclass.

Uses Evennia's TraitHandler contrib for the 6 core stats.
"""

import time

from evennia.objects.objects import DefaultCharacter
from evennia.utils import lazy_property

from .objects import ObjectParent

# Wrestling styles and their starting stat bonuses
WRESTLING_STYLES = {
    "Brawler": {"str": 3, "tou": 3, "agi": 0, "tec": 0, "cha": 2, "psy": 2},
    "Technical": {"str": 0, "tou": 1, "agi": 1, "tec": 4, "cha": 1, "psy": 3},
    "High-Flyer": {"str": 0, "tou": 1, "agi": 4, "tec": 2, "cha": 2, "psy": 1},
    "Showman": {"str": 1, "tou": 1, "agi": 1, "tec": 0, "cha": 4, "psy": 3},
    "All-Rounder": {"str": 2, "tou": 2, "agi": 1, "tec": 2, "cha": 1, "psy": 2},
}

# Career rank progression
CAREER_RANKS = [
    "Greenhorn",
    "Jobber",
    "Enhancement",
    "Midcarder",
    "Upper Midcarder",
    "Main Eventer",
    "Champion",
    "Legend",
]

# Alignment options
ALIGNMENTS = ("Face", "Heel", "Anti-Hero")


class Wrestler(ObjectParent, DefaultCharacter):
    """
    The Wrestler typeclass for player characters in Kayfabe.

    Attributes stored via db:
        chargen_complete (bool): Whether character creation is done
        real_name (str): Wrestler's real/shoot name
        hometown (str): Where they're from
        wrestling_style (str): Brawler/Technical/High-Flyer/Showman/All-Rounder
        alignment (str): Face/Heel/Anti-Hero
        rank (str): Current career rank
        rank_index (int): Index into CAREER_RANKS
        kayfabe (int): Kayfabe score 0-100
        rebel_meter (int): Anti-Hero rebel meter 0-100
        wins (int): Career wins
        losses (int): Career losses
        draws (int): Career draws
        match_quality_total (float): Sum of star ratings
        matches_wrestled (int): Total matches
        money (int): Current funds in dollars
        xp (int): Experience points
        level (int): Character level
        territory (str): Current territory key
        tier (int): Current tier (1-4)
        manager (str): Key of current manager NPC (or "")
        promoter_trust (dict): {territory_key: int} trust per territory
        gear_tier (int): 0-4 gear quality
        vehicle_tier (int): 0-3 vehicle quality
        finisher_name (str): Name of finishing move
        finisher_type (str): power/technical/aerial/charisma
    """

    @lazy_property
    def traits(self):
        from evennia.contrib.rpg.traits import TraitHandler
        return TraitHandler(self)

    def at_object_creation(self):
        """Called once when first created."""
        super().at_object_creation()

        # Mark chargen as incomplete — EvMenu will fire on first puppet
        self.db.chargen_complete = False

        # Identity
        self.db.real_name = ""
        self.db.hometown = ""
        self.db.gender = "Undisclosed"
        self.db.wrestling_style = ""
        self.db.alignment = "Face"

        # Career
        self.db.rank = "Greenhorn"
        self.db.rank_index = 0
        self.db.kayfabe = 50
        self.db.rebel_meter = 0

        # Record
        self.db.wins = 0
        self.db.losses = 0
        self.db.draws = 0
        self.db.match_quality_total = 0.0
        self.db.matches_wrestled = 0

        # Economy
        self.db.money = 50  # start with $50
        self.db.xp = 0
        self.db.level = 1

        # Location tracking
        self.db.territory = ""
        self.db.tier = 1

        # Manager
        self.db.manager = ""

        # Trust per territory
        self.db.promoter_trust = {}

        # Gear, equipment & vehicle
        self.db.gear_tier = 0
        self.db.equipment_tier = 0
        self.db.vehicle_tier = 0

        # Finisher
        self.db.finisher_name = ""
        self.db.finisher_type = ""

        # Fatigue & Rest
        self.db.fatigue_stacks = 0
        self.db.rest_bonus_active = {}  # e.g. {"all": 2}
        self.db.rest_bonus_expires = 0  # timestamp when rest bonus expires

        # Player Houses
        self.db.owned_houses = []  # list of house dbref ids

        # Match History (Phase 1)
        self.db.match_history = []  # list of dicts, capped at 50
        self.db.best_match_stars = 0.0
        self.db.best_match_opponent = ""
        self.db.rivals = {}  # {opponent_name: times_faced}

        # Injury (Phase 3)
        self.db.injury = None  # dict or None

        # Contract (Phase 3)
        self.db.contract = None  # dict or None

        # Stable (Phase 2)
        self.db.stable = ""  # stable name if in one

    def setup_traits(self):
        """Initialize the 6 core stats. Called during chargen after style is chosen."""
        for stat_key, stat_name in [
            ("str", "Strength"),
            ("agi", "Agility"),
            ("tec", "Technical"),
            ("cha", "Charisma"),
            ("tou", "Toughness"),
            ("psy", "Psychology"),
        ]:
            self.traits.add(
                stat_key,
                stat_name,
                trait_type="static",
                base=5,
                min=1,
                max=30,
            )

    def apply_style_bonuses(self):
        """Apply wrestling style stat bonuses."""
        style = self.db.wrestling_style
        if style in WRESTLING_STYLES:
            for stat_key, bonus in WRESTLING_STYLES[style].items():
                if bonus > 0:
                    trait = self.traits.get(stat_key)
                    if trait:
                        trait.base += bonus

    def apply_bonus_points(self, point_dict):
        """Apply player-allocated bonus points. point_dict = {stat_key: points}."""
        for stat_key, points in point_dict.items():
            if points > 0:
                trait = self.traits.get(stat_key)
                if trait:
                    trait.base += points

    def get_stat(self, stat_key):
        """Get current value of a stat, with fatigue penalty and rest bonus."""
        trait = self.traits.get(stat_key)
        if not trait:
            return 0
        value = trait.value

        # Apply fatigue penalty: -5% per stack
        fatigue = self.db.fatigue_stacks or 0
        if fatigue > 0:
            penalty = fatigue * 0.05
            value = value * (1.0 - penalty)

        # Apply rest bonus if active and not expired
        rest_bonus = self.db.rest_bonus_active or {}
        expires = self.db.rest_bonus_expires or 0
        if rest_bonus and time.time() < expires:
            all_bonus = rest_bonus.get("all", 0)
            stat_bonus = rest_bonus.get(stat_key, 0)
            value += all_bonus + stat_bonus
        elif rest_bonus and time.time() >= expires:
            # Expired — clear it
            self.db.rest_bonus_active = {}
            self.db.rest_bonus_expires = 0

        # Apply injury penalty
        injury = self.db.injury
        if injury and injury.get("stat_penalty") == stat_key:
            value -= injury.get("penalty_amount", 0)

        return max(1, int(value))

    def clear_fatigue(self):
        """Clear all fatigue stacks."""
        self.db.fatigue_stacks = 0

    def apply_rest_bonus(self, bonus_dict, duration=43200):
        """Apply rest bonus. duration defaults to 12 hours (43200 seconds)."""
        self.db.rest_bonus_active = bonus_dict
        self.db.rest_bonus_expires = time.time() + duration

    def is_in_safe_lodging(self):
        """Check if character is in an InnRoom or owned PlayerHouse."""
        from typeclasses.rooms import InnRoom, PlayerHouse
        loc = self.location
        if not loc:
            return False
        if isinstance(loc, InnRoom):
            return True
        if isinstance(loc, PlayerHouse):
            owner = loc.db.owner or ""
            allowed = loc.db.allowed_players or []
            if owner == self.key or self.key in allowed:
                return True
        return False

    def get_match_quality_avg(self):
        """Average star rating across all matches."""
        if self.db.matches_wrestled > 0:
            return self.db.match_quality_total / self.db.matches_wrestled
        return 0.0

    def get_rank(self):
        """Return current career rank string."""
        return CAREER_RANKS[min(self.db.rank_index, len(CAREER_RANKS) - 1)]

    def get_current_objective(self):
        """Derive the player's current objective from game state."""
        # Injured
        injury = self.db.injury
        if injury:
            return "You're injured. Rest at an inn to recover."

        # Exhaustion
        fatigue = self.db.fatigue_stacks or 0
        if fatigue >= 3:
            return "Exhaustion is hurting you. Find an inn and type: |wrest|n"

        # First match
        matches = self.db.matches_wrestled or 0
        if matches == 0:
            return "Challenge a wrestler! Type: |wwrestle <name>|n"

        # Early wins
        wins = self.db.wins or 0
        if wins > 0 and wins < 5:
            remaining = 5 - wins
            return f"Win {remaining} more match{'es' if remaining != 1 else ''} to prove yourself. Type: |wcard|n"

        # Rank-up eligible
        from world.rules import RANK_THRESHOLDS
        rank_idx = self.db.rank_index or 0
        next_idx = rank_idx + 1
        if next_idx in RANK_THRESHOLDS:
            _, threshold = RANK_THRESHOLDS[next_idx]
            total_career = (self.db.wins or 0) * 20 + (self.db.xp or 0)
            if total_career >= threshold:
                return "You have enough XP to rank up! The business is taking notice."

        # Outgrown backyard
        tier = self.db.tier or 1
        if tier == 1 and rank_idx >= 2:
            return "You've outgrown backyard feds. Type: |wtravel|n"

        # Low on cash
        money = self.db.money or 0
        if money < 20:
            return "Running low on cash. Try: |wsidejob|n"

        # No contract at higher tiers
        contract = self.db.contract
        if not contract and tier >= 3:
            return "Sign a contract for steady income. Visit a Promoter's Office."

        # Default
        return "Win matches and build your reputation. Type: |wcard|n"

    def get_stats_display(self):
        """Build a formatted stats display string, reusable from login and stats command."""
        from commands.career import STAT_NAMES, RANK_COLORS, _stat_bar

        style = self.db.wrestling_style or "Unknown"
        alignment = self.db.alignment or "Unknown"
        rank = self.get_rank()
        rank_color = RANK_COLORS.get(rank, "|w")

        if alignment == "Face":
            align_str = "|gFace|n"
        elif alignment == "Heel":
            align_str = "|rHeel|n"
        elif alignment == "Anti-Hero":
            align_str = "|yAnti-Hero|n"
        else:
            align_str = alignment

        territory = self.db.territory or "None"
        tier = self.db.tier or 1
        tier_names = {1: "Backyard", 2: "Training", 3: "Regional", 3.5: "Developmental", 4: "National"}
        tier_label = tier_names.get(tier, f"Tier {tier}")

        gender = self.db.gender or "Undisclosed"
        division_map = {
            "Male": "Men's Division",
            "Female": "Women's Division",
            "Non-Binary": "Open Division",
            "Undisclosed": "Open Division",
        }
        division = division_map.get(gender, "Open Division")

        wins = self.db.wins or 0
        losses = self.db.losses or 0
        draws = self.db.draws or 0
        avg_quality = self.get_match_quality_avg()

        msg = f"\n|w{'=' * 50}|n\n|w  WRESTLER STATUS: {self.key}|n\n|w{'=' * 50}|n\n"

        # Identity
        msg += (
            f"  {style} {align_str} | {rank_color}{rank}|n | Lv {self.db.level or 1}\n"
            f"  {territory} ({tier_label}) | {division}\n"
        )

        # Stats
        msg += f"\n|w  --- STATS ---{'':>30}|n\n"
        stat_order = ["str", "agi", "tec", "cha", "tou", "psy"]
        for key in stat_order:
            val = self.get_stat(key)
            name = STAT_NAMES.get(key, key.upper())
            msg += f"  {name:12s} {_stat_bar(val)} {val:>5.1f}\n"

        # Record
        msg += (
            f"\n|w  --- RECORD ---{'':>29}|n\n"
            f"  W-L-D: |g{wins}|n-|r{losses}|n-|y{draws}|n"
            f"  Avg Stars: {'%.1f' % avg_quality}"
        )
        best_stars = self.db.best_match_stars or 0
        if best_stars > 0:
            msg += f"  Best: {'%.1f' % best_stars} vs {self.db.best_match_opponent or '???'}"
        # Find top rival
        rivals = self.db.rivals or {}
        if rivals:
            top_rival = max(rivals, key=rivals.get)
            msg += f"\n  Rival: |c{top_rival}|n ({rivals[top_rival]} matches)"
        msg += "\n"

        # Business
        kayfabe = self.db.kayfabe or 50
        if kayfabe >= 70:
            k_color = "|g"
        elif kayfabe >= 40:
            k_color = "|y"
        else:
            k_color = "|r"

        msg += (
            f"\n|w  --- BUSINESS ---{'':>27}|n\n"
            f"  Money: |y${self.db.money or 0}|n  XP: {self.db.xp or 0}"
            f"  Kayfabe: {k_color}{kayfabe}|n/100\n"
        )
        if self.db.alignment == "Anti-Hero":
            msg += f"  Rebel: |y{self.db.rebel_meter or 0}|n/100\n"
        if self.db.manager:
            msg += f"  Manager: |m{self.db.manager}|n\n"
        contract = self.db.contract
        if contract:
            msg += f"  Contract: {contract.get('territory', '???')} (${contract.get('weekly_pay', 0)}/wk, {contract.get('weeks_remaining', 0)} wks)\n"

        gear_names = ["Street Clothes", "Basic Trunks", "Custom Boots", "Entrance Jacket", "Full Custom Gear"]
        vehicle_names = ["On Foot", "Junker Car", "Reliable Sedan", "Van", "Tour Bus"]
        gear_tier = self.db.gear_tier or 0
        vehicle_tier = self.db.vehicle_tier or 0
        msg += f"  Gear: {gear_names[min(gear_tier, 4)]}  Vehicle: {vehicle_names[min(vehicle_tier, 4)]}\n"
        msg += f"  Finisher: |c{self.db.finisher_name or 'None'}|n ({self.db.finisher_type or '???'})\n"

        # Effects (only if active)
        effects = []
        fatigue = self.db.fatigue_stacks or 0
        if fatigue > 0:
            effects.append(f"|rFatigue x{fatigue} (-{fatigue * 5}% all)|n")
        injury = self.db.injury
        if injury:
            effects.append(f"|r{injury.get('severity_name', 'Injured')}: {injury.get('name', '???')}|n")
        rest_bonus = self.db.rest_bonus_active or {}
        expires = self.db.rest_bonus_expires or 0
        if rest_bonus and time.time() < expires:
            remaining = int(expires - time.time())
            hours = remaining // 3600
            mins = (remaining % 3600) // 60
            all_b = rest_bonus.get("all", 0)
            effects.append(f"|gWell-Rested +{all_b} ({hours}h {mins}m)|n")
        if effects:
            msg += f"\n|w  --- EFFECTS ---{'':>28}|n\n"
            for eff in effects:
                msg += f"  {eff}\n"

        # Objective
        msg += f"\n|y>> NEXT:|n {self.get_current_objective()}\n"
        msg += f"|w{'=' * 50}|n"

        return msg

    def at_post_puppet(self, **kwargs):
        """Called after puppeting. Launch chargen if not complete."""
        super().at_post_puppet(**kwargs)

        if not self.db.chargen_complete:
            from evennia.utils.evmenu import EvMenu
            EvMenu(
                self,
                "commands.chargen",
                startnode="node_welcome",
                cmd_on_exit=None,
            )
        elif not self.db.territory:
            # Chargen finished but disconnected before choosing a starting fed.
            # Resume at fed selection.
            from evennia.utils.evmenu import EvMenu
            self.msg(
                "\n|wYou still need to pick your starting federation.|n\n"
            )
            EvMenu(
                self,
                "commands.chargen",
                startnode="node_starting_fed_intro",
                cmd_on_exit=None,
            )
        else:
            # Normal login — condensed status
            rank = self.get_rank()
            wins = self.db.wins or 0
            losses = self.db.losses or 0
            territory = self.db.territory or "Unknown"
            tier = self.db.tier or 1
            tier_names = {1: "Backyard", 2: "Training", 3: "Regional", 3.5: "Developmental", 4: "National"}
            tier_label = tier_names.get(tier, f"Tier {tier}")

            self.msg(
                f"\n|w*** KAYFABE: Protect the Business ***|n\n"
                f"Welcome back, |c{self.key}|n.\n"
                f"|w{rank}|n | Lv {self.db.level or 1} | "
                f"|g{wins}|nW-|r{losses}|nL | "
                f"|y${self.db.money or 0}|n | "
                f"{territory} ({tier_label})\n"
            )

            # Show active effects (compact)
            fatigue = self.db.fatigue_stacks or 0
            if fatigue > 0:
                penalty = fatigue * 5
                self.msg(
                    f"|r  Fatigue x{fatigue} (-{penalty}% all checks)"
                    f" — rest at an inn to clear|n"
                )

            rest_bonus = self.db.rest_bonus_active or {}
            expires = self.db.rest_bonus_expires or 0
            if rest_bonus and time.time() < expires:
                remaining = int(expires - time.time())
                hours = remaining // 3600
                mins = (remaining % 3600) // 60
                all_b = rest_bonus.get("all", 0)
                self.msg(
                    f"|g  Well-Rested: +{all_b} all stats ({hours}h {mins}m remaining)|n"
                )

            injury = self.db.injury
            if injury:
                self.msg(
                    f"|r  Injured: {injury.get('severity_name', '???')} "
                    f"{injury.get('name', '???')}|n"
                )

            # Current objective
            self.msg(f"\n|y>> NEXT:|n {self.get_current_objective()}\n")

            self.execute_cmd("look")

    def get_display_name(self, looker=None, **kwargs):
        """Show alignment tag next to name."""
        name = super().get_display_name(looker, **kwargs)
        if self.db.chargen_complete and self.db.alignment:
            align = self.db.alignment
            if align == "Face":
                return f"{name} |g[Face]|n"
            elif align == "Heel":
                return f"{name} |r[Heel]|n"
            elif align == "Anti-Hero":
                return f"{name} |y[Anti-Hero]|n"
        return name
