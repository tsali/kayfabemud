"""
Kayfabe: Protect the Business — Room typeclasses.

Room hierarchy:
  Room (base)
    TerritoryRoom — any room that belongs to a territory/zone
      BackyardFedRoom — Tier 1 small fed venues
      TrainingSchoolRoom — Tier 2 training schools
      ArenaRoom — match venues in Tier 3-4 territories
      GymRoom — training rooms (stat gains)
      BarRoom — social/kayfabe event rooms
      TravelHub — exits to other territories
      LockerRoom — backstage area
      PromoterOffice — booking, trust interactions
      UniqueRoom — territory-specific special locations
    ChargenRoom — limbo room for character creation
"""

from evennia.objects.objects import DefaultRoom

from .objects import ObjectParent


class Room(ObjectParent, DefaultRoom):
    """Base room for Kayfabe."""
    pass


class ChargenRoom(ObjectParent, DefaultRoom):
    """Limbo room where new characters go through character creation."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.desc = (
            "You stand in darkness. The distant roar of a crowd echoes around "
            "you. A single spotlight cuts through the black, waiting for you "
            "to step into it.\n\n"
            "Your story is about to begin."
        )


class TerritoryRoom(ObjectParent, DefaultRoom):
    """
    Base class for all rooms within a territory zone.

    Attributes:
        territory_key (str): Key of the territory this room belongs to
        territory_name (str): Display name of the territory
        tier (int): Tier level (1-4)
        room_type (str): Type identifier (arena, gym, bar, etc.)
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.territory_key = ""
        self.db.territory_name = ""
        self.db.tier = 1
        self.db.room_type = "generic"

    def get_display_header(self, looker, **kwargs):
        """Show territory info in room header."""
        territory = self.db.territory_name or "Unknown"
        tier = self.db.tier or 1
        tier_names = {1: "Backyard", 2: "Training", 3: "Regional", 3.5: "Developmental", 4: "National"}
        tier_label = tier_names.get(tier, f"Tier {tier}")
        return f"|w[{territory}]|n |x({tier_label})|n"


class BackyardFedRoom(TerritoryRoom):
    """Tier 1 small fed venues — VFW halls, backyards, fairgrounds."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.tier = 1
        self.db.room_type = "backyard"


class TrainingSchoolRoom(TerritoryRoom):
    """Tier 2 training school rooms."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.tier = 2
        self.db.room_type = "training"


class ArenaRoom(TerritoryRoom):
    """Match venues — where wrestling happens."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.room_type = "arena"
        self.db.capacity = 100  # crowd capacity
        self.db.current_event = ""  # name of current show if any


class GymRoom(TerritoryRoom):
    """Training rooms where players can use the `train` command."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.room_type = "gym"
        self.db.stat_bonus = ""  # which stat gets a bonus here (e.g. "tou" for The Pit)
        self.db.bonus_amount = 0  # extra training bonus

    def get_display_desc(self, looker, **kwargs):
        desc = super().get_display_desc(looker, **kwargs)
        bonus = self.db.stat_bonus
        if bonus:
            stat_names = {
                "str": "Strength", "agi": "Agility", "tec": "Technical",
                "cha": "Charisma", "tou": "Toughness", "psy": "Psychology",
            }
            name = stat_names.get(bonus, bonus.upper())
            desc = f"{desc}\n|yTraining bonus: {name} +{self.db.bonus_amount}|n"
        return desc


class BarRoom(TerritoryRoom):
    """Social rooms — bars, restaurants. Kayfabe events trigger here."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.room_type = "bar"


class TravelHub(TerritoryRoom):
    """Room that connects territories. Travel command works here."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.room_type = "travel"
        self.db.destinations = []  # list of territory_keys reachable


class LockerRoom(TerritoryRoom):
    """Backstage area for wrestlers."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.room_type = "locker"


class PromoterOffice(TerritoryRoom):
    """Promoter's office — booking, trust, negotiations."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.room_type = "office"
        self.db.promoter_name = ""


class UniqueRoom(TerritoryRoom):
    """Territory-specific special locations (Bourbon Street, The Dungeon, etc.)."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.room_type = "unique"
