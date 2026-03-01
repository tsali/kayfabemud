"""
Kayfabe: Protect the Business — Wrestler Character typeclass.

Uses Evennia's TraitHandler contrib for the 6 core stats.
"""

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
        """Get current value of a stat."""
        trait = self.traits.get(stat_key)
        return trait.value if trait else 0

    def get_match_quality_avg(self):
        """Average star rating across all matches."""
        if self.db.matches_wrestled > 0:
            return self.db.match_quality_total / self.db.matches_wrestled
        return 0.0

    def get_rank(self):
        """Return current career rank string."""
        return CAREER_RANKS[min(self.db.rank_index, len(CAREER_RANKS) - 1)]

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
        else:
            # Normal login message
            self.msg(
                f"\n|w*** KAYFABE: Protect the Business ***|n\n"
                f"Welcome back, |c{self.key}|n. "
                f"You are at |w{self.location.key}|n.\n"
            )
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
