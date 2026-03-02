"""
Kayfabe: Protect the Business — Scheduled Shows/Events.

ShowSchedulerScript runs every 4 economy ticks (1 game month).
Generates a card per territory with 4-6 matches.
Players with contracts are booked automatically.
"""

import random
import time


# Show name templates per territory style
SHOW_NAMES = {
    # Tier 3 regional
    "memphis": ["Memphis Monday Night Wrestling", "Mid-South Coliseum Showdown",
                "Memphis TV Taping", "Saturday Morning Wrestling"],
    "midsouth": ["Mid-South Wrestling", "Superdome Saturday Night",
                 "Tuesday Night Grapplin'", "Mid-South TV Taping"],
    "midatlantic": ["NWA Mid-Atlantic Championship Wrestling", "World Wide Wrestling",
                    "Saturday Night at the Chase", "Mid-Atlantic Showcase"],
    "florida": ["Championship Wrestling from Florida", "Fort Homer Hesterly Armory Show",
                "Florida Heavyweight Showcase", "Sunshine State Smash"],
    "georgia": ["Georgia Championship Wrestling", "TBS Saturday Night",
                "Georgia TV Taping", "Omni Coliseum Spectacular"],
    "wccw": ["World Class Championship Wrestling", "WCCW Star Wars",
             "Cotton Bowl Extravaganza", "Fort Worth Stockyards Showdown"],
    "awa": ["AWA Championship Wrestling", "AWA All-Star Wrestling",
            "AWA Super Sunday", "Target Center Main Event"],
    "stampede": ["Stampede Wrestling", "Calgary Corral Carnage",
                 "Stampede TV Taping", "Alberta Main Event"],
    "pnw": ["Pacific Northwest Wrestling", "Portland Sports Arena Show",
            "PNW TV Taping", "Northwest Championship Night"],
    # Tier 3.5 developmental
    "ovw": ["OVW TV Taping", "OVW Saturday Night Special"],
    "fcw": ["FCW TV Taping", "FCW Showcase"],
    "dsw": ["DSW TV Taping", "DSW Championship Night"],
    "hwa": ["HWA TV Taping", "HWA Main Event"],
    # Tier 4 national
    "wwf": ["WWF Monday Night RAW", "WWF Superstars", "WWF Saturday Night's Main Event",
            "WWF Wrestling Challenge", "WWF Prime Time Wrestling"],
    "wcw": ["WCW Monday Nitro", "WCW Saturday Night", "WCW Thunder",
            "WCW Worldwide", "WCW Main Event"],
    "ecw": ["ECW Hardcore TV", "ECW on TNN", "ECW Arena Show",
            "ECW House of Hardcore"],
    "uk": ["World of Sport Wrestling", "Joint Promotions Spectacular",
           "Wembley Arena Show"],
    "japan": ["NJPW Strong Style", "NJPW World Tag League Night",
              "NJPW Road to the Tokyo Dome"],
}

# Default show names for territories without specific names
DEFAULT_SHOW_NAMES = [
    "Championship Wrestling", "Saturday Night Showdown",
    "Main Event", "Wrestling Spectacular",
]


def generate_show_card(territory_key, contracted_players=None, npcs=None):
    """
    Generate a show card for a territory.

    Args:
        territory_key: Territory key string
        contracted_players: List of player character objects with contracts here
        npcs: List of NPC wrestlers in this territory

    Returns:
        dict with show info: name, territory, matches (list of match dicts), timestamp
    """
    contracted_players = contracted_players or []
    npcs = npcs or []

    # Pick show name
    names = SHOW_NAMES.get(territory_key, DEFAULT_SHOW_NAMES)
    show_name = random.choice(names)

    # Generate 4-6 matches
    num_matches = random.randint(4, 6)
    matches = []
    used_players = set()
    used_npcs = set()

    # Book contracted players first
    for player in contracted_players:
        if len(matches) >= num_matches:
            break
        if player.key in used_players:
            continue

        # Find an NPC opponent
        available_npcs = [n for n in npcs if n.key not in used_npcs]
        if not available_npcs:
            break

        opponent = random.choice(available_npcs)
        used_players.add(player.key)
        used_npcs.add(opponent.key)

        matches.append({
            "wrestler_a": player.key,
            "wrestler_b": opponent.key,
            "is_player": True,
            "position": "midcard",  # Will be sorted later
        })

    # Fill remaining with NPC vs NPC
    available_npcs = [n for n in npcs if n.key not in used_npcs]
    while len(matches) < num_matches and len(available_npcs) >= 2:
        a = available_npcs.pop(random.randrange(len(available_npcs)))
        b = available_npcs.pop(random.randrange(len(available_npcs)))
        matches.append({
            "wrestler_a": a.key,
            "wrestler_b": b.key,
            "is_player": False,
            "position": "midcard",
        })

    # Assign card positions
    positions = ["opener", "midcard", "midcard", "semi_main", "main_event"]
    if len(matches) >= 6:
        positions = ["dark", "opener", "midcard", "midcard", "semi_main", "main_event"]
    for i, match in enumerate(matches):
        if i < len(positions):
            match["position"] = positions[i]

    return {
        "name": show_name,
        "territory": territory_key,
        "matches": matches,
        "timestamp": time.time(),
        "announced": False,
    }


def format_show_card(show):
    """Format a show card for display."""
    if not show:
        return "No upcoming shows."

    msg = (
        f"\n|w{'=' * 50}|n\n"
        f"|w  {show['name']}|n\n"
        f"|w  {show['territory'].upper()}|n\n"
        f"|w{'=' * 50}|n\n"
    )

    pos_colors = {
        "dark": "|x",
        "opener": "|w",
        "midcard": "|c",
        "semi_main": "|y",
        "main_event": "|Y",
    }

    for i, match in enumerate(show.get("matches", []), 1):
        pos = match.get("position", "midcard")
        color = pos_colors.get(pos, "|w")
        pos_label = pos.replace("_", " ").title()
        player_tag = " |g[YOU]|n" if match.get("is_player") else ""
        msg += (
            f"  {color}[{pos_label}]|n {match['wrestler_a']} vs {match['wrestler_b']}"
            f"{player_tag}\n"
        )

    msg += f"|w{'=' * 50}|n"
    return msg
