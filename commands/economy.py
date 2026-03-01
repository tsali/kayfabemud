"""
Kayfabe: Protect the Business — Economy commands.

Commands:
    balance - Show current funds and financial summary
    buy     - Purchase gear, equipment, or vehicles
    sidejob - Work a side job for extra cash (risk of missed shows)
"""

from evennia.commands.command import Command


# --- Gear / Equipment / Vehicle Tiers ---

GEAR_TIERS = {
    0: {"name": "Street Clothes", "desc": "Jean shorts and a t-shirt", "cha_bonus": 0, "cost": 0},
    1: {"name": "Basic Gear", "desc": "Trunks and custom boots", "cha_bonus": 1, "cost": 100},
    2: {"name": "Custom Gear", "desc": "Airbrushed tights and entrance jacket", "cha_bonus": 2, "cost": 500},
    3: {"name": "Premium Gear", "desc": "Full custom gear with logo and pyro entrance", "cha_bonus": 3, "cost": 2000},
    4: {"name": "Superstar Gear", "desc": "Iconic look — the crowd pops just seeing the outfit", "cha_bonus": 5, "cost": 8000},
}

EQUIPMENT_TIERS = {
    0: {"name": "Nothing", "desc": "You train at the gym only", "train_bonus": 0, "cost": 0},
    1: {"name": "Basic Home Gym", "desc": "Half-broken treadmill and some free weights", "train_bonus": 1, "cost": 150},
    2: {"name": "Decent Setup", "desc": "Proper weight set and a bench", "train_bonus": 2, "cost": 600},
    3: {"name": "Smart Gym", "desc": "Heart-rate tracking, resistance bands, the works", "train_bonus": 3, "cost": 2500},
    4: {"name": "Full Home Gym", "desc": "Pro-level setup rivaling any territory gym", "train_bonus": 4, "cost": 10000},
}

VEHICLE_TIERS = {
    0: {"name": "Hitchhiking", "desc": "You bum rides and take the bus", "travel_discount": 0, "cost": 0},
    1: {"name": "Junker Car", "desc": "Rusty sedan that barely runs", "travel_discount": 10, "cost": 200},
    2: {"name": "Reliable Sedan", "desc": "Gets you there without breaking down", "travel_discount": 25, "cost": 1000},
    3: {"name": "Van", "desc": "Carry all your gear, sleep in the back", "travel_discount": 40, "cost": 4000},
    4: {"name": "Tour Bus", "desc": "You've made it — travel in style", "travel_discount": 60, "cost": 15000},
}

SIDE_JOBS = {
    "security": {
        "name": "Bar Security",
        "desc": "Bounce at a local bar",
        "pay": (20, 40),
        "stat_gain": "tou",
        "conflict_chance": 0.15,
    },
    "food": {
        "name": "Fast Food",
        "desc": "Work a diner shift",
        "pay": (10, 25),
        "stat_gain": None,
        "conflict_chance": 0.10,
    },
    "gym": {
        "name": "Personal Trainer",
        "desc": "Train normies at the local gym",
        "pay": (25, 45),
        "stat_gain": "str",
        "conflict_chance": 0.15,
    },
    "moving": {
        "name": "Moving Crew",
        "desc": "Haul furniture for a moving company",
        "pay": (30, 55),
        "stat_gain": "tou",
        "conflict_chance": 0.20,
    },
}


class CmdBalance(Command):
    """
    Check your financial status.

    Usage:
        balance

    Shows your current money, gear tier, equipment, vehicle,
    and manager expenses.
    """
    key = "balance"
    aliases = ["money", "wallet", "funds"]
    locks = "cmd:all()"
    help_category = "Economy"

    def func(self):
        caller = self.caller
        money = caller.db.money or 0
        gear = GEAR_TIERS.get(caller.db.gear_tier or 0, GEAR_TIERS[0])
        equip = EQUIPMENT_TIERS.get(caller.db.equipment_tier or 0, EQUIPMENT_TIERS[0])
        vehicle = VEHICLE_TIERS.get(caller.db.vehicle_tier or 0, VEHICLE_TIERS[0])

        msg = (
            f"\n|w{'=' * 44}|n\n"
            f"|w  FINANCIAL STATUS|n\n"
            f"|w{'=' * 44}|n\n"
            f"  |yCash:|n ${money}\n"
            f"\n  |wGear:|n {gear['name']}\n"
            f"    {gear['desc']}\n"
            f"    CHA bonus: +{gear['cha_bonus']}\n"
            f"\n  |wHome Gym:|n {equip['name']}\n"
            f"    {equip['desc']}\n"
            f"    Train bonus: +{equip['train_bonus']}\n"
            f"\n  |wVehicle:|n {vehicle['name']}\n"
            f"    {vehicle['desc']}\n"
            f"    Travel discount: {vehicle['travel_discount']}%\n"
        )

        # Manager costs
        if caller.db.manager:
            from evennia.utils.search import search_tag
            managers = search_tag("npc_manager", category="npc_type")
            mgr = None
            for m in managers:
                if m.key == caller.db.manager:
                    mgr = m
                    break
            if mgr:
                retainer = mgr.db.retainer_cost or 100
                cut = mgr.db.cut_percent or 20
                msg += (
                    f"\n  |wManager:|n {mgr.key}\n"
                    f"    Retainer: |r${retainer}/week|n\n"
                    f"    Cut: |r{cut}% of match pay|n\n"
                )

        msg += f"|w{'=' * 44}|n"
        caller.msg(msg)


class CmdBuy(Command):
    """
    Purchase upgrades for your wrestling career.

    Usage:
        buy gear
        buy equipment
        buy vehicle
        buy <category> <tier>

    Categories:
        gear      - Ring gear (CHA bonus during matches)
        equipment - Home gym equipment (training bonus)
        vehicle   - Vehicle (travel cost reduction)

    Without a tier number, shows available options.
    With a tier number (1-4), purchases that tier.
    """
    key = "buy"
    aliases = ["purchase", "shop"]
    locks = "cmd:all()"
    help_category = "Economy"

    def func(self):
        caller = self.caller
        args = self.args.strip().split()

        if not args:
            caller.msg(
                "|wUsage:|n buy <gear|equipment|vehicle> [tier]\n"
                "  buy gear       - Show gear options\n"
                "  buy gear 2     - Buy tier 2 gear\n"
                "  buy equipment  - Show home gym options\n"
                "  buy vehicle    - Show vehicle options"
            )
            return

        category = args[0].lower()
        tier = None
        if len(args) > 1:
            try:
                tier = int(args[1])
            except ValueError:
                caller.msg("|rTier must be a number (1-4).|n")
                return

        if category in ("gear", "g"):
            self._handle_buy(caller, "gear", GEAR_TIERS, "gear_tier", "cha_bonus", tier)
        elif category in ("equipment", "equip", "eq", "gym"):
            self._handle_buy(caller, "equipment", EQUIPMENT_TIERS, "equipment_tier", "train_bonus", tier)
        elif category in ("vehicle", "car", "ride"):
            self._handle_buy(caller, "vehicle", VEHICLE_TIERS, "vehicle_tier", "travel_discount", tier)
        else:
            caller.msg("|rUnknown category. Try: gear, equipment, vehicle|n")

    def _handle_buy(self, caller, category_name, tiers, attr_name, bonus_key, tier):
        current = getattr(caller.db, attr_name, 0) or 0
        money = caller.db.money or 0

        if tier is None:
            # Show options
            msg = f"\n|w{'=' * 44}|n\n"
            msg += f"|w  {category_name.upper()} SHOP|n\n"
            msg += f"|w{'=' * 44}|n\n"
            msg += f"  Current: |c{tiers[current]['name']}|n (tier {current})\n"
            msg += f"  Cash: |y${money}|n\n\n"

            for t in range(1, len(tiers)):
                info = tiers[t]
                owned = " |g[OWNED]|n" if t <= current else ""
                affordable = " |y[Can afford]|n" if t > current and money >= info["cost"] else ""
                msg += (
                    f"  |wTier {t}:|n {info['name']}{owned}{affordable}\n"
                    f"    {info['desc']}\n"
                    f"    {bonus_key.replace('_', ' ').title()}: +{info[bonus_key]}  |  Cost: ${info['cost']}\n\n"
                )

            msg += f"|w{'=' * 44}|n"
            caller.msg(msg)
            return

        # Attempt purchase
        if tier < 1 or tier >= len(tiers):
            caller.msg(f"|rTier must be between 1 and {len(tiers) - 1}.|n")
            return

        if tier <= current:
            caller.msg(f"|rYou already own tier {tier} {category_name} or better.|n")
            return

        if tier > current + 1:
            caller.msg(f"|rYou must buy tiers in order. Next tier: {current + 1}.|n")
            return

        info = tiers[tier]
        cost = info["cost"]

        if money < cost:
            caller.msg(f"|rNot enough money. Need ${cost}, have ${money}.|n")
            return

        caller.db.money = money - cost
        setattr(caller.db, attr_name, tier)
        caller.msg(
            f"|gPurchased |w{info['name']}|g for ${cost}!|n\n"
            f"  {info['desc']}\n"
            f"  {bonus_key.replace('_', ' ').title()}: +{info[bonus_key]}"
        )


class CmdSideJob(Command):
    """
    Work a side job for extra cash.

    Usage:
        sidejob
        sidejob <type>

    Available jobs:
        security - Bar bouncer (decent pay, +TOU risk of conflict)
        food     - Fast food shift (low pay, safe)
        gym      - Personal trainer (moderate pay, +STR)
        moving   - Moving crew (good pay, +TOU, higher conflict risk)

    Warning: Side jobs risk conflicting with training or card spots.
    Missing a show tanks your promoter trust.
    """
    key = "sidejob"
    aliases = ["side", "hustle"]
    locks = "cmd:all()"
    help_category = "Economy"

    def func(self):
        import random
        caller = self.caller
        args = self.args.strip().lower()

        if not args:
            msg = (
                "\n|w{'=' * 44}|n\n"
                "|w  SIDE JOBS|n\n"
                "|w{'=' * 44}|n\n"
            )
            msg = f"\n|w{'=' * 44}|n\n|w  SIDE JOBS|n\n|w{'=' * 44}|n\n"
            for key, job in SIDE_JOBS.items():
                pay_lo, pay_hi = job["pay"]
                stat = f"+{job['stat_gain'].upper()}" if job["stat_gain"] else "None"
                risk = f"{int(job['conflict_chance'] * 100)}%"
                msg += (
                    f"  |w{key:10s}|n - {job['name']}\n"
                    f"    {job['desc']}\n"
                    f"    Pay: ${pay_lo}-${pay_hi} | Stat: {stat} | Conflict risk: {risk}\n\n"
                )
            msg += f"Usage: |wsidejob <type>|n\n|w{'=' * 44}|n"
            caller.msg(msg)
            return

        if args not in SIDE_JOBS:
            caller.msg(f"|rUnknown job. Try: {', '.join(SIDE_JOBS.keys())}|n")
            return

        job = SIDE_JOBS[args]
        pay_lo, pay_hi = job["pay"]
        pay = random.randint(pay_lo, pay_hi)

        # Check for scheduling conflict
        conflict = random.random() < job["conflict_chance"]

        if conflict:
            # Determine what was missed
            conflict_types = [
                ("training session", "You missed a training session at the gym."),
                ("card spot", "The promoter had a spot for you on tonight's card. You were a no-show."),
                ("scouting opportunity", "A scout from a bigger territory was watching tonight's show. You weren't there."),
            ]
            c_type, c_msg = random.choice(conflict_types)

            # Trust penalty for missed card
            territory = caller.db.territory or ""
            if c_type == "card spot" and territory:
                trust = caller.db.promoter_trust or {}
                current_trust = trust.get(territory, 50)
                trust[territory] = max(0, current_trust - 10)
                caller.db.promoter_trust = trust
                c_msg += f" |r(Promoter trust -{10} in {territory})|n"

            caller.db.money = (caller.db.money or 0) + pay

            caller.msg(
                f"\n|yYou worked a shift at |w{job['name']}|y and earned |g${pay}|y.|n\n"
                f"|rBut there was a scheduling conflict!|n\n"
                f"  {c_msg}\n"
            )
        else:
            caller.db.money = (caller.db.money or 0) + pay
            caller.msg(
                f"\n|gYou worked a shift at |w{job['name']}|g and earned |y${pay}|g.|n\n"
                f"No conflicts — you made it to the arena on time.\n"
            )

        # Possible stat gain
        if job["stat_gain"]:
            if random.random() < 0.3:  # 30% chance of minor stat gain
                from world.rules import training_gain
                gained, amount, msg = training_gain(caller, job["stat_gain"])
                if gained:
                    stat_name = job["stat_gain"].upper()
                    caller.msg(f"|cSide benefit: The physical work paid off. (+{amount:.1f} {stat_name})|n")
