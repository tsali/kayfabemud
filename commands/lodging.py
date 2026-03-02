"""
Kayfabe: Protect the Business — Lodging commands.

rest — rest at inn/house, clear fatigue, apply stat bonus
board — read inn/house message board
post <message> — post to message board
buyhouse — purchase a house in current territory
gohome — teleport to owned house
upgrade — buy house upgrades
"""

import time
from evennia.commands.command import Command
from evennia.utils.create import create_object
from evennia.utils.search import search_tag
from commands.command import pause_then_look


# House purchase costs by territory tier
HOUSE_COSTS = {1: 500, 2: 1000, 3: 3000, 4: 15000}

# Rest bonuses by inn tier
INN_REST_BONUSES = {
    1: {},           # Roadside: clears fatigue only
    2: {"all": 1},   # Budget: +1 all stats
    3: {"all": 2},   # Mid-Range: +2 all stats
    4: {"all": 3},   # Luxury: +3 all stats
}

INN_REST_COSTS = {1: 10, 2: 25, 3: 75, 4: 200}


class CmdRest(Command):
    """
    Rest at an inn or your house.

    Usage:
      rest

    Clears all fatigue stacks. At an inn, costs money and may grant
    a temporary stat bonus. At your house, rest is free (upgrades
    can provide bonuses).
    """

    key = "rest"
    aliases = ["sleep", "checkin"]
    locks = "cmd:all()"
    help_category = "Lodging"

    def func(self):
        caller = self.caller
        if not caller.db.chargen_complete:
            caller.msg("Finish character creation first.")
            return

        from typeclasses.rooms import InnRoom, PlayerHouse

        loc = caller.location
        is_inn = isinstance(loc, InnRoom)
        is_house = isinstance(loc, PlayerHouse)

        if not is_inn and not is_house:
            caller.msg("You need to be at an inn or your house to rest.")
            return

        if is_inn:
            cost = loc.db.rest_cost or INN_REST_COSTS.get(loc.db.inn_tier, 10)
            money = caller.db.money or 0
            if money < cost:
                caller.msg(f"You can't afford the ${cost} room rate. You have ${money}.")
                return

            caller.db.money = money - cost

            # Apply rest bonus based on inn tier
            inn_tier = loc.db.inn_tier or 1
            bonus = loc.db.rest_bonus or INN_REST_BONUSES.get(inn_tier, {})

            caller.clear_fatigue()
            if bonus:
                caller.apply_rest_bonus(bonus, duration=43200)  # 12 hours

            caller.msg(
                f"\n|w--- REST ---\n"
                f"You check into the {loc.key} for ${cost}.|n\n"
            )
            if caller.db.fatigue_stacks == 0:
                caller.msg("|gAll fatigue cleared.|n")
            if bonus:
                all_b = bonus.get("all", 0)
                if all_b:
                    caller.msg(f"|g+{all_b} to all stats for 12 hours.|n")

            caller.msg(f"|yBalance: ${caller.db.money}|n")

        elif is_house:
            owner = loc.db.owner or ""
            allowed = loc.db.allowed_players or []
            if owner != caller.key and caller.key not in allowed:
                caller.msg("This isn't your house and you're not on the guest list.")
                return

            caller.clear_fatigue()

            # House rest bonus from upgrades
            upgrades = loc.db.upgrades or []
            bonus = {}
            if "hot_tub" in upgrades:
                bonus["all"] = bonus.get("all", 0) + 2
            if "party_deck" in upgrades:
                bonus["cha"] = bonus.get("cha", 0) + 1

            if bonus:
                caller.apply_rest_bonus(bonus, duration=43200)

            caller.msg(
                f"\n|w--- REST ---\n"
                f"You rest at home. No charge.|n\n"
                f"|gAll fatigue cleared.|n"
            )
            if bonus:
                parts = []
                if bonus.get("all"):
                    parts.append(f"+{bonus['all']} all stats")
                if bonus.get("cha"):
                    parts.append(f"+{bonus['cha']} CHA")
                caller.msg(f"|g{', '.join(parts)} for 12 hours.|n")


class CmdBoard(Command):
    """
    Read the message board at an inn or house.

    Usage:
      board
    """

    key = "board"
    aliases = ["messages", "readboard"]
    locks = "cmd:all()"
    help_category = "Lodging"

    def func(self):
        caller = self.caller
        from typeclasses.rooms import InnRoom, PlayerHouse

        loc = caller.location
        if not isinstance(loc, (InnRoom, PlayerHouse)):
            caller.msg("There's no message board here.")
            return

        messages = loc.db.messages or []
        if not messages:
            caller.msg("|wThe message board is empty.|n")
            return

        header = f"|w{'=' * 50}\n  MESSAGE BOARD — {loc.key}\n{'=' * 50}|n"
        caller.msg(header)
        for i, msg in enumerate(messages, 1):
            author = msg.get("author", "Anonymous")
            ts = msg.get("time", 0)
            text = msg.get("text", "")
            if ts:
                import datetime
                try:
                    from zoneinfo import ZoneInfo
                except ImportError:
                    from backports.zoneinfo import ZoneInfo
                dt = datetime.datetime.fromtimestamp(ts, tz=ZoneInfo("America/Chicago"))
                time_str = dt.strftime("%m/%d %I:%M%p")
            else:
                time_str = "???"
            caller.msg(f"  |c{i}.|n |w{author}|n ({time_str}): {text}")
        caller.msg(f"|w{'=' * 50}|n")
        pause_then_look(caller)


class CmdPost(Command):
    """
    Post a message to the inn/house message board.

    Usage:
      post <message>
    """

    key = "post"
    locks = "cmd:all()"
    help_category = "Lodging"

    def func(self):
        caller = self.caller
        if not caller.db.chargen_complete:
            caller.msg("Finish character creation first.")
            return

        from typeclasses.rooms import InnRoom, PlayerHouse

        loc = caller.location
        if not isinstance(loc, (InnRoom, PlayerHouse)):
            caller.msg("There's no message board here.")
            return

        if not self.args:
            caller.msg("Usage: post <message>")
            return

        text = self.args.strip()[:200]  # cap at 200 chars

        messages = loc.db.messages or []
        messages.append({
            "author": caller.key,
            "time": time.time(),
            "text": text,
        })

        # Rolling buffer: keep only last 20 messages
        if len(messages) > 20:
            messages = messages[-20:]

        loc.db.messages = messages
        caller.msg(f"|gMessage posted to the board.|n")
        # Announce to room
        caller.location.msg_contents(
            f"|w{caller.key}|n posts a message on the board.",
            exclude=[caller],
        )


class CmdBuyHouse(Command):
    """
    Purchase a house in the current territory.

    Usage:
      buyhouse

    House cost depends on territory tier:
      Tier 1: $500, Tier 2: $1000, Tier 3: $3000, Tier 4: $15000
    """

    key = "buyhouse"
    aliases = ["buy house", "purchasehouse"]
    locks = "cmd:all()"
    help_category = "Lodging"

    def func(self):
        caller = self.caller
        if not caller.db.chargen_complete:
            caller.msg("Finish character creation first.")
            return

        loc = caller.location
        territory_key = getattr(loc.db, 'territory_key', '') or ''
        territory_name = getattr(loc.db, 'territory_name', '') or ''

        if not territory_key:
            caller.msg("You're not in a territory where you can buy a house.")
            return

        tier = getattr(loc.db, 'tier', 1) or 1
        # Normalize tier for cost lookup
        cost_tier = int(tier) if tier != 3.5 else 3
        cost = HOUSE_COSTS.get(cost_tier, 500)

        # Check if already own a house in this territory
        owned = caller.db.owned_houses or []
        for house_id in owned:
            from evennia.objects.models import ObjectDB
            try:
                house = ObjectDB.objects.get(id=house_id)
                if house.db.territory_key == territory_key:
                    caller.msg(f"You already own a house in {territory_name}.")
                    return
            except ObjectDB.DoesNotExist:
                continue

        money = caller.db.money or 0
        if money < cost:
            caller.msg(f"A house here costs ${cost}. You have ${money}.")
            return

        # Create the house
        caller.db.money = money - cost

        house = create_object(
            "typeclasses.rooms.PlayerHouse",
            key=f"{caller.key}'s House",
            tags=[(territory_key, "territory"), ("player_house", "house")],
        )
        house.db.owner = caller.key
        house.db.territory_key = territory_key
        house.db.territory_name = territory_name
        house.db.desc = (
            f"A modest place in {territory_name}. It's not much, but it's yours. "
            f"The walls are bare and it could use some upgrades, but at least you "
            f"have somewhere to sleep that isn't a parking lot.\n\n"
            f"Type |wupgrade|n to see available improvements."
        )

        owned.append(house.id)
        caller.db.owned_houses = owned

        caller.msg(
            f"\n|w*** HOUSE PURCHASED ***|n\n"
            f"You bought a house in |c{territory_name}|n for |y${cost}|n.\n"
            f"Use |wgohome|n from anywhere to teleport there.\n"
            f"|yBalance: ${caller.db.money}|n"
        )


class CmdGoHome(Command):
    """
    Teleport to one of your owned houses.

    Usage:
      gohome
      gohome <territory>
    """

    key = "gohome"
    aliases = ["go home", "home"]
    locks = "cmd:all()"
    help_category = "Lodging"

    def func(self):
        caller = self.caller
        if not caller.db.chargen_complete:
            caller.msg("Finish character creation first.")
            return

        if caller.scripts.get("match_script"):
            caller.msg("You can't leave during a match.")
            return

        owned = caller.db.owned_houses or []
        if not owned:
            caller.msg("You don't own any houses. Use |wbuyhouse|n in a territory to purchase one.")
            return

        # Resolve valid houses
        from evennia.objects.models import ObjectDB
        valid_houses = []
        for house_id in owned:
            try:
                house = ObjectDB.objects.get(id=house_id)
                valid_houses.append(house)
            except ObjectDB.DoesNotExist:
                continue

        if not valid_houses:
            caller.msg("You don't own any houses (they may have been removed).")
            caller.db.owned_houses = []
            return

        target = self.args.strip().lower() if self.args else ""

        if len(valid_houses) == 1 and not target:
            house = valid_houses[0]
        elif target:
            house = None
            for h in valid_houses:
                terr = (h.db.territory_key or "").lower()
                terr_name = (h.db.territory_name or "").lower()
                if target in terr or target in terr_name:
                    house = h
                    break
            if not house:
                caller.msg(f"No house found matching '{target}'.")
                caller.msg("Your houses: " + ", ".join(
                    h.db.territory_name or h.db.territory_key for h in valid_houses
                ))
                return
        else:
            # Multiple houses, show list
            caller.msg("|wYour houses:|n")
            for h in valid_houses:
                terr = h.db.territory_name or h.db.territory_key
                caller.msg(f"  |c{terr}|n")
            caller.msg("Use |wgohome <territory>|n to choose.")
            return

        # Teleport
        old_loc = caller.location
        caller.msg(f"|wYou head home to {house.db.territory_name}...|n")
        if old_loc:
            old_loc.msg_contents(
                f"|w{caller.key} heads home.|n",
                exclude=[caller],
            )
        caller.move_to(house, quiet=True)
        caller.msg(caller.at_look(caller.location))


class CmdUpgrade(Command):
    """
    Buy upgrades for your house.

    Usage:
      upgrade              — list available upgrades
      upgrade <name>       — purchase an upgrade

    Available upgrades:
      home_gym      ($2,000) — Train stats at home (+2 bonus)
      practice_ring ($5,000) — Wrestle training dummies at home
      trophy_case   ($500)   — Display titles (flavor)
      hot_tub       ($1,500) — Rest bonus +2 all stats for 12h
      party_deck    ($3,000) — +1 CHA bonus for 12h (stacks with hot tub)
    """

    key = "upgrade"
    aliases = ["upgrades"]
    locks = "cmd:all()"
    help_category = "Lodging"

    def func(self):
        caller = self.caller
        if not caller.db.chargen_complete:
            caller.msg("Finish character creation first.")
            return

        from typeclasses.rooms import PlayerHouse

        loc = caller.location
        if not isinstance(loc, PlayerHouse):
            caller.msg("You need to be in your house to buy upgrades.")
            return

        if loc.db.owner != caller.key:
            caller.msg("This isn't your house.")
            return

        current_upgrades = loc.db.upgrades or []

        if not self.args:
            # Show available upgrades
            caller.msg("|w--- HOUSE UPGRADES ---|n")
            for key, cost in PlayerHouse.UPGRADE_COSTS.items():
                name = PlayerHouse.UPGRADE_NAMES.get(key, key)
                owned = "|g[OWNED]|n" if key in current_upgrades else f"|y${cost}|n"
                effects = {
                    "home_gym": "Train stats at home (+2 bonus)",
                    "practice_ring": "Wrestle training dummies at home",
                    "trophy_case": "Display titles (flavor)",
                    "hot_tub": "Rest bonus +2 all stats for 12h",
                    "party_deck": "+1 CHA bonus for 12h (stacks with hot tub)",
                }
                desc = effects.get(key, "")
                caller.msg(f"  |w{key:15s}|n {owned:20s} — {desc}")
            caller.msg(f"\n|wUsage:|n upgrade <name>")
            caller.msg(f"|yYour balance: ${caller.db.money or 0}|n")
            return

        upgrade_key = self.args.strip().lower()
        if upgrade_key not in PlayerHouse.UPGRADE_COSTS:
            caller.msg(f"Unknown upgrade '{upgrade_key}'. Type |wupgrade|n to see options.")
            return

        if upgrade_key in current_upgrades:
            caller.msg(f"You already have {PlayerHouse.UPGRADE_NAMES.get(upgrade_key, upgrade_key)}.")
            return

        cost = PlayerHouse.UPGRADE_COSTS[upgrade_key]
        money = caller.db.money or 0
        if money < cost:
            caller.msg(f"That costs ${cost}. You have ${money}.")
            return

        caller.db.money = money - cost
        current_upgrades.append(upgrade_key)
        loc.db.upgrades = current_upgrades

        name = PlayerHouse.UPGRADE_NAMES.get(upgrade_key, upgrade_key)

        # If home_gym, add gym room_type and stat_bonus attributes
        if upgrade_key == "home_gym":
            loc.db.room_type = "gym"
            loc.db.stat_bonus = ""  # no specific stat, but +2 generic
            loc.db.bonus_amount = 2

        caller.msg(
            f"\n|w*** UPGRADE INSTALLED ***|n\n"
            f"|g{name}|n has been added to your house.\n"
            f"|yBalance: ${caller.db.money}|n"
        )
