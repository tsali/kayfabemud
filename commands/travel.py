"""
Kayfabe: Protect the Business — Travel command.

travel          — list available destinations
travel <place>  — travel to a destination
"""

import random
from evennia.commands.command import Command
from evennia.utils.search import search_tag


TERRITORY_DISPLAY = {
    "fhwa": ("FHWA", "Shepherdsville, KY", 1),
    "gccw": ("GCCW", "Pensacola, FL", 1),
    "gsg": ("GSG", "Vineland, NJ", 1),
    "bba": ("BBA", "Shreveport, LA", 1),
    "lsu": ("LSU", "Fort Worth, TX", 1),
    "psc": ("PSC", "Macon, GA", 1),
    "pensacola": ("Pensacola", "Pensacola, FL", 2),
    "slaughterhouse": ("Slaughterhouse", "North Andover, MA", 2),
    "beastworks": ("Beast Works", "Westville, NJ", 2),
    "conservatory": ("Conservatory", "Ocala, FL", 2),
    "dungeon": ("Dungeon of Holds", "Tampa, FL", 2),
    "proving_grounds": ("Proving Grounds", "Eldon, MO", 2),
    "memphis": ("Memphis CW", "Memphis, TN", 3),
    "midsouth": ("Mid-South", "Shreveport, LA", 3),
    "midatlantic": ("Mid-Atlantic", "Charlotte, NC", 3),
    "florida": ("Florida CWF", "Tampa, FL", 3),
    "georgia": ("Georgia CW", "Atlanta, GA", 3),
    "wccw": ("World Class", "Dallas, TX", 3),
    "awa": ("AWA", "Minneapolis, MN", 3),
    "stampede": ("Stampede", "Calgary, AB", 3),
    "pnw": ("Pacific NW", "Portland, OR", 3),
    "ovw": ("OVW", "Louisville, KY", 3.5),
    "fcw": ("FCW", "Tampa, FL", 3.5),
    "dsw": ("DSW", "McDonough, GA", 3.5),
    "hwa": ("HWA", "Cincinnati, OH", 3.5),
    "wwf": ("WWF", "New York, NY", 4),
    "wcw": ("WCW", "Atlanta, GA", 4),
    "ecw": ("ECW", "Philadelphia, PA", 4),
    "uk": ("UK", "London, UK", 4),
    "japan": ("Japan", "Tokyo, Japan", 4),
}

TRAVEL_COSTS = {
    1: 0,
    2: 0,
    3: 25,
    3.5: 30,
    4: 100,
}

TIER_NAMES = {1: "Backyard", 2: "Training", 3: "Regional", 3.5: "Developmental", 4: "National"}


class CmdTravel(Command):
    """
    Travel between territories.

    Usage:
      travel              — list available destinations
      travel <territory>  — travel to a territory

    Must be in a travel hub room. Travel costs money at higher tiers.
    Random fan encounters may happen during travel.
    """

    key = "travel"
    aliases = ["go", "drive"]
    locks = "cmd:all()"
    help_category = "Wrestling"

    def func(self):
        caller = self.caller
        if not caller.db.chargen_complete:
            caller.msg("Finish character creation first.")
            return

        if caller.scripts.get("match_script"):
            caller.msg("You're in a match. Can't leave.")
            return

        location = caller.location
        room_type = getattr(location.db, 'room_type', '')
        if room_type != "travel":
            caller.msg("You need to be at a travel point (road, highway, interchange) to travel.")
            return

        destinations = getattr(location.db, 'destinations', [])
        if not destinations:
            caller.msg("No destinations available from here.")
            return

        if not self.args:
            # List destinations
            caller.msg(f"\n|wAvailable destinations:|n")
            for dest_key in destinations:
                info = TERRITORY_DISPLAY.get(dest_key)
                if info:
                    name, loc, tier = info
                    tier_label = TIER_NAMES.get(tier, f"Tier {tier}")
                    cost = TRAVEL_COSTS.get(tier, 0)
                    cost_str = f"|y${cost}|n" if cost > 0 else "|gFree|n"
                    caller.msg(f"  |c{dest_key:15s}|n {name:20s} {loc:20s} ({tier_label}) {cost_str}")
                else:
                    caller.msg(f"  |c{dest_key}|n")
            caller.msg(f"\n|wUsage: travel <territory name>|n")
            return

        # Find destination
        target = self.args.strip().lower()

        # Match against available destinations
        matched = None
        for dest_key in destinations:
            if target == dest_key:
                matched = dest_key
                break
            info = TERRITORY_DISPLAY.get(dest_key)
            if info and target in info[0].lower():
                matched = dest_key
                break

        if not matched:
            caller.msg(f"'{target}' is not an available destination. Type |wtravel|n to see options.")
            return

        # Check travel cost
        info = TERRITORY_DISPLAY.get(matched, ("???", "???", 1))
        dest_tier = info[2]
        cost = TRAVEL_COSTS.get(dest_tier, 0)

        if cost > 0:
            if (caller.db.money or 0) < cost:
                caller.msg(f"You need ${cost} for travel. You have ${caller.db.money or 0}.")
                return
            caller.db.money -= cost
            caller.msg(f"|yYou pay ${cost} for travel.|n")

        # Find the start room for the destination
        start_rooms = search_tag(f"start_{matched}", category="chargen")
        if not start_rooms:
            # Fallback: any room tagged with the territory
            start_rooms = search_tag(matched, category="territory")

        if not start_rooms:
            caller.msg(f"That territory hasn't been built yet. Check back later.")
            return

        dest_room = start_rooms[0]

        # Travel narrative
        caller.msg(
            f"\n|w--- TRAVELING ---\n"
            f"You hit the road to {info[0]} ({info[1]})...|n\n"
        )

        # Random fan encounter during travel
        from world.rules import random_fan_encounter, kayfabe_change
        encounter = random_fan_encounter()
        if encounter:
            _handle_fan_encounter(caller, encounter)

        # Move the player
        caller.move_to(dest_room, quiet=True)
        caller.db.territory = matched
        caller.db.tier = dest_tier

        caller.msg(f"|gYou arrive at {info[0]}.|n\n")
        caller.execute_cmd("look")


def _handle_fan_encounter(caller, encounter):
    """
    Handle a random fan encounter during travel.
    For now, auto-resolve with a random choice weighted toward kayfabe protection.
    In the future this could be an EvMenu prompt.
    """
    caller.msg(f"\n|y--- FAN ENCOUNTER: {encounter['name']} ---|n")
    caller.msg(encounter['desc'])

    # Auto-resolve: pick the kayfabe-protecting choice most of the time
    alignment = caller.db.alignment or "Face"
    choices = encounter['choices']

    # Weight toward kayfabe-positive choices
    best = max(choices, key=lambda c: c.get('kayfabe', 0))
    chosen = best if random.random() < 0.7 else random.choice(choices)

    # Get message
    if alignment == "Face" and 'msg_face' in chosen:
        msg = chosen['msg_face']
    elif alignment == "Heel" and 'msg_heel' in chosen:
        msg = chosen['msg_heel']
    else:
        msg = chosen.get('msg', '')
        msg = msg.format(align_action="posing for the fans" if alignment == "Face" else "scowling menacingly")

    # Kayfabe change
    if alignment == "Face" and 'kayfabe_face' in chosen:
        delta = chosen['kayfabe_face']
    elif alignment == "Heel" and 'kayfabe_heel' in chosen:
        delta = chosen['kayfabe_heel']
    else:
        delta = chosen.get('kayfabe', 0)

    from world.rules import kayfabe_change
    actual = kayfabe_change(caller, delta)

    caller.msg(f"\n{msg}")
    if actual > 0:
        caller.msg(f"|gKayfabe +{actual}|n")
    elif actual < 0:
        caller.msg(f"|rKayfabe {actual}|n")
    caller.msg("")
