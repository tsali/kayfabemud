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

    def get_display_exits(self, looker, **kwargs):
        """Show exits with yellow direction names to stand out."""
        exits = self.filter_visible(
            self.contents_get(content_type="exit"), looker, **kwargs
        )
        if not exits:
            return ""
        parts = []
        for exi in exits:
            ename = exi.key
            dest = exi.destination
            if dest:
                parts.append(f"|lc{ename}|lt|y{ename}|n|le to |w{dest.key}|n")
            else:
                parts.append(f"|lc{ename}|lt|y{ename}|n|le")
        return "|wExits:|n " + ", ".join(parts)

    def get_display_characters(self, looker, **kwargs):
        """Group characters by type: Wrestlers, Managers, Trainers, etc."""
        from typeclasses.npcs import NPCWrestler, NPCManager, BackyardNPC
        from typeclasses.characters import Wrestler

        characters = self.filter_visible(
            self.contents_get(content_type="character"), looker, **kwargs
        )
        if not characters:
            return ""

        groups = {}
        for char in characters:
            if char == looker:
                continue
            if isinstance(char, NPCManager):
                label = "Managers"
            elif isinstance(char, (NPCWrestler, BackyardNPC)):
                role = getattr(char.db, "role", "wrestler") or "wrestler"
                if role == "trainer":
                    label = "Trainers"
                elif role == "announcer":
                    label = "Announcers"
                elif role == "authority":
                    label = "Promoters"
                else:
                    label = "Wrestlers"
            elif isinstance(char, Wrestler):
                label = "Players"
            else:
                label = "Others"
            groups.setdefault(label, []).append(char)

        parts = []
        order = ["Players", "Wrestlers", "Trainers", "Managers", "Announcers", "Promoters", "Others"]
        for label in order:
            chars = groups.get(label)
            if not chars:
                continue
            if label == "Wrestlers" and len(chars) > 5:
                # Summary mode for large groups
                levels = [getattr(c.db, 'level', 1) or 1 for c in chars]
                min_lv = min(levels)
                max_lv = max(levels)
                parts.append(f"|wWrestlers:|n {len(chars)} wrestlers (Lv {min_lv}-{max_lv})")
            else:
                names = []
                for char in chars:
                    name = char.get_display_name(looker, **kwargs)
                    lv = getattr(char.db, 'level', None)
                    if lv is not None and label in ("Wrestlers", "Trainers"):
                        name = f"{name} |xLv{lv}|n"
                    names.append(name)
                parts.append(f"|w{label}:|n {', '.join(names)}")

        return "\n".join(parts)


class ChargenRoom(Room):
    """Limbo room where new characters go through character creation."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.desc = (
            "You stand in darkness. The distant roar of a crowd echoes around "
            "you. A single spotlight cuts through the black, waiting for you "
            "to step into it.\n\n"
            "Your story is about to begin."
        )


class TerritoryRoom(Room):
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

    def _format_footer(self, looker, commands):
        """Format a footer with commands and the looker's objective."""
        from typeclasses.characters import Wrestler
        parts = []
        if commands:
            cmd_str = "  ".join(f"|y{c}|n" for c in commands)
            parts.append(f"|wCommands:|n {cmd_str}")
        if isinstance(looker, Wrestler) and looker.db.chargen_complete:
            if hasattr(looker, 'get_current_objective'):
                parts.append(f"|y>> NEXT:|n {looker.get_current_objective()}")
        return "\n".join(parts) if parts else ""


class BackyardFedRoom(TerritoryRoom):
    """Tier 1 small fed venues — VFW halls, backyards, fairgrounds."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.tier = 1
        self.db.room_type = "backyard"

    def get_display_footer(self, looker, **kwargs):
        return self._format_footer(looker, ["card", "wrestle <name>", "moves", "promo"])


class TrainingSchoolRoom(TerritoryRoom):
    """Tier 2 training school rooms."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.tier = 2
        self.db.room_type = "training"

    def get_display_footer(self, looker, **kwargs):
        return self._format_footer(looker, ["card", "wrestle <name>", "train <stat>", "learn"])


class ArenaRoom(TerritoryRoom):
    """Match venues — where wrestling happens."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.room_type = "arena"
        self.db.capacity = 100  # crowd capacity
        self.db.current_event = ""  # name of current show if any

    def get_display_footer(self, looker, **kwargs):
        return self._format_footer(looker, ["card", "wrestle <name>", "moves", "promo"])


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

    def get_display_footer(self, looker, **kwargs):
        return self._format_footer(looker, ["train <stat>", "learn", "stats"])


class BarRoom(TerritoryRoom):
    """Social rooms — bars, restaurants. Kayfabe events trigger here."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.room_type = "bar"

    def at_object_receive(self, moved_obj, source_location, **kwargs):
        """Trigger backstage segment on entry."""
        super().at_object_receive(moved_obj, source_location, **kwargs)
        self._try_backstage_segment(moved_obj)

    def _try_backstage_segment(self, character):
        from typeclasses.characters import Wrestler
        if not isinstance(character, Wrestler):
            return
        if not character.db.chargen_complete or not character.sessions.count():
            return

        from world.backstage import trigger_backstage_segment, format_segment_prompt
        segment = trigger_backstage_segment(character, "bar")
        if segment:
            character.ndb.pending_backstage = segment
            character.msg(format_segment_prompt(segment, character))

    def get_display_footer(self, looker, **kwargs):
        return self._format_footer(looker, ["promo", "who", "roster", "dirtsheet"])


class TravelHub(TerritoryRoom):
    """Room that connects territories. Travel command works here."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.room_type = "travel"
        self.db.destinations = []  # list of territory_keys reachable

    def get_display_footer(self, looker, **kwargs):
        return self._format_footer(looker, ["travel", "map", "balance"])


class LockerRoom(TerritoryRoom):
    """Backstage area for wrestlers."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.room_type = "locker"

    def at_object_receive(self, moved_obj, source_location, **kwargs):
        """Trigger backstage segment on entry."""
        super().at_object_receive(moved_obj, source_location, **kwargs)
        self._try_backstage_segment(moved_obj)

    def _try_backstage_segment(self, character):
        from typeclasses.characters import Wrestler
        if not isinstance(character, Wrestler):
            return
        if not character.db.chargen_complete or not character.sessions.count():
            return

        from world.backstage import trigger_backstage_segment, format_segment_prompt
        segment = trigger_backstage_segment(character, "locker")
        if segment:
            character.ndb.pending_backstage = segment
            character.msg(format_segment_prompt(segment, character))

    def get_display_footer(self, looker, **kwargs):
        return self._format_footer(looker, ["card", "stats", "rank", "contract"])


class PromoterOffice(TerritoryRoom):
    """Promoter's office — booking, trust, negotiations."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.room_type = "office"
        self.db.promoter_name = ""

    def get_display_footer(self, looker, **kwargs):
        return self._format_footer(looker, ["contract", "titleshot", "shows"])


class UniqueRoom(TerritoryRoom):
    """Territory-specific special locations (Bourbon Street, The Dungeon, etc.)."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.room_type = "unique"


class InnRoom(TerritoryRoom):
    """
    Lodging room where players can rest to clear fatigue and gain stat bonuses.

    Attributes:
        inn_tier (int): 1=Roadside, 2=Budget, 3=Mid-Range, 4=Luxury
        rest_cost (int): Dollar cost per rest
        rest_bonus (dict): Stat bonuses granted on rest (e.g. {"all": 2})
        messages (list): Territory-specific message board (up to 20 messages)
    """

    INN_TIER_NAMES = {
        1: "Roadside Motel",
        2: "Budget Motel",
        3: "Mid-Range Hotel",
        4: "Luxury Hotel",
    }

    def at_object_creation(self):
        super().at_object_creation()
        self.db.room_type = "inn"
        self.db.inn_tier = 1
        self.db.rest_cost = 10
        self.db.rest_bonus = {}  # e.g. {"all": 2} means +2 to all stats
        self.db.messages = []  # list of {"author": str, "time": float, "text": str}

    def get_display_desc(self, looker, **kwargs):
        desc = super().get_display_desc(looker, **kwargs)
        tier_name = self.INN_TIER_NAMES.get(self.db.inn_tier, "Lodging")
        cost = self.db.rest_cost or 0
        bonus = self.db.rest_bonus or {}
        bonus_str = ""
        if bonus.get("all"):
            bonus_str = f", +{bonus['all']} all stats for 12h"
        desc = (
            f"{desc}\n\n"
            f"|w[{tier_name}]|n — Rest cost: |y${cost}|n{bonus_str}\n"
            f"Type |wrest|n to check in. |wboard|n to read messages. |wpost <msg>|n to leave one."
        )
        return desc

    def get_display_footer(self, looker, **kwargs):
        return self._format_footer(looker, ["rest", "board", "post", "balance"])


class PlayerHouse(Room):
    """
    Player-owned house. Can be purchased in any territory.

    Attributes:
        owner (str): Character key of the owner
        territory_key (str): Territory where the house is located
        territory_name (str): Display name of the territory
        upgrades (list): List of upgrade keys owned
        allowed_players (list): Character keys allowed to use this house
        messages (list): Private message board (up to 20 messages)
    """

    UPGRADE_COSTS = {
        "home_gym": 2000,
        "practice_ring": 5000,
        "trophy_case": 500,
        "hot_tub": 1500,
        "party_deck": 3000,
    }

    UPGRADE_NAMES = {
        "home_gym": "Home Gym",
        "practice_ring": "Practice Ring",
        "trophy_case": "Trophy Case",
        "hot_tub": "Hot Tub",
        "party_deck": "Party Deck",
    }

    def at_object_creation(self):
        super().at_object_creation()
        self.db.owner = ""
        self.db.territory_key = ""
        self.db.territory_name = ""
        self.db.upgrades = []
        self.db.allowed_players = []
        self.db.messages = []

    def get_display_header(self, looker, **kwargs):
        owner = self.db.owner or "Nobody"
        territory = self.db.territory_name or "Unknown"
        return f"|w[{owner}'s House]|n |x({territory})|n"

    def get_display_desc(self, looker, **kwargs):
        desc = super().get_display_desc(looker, **kwargs)
        upgrades = self.db.upgrades or []
        if upgrades:
            names = [self.UPGRADE_NAMES.get(u, u) for u in upgrades]
            desc = f"{desc}\n\n|wUpgrades:|n {', '.join(names)}"
        desc = f"{desc}\n\nType |wrest|n to rest. |wupgrade|n to see available upgrades."
        return desc
