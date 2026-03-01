"""
Kayfabe: Protect the Business — Character Creation (EvMenu).

Launched automatically on first puppet via Wrestler.at_post_puppet().
Flow: Welcome → Ring Name → Real Name → Hometown → Style → Stat Allocation →
      Alignment → Starting Fed → Finisher → Confirm → Done
"""

from evennia.utils.evmenu import EvMenu
from typeclasses.characters import WRESTLING_STYLES, ALIGNMENTS

# Starting small feds data
STARTING_FEDS = {
    "fhwa": {
        "name": "Federal Hills Wrestling Association",
        "abbrev": "FHWA",
        "location": "Shepherdsville, KY",
        "nearest_school": "OVW (Louisville)",
        "nearest_territory": "Mid-South",
        "pros": "Fast track to OVW developmental; TV exposure nearby",
        "cons": "Cornette-style gatekeepers, very competitive",
    },
    "gccw": {
        "name": "Gulf Coast Championship Wrestling",
        "abbrev": "GCCW",
        "location": "Pensacola, FL",
        "nearest_school": "Samoan Training Grounds (Pensacola)",
        "nearest_territory": "Florida",
        "pros": "World-class training from the Saveas; toughness focus",
        "cons": "Remote, fewer big scouts pass through",
    },
    "gsg": {
        "name": "Garden State Grappling",
        "abbrev": "GSG",
        "location": "Vineland, NJ",
        "nearest_school": "The Beast Works",
        "nearest_territory": "WWF (NYC)",
        "pros": "Closest pipeline to the biggest national promotion",
        "cons": "Expensive area, cutthroat competition",
    },
    "bba": {
        "name": "Bayou Brawling Alliance",
        "abbrev": "BBA",
        "location": "Shreveport, LA",
        "nearest_school": "The Proving Grounds (MO)",
        "nearest_territory": "Mid-South",
        "pros": "Stiff, hard-hitting style gets you noticed fast",
        "cons": "Brutal conditions, injuries more likely",
    },
    "lsu": {
        "name": "Lone Star Underground",
        "abbrev": "LSU",
        "location": "Fort Worth, TX",
        "nearest_school": "None (learn on the job)",
        "nearest_territory": "World Class (Dallas)",
        "pros": "Direct territory access, no school needed if spotted",
        "cons": "Sink or swim, no safety net",
    },
    "psc": {
        "name": "Peach State Championship",
        "abbrev": "PSC",
        "location": "Macon, GA",
        "nearest_school": "The Conservatory (Ocala)",
        "nearest_territory": "Georgia (TBS)",
        "pros": "National TV territory nearby, CHA-focused",
        "cons": "Need the look and the talk, not just the work",
    },
}

STAT_NAMES = {
    "str": "Strength",
    "agi": "Agility",
    "tec": "Technical",
    "cha": "Charisma",
    "tou": "Toughness",
    "psy": "Psychology",
}


def _format_stat_bar(value, max_val=15):
    """Simple ASCII bar for stat display."""
    filled = int(value)
    empty = max_val - filled
    return f"|w{'#' * filled}|x{'.' * empty}|n {value}/{max_val}"


# --- EvMenu Nodes ---

def node_welcome(caller, raw_string, **kwargs):
    """Welcome screen."""
    text = (
        "\n|w========================================|n\n"
        "|w    KAYFABE: PROTECT THE BUSINESS|n\n"
        "|w========================================|n\n\n"
        "Welcome to the world of professional wrestling.\n\n"
        "You're about to create your wrestler — a nobody from nowhere\n"
        "with a dream of making it to the big time. You'll start in a\n"
        "backyard fed, working for hot dogs and handshakes, and if you're\n"
        "good enough (and smart enough to protect the business), you might\n"
        "just make it to Madison Square Garden.\n\n"
        "Let's build your character.\n"
    )
    options = ({"desc": "Begin character creation", "goto": "node_ring_name"},)
    return text, options


def node_ring_name(caller, raw_string, **kwargs):
    """Choose ring name."""
    text = (
        "\n|wRING NAME|n\n"
        "----------\n"
        "What's your ring name? This is what the crowd will chant,\n"
        "what the announcer will call, and what'll be on your tights.\n\n"
        "Enter your ring name:"
    )
    options = {"key": "_default", "goto": _set_ring_name}
    return text, options


def _set_ring_name(caller, raw_string, **kwargs):
    """Process ring name input."""
    name = raw_string.strip()
    if not name or len(name) < 2:
        caller.msg("|rName must be at least 2 characters.|n")
        return "node_ring_name"
    if len(name) > 30:
        caller.msg("|rName must be 30 characters or less.|n")
        return "node_ring_name"
    caller.ndb._menutree.ring_name = name
    return "node_real_name"


def node_real_name(caller, raw_string, **kwargs):
    """Choose real/shoot name."""
    text = (
        f"\n|wREAL NAME|n\n"
        f"----------\n"
        f"Ring name: |c{caller.ndb._menutree.ring_name}|n\n\n"
        f"What's your shoot name? The name on your driver's license.\n"
        f"The boys in the back will know you by this.\n\n"
        f"Enter your real name:"
    )
    options = {"key": "_default", "goto": _set_real_name}
    return text, options


def _set_real_name(caller, raw_string, **kwargs):
    name = raw_string.strip()
    if not name or len(name) < 2:
        caller.msg("|rName must be at least 2 characters.|n")
        return "node_real_name"
    if len(name) > 40:
        caller.msg("|rName must be 40 characters or less.|n")
        return "node_real_name"
    caller.ndb._menutree.real_name = name
    return "node_hometown"


def node_hometown(caller, raw_string, **kwargs):
    """Choose hometown."""
    text = (
        f"\n|wHOMETOWN|n\n"
        f"---------\n"
        f"Ring name: |c{caller.ndb._menutree.ring_name}|n\n"
        f"Real name: |c{caller.ndb._menutree.real_name}|n\n\n"
        f"Where are you from? The announcer needs to know.\n"
        f"\"Hailing from...\"\n\n"
        f"Enter your hometown (city, state/country):"
    )
    options = {"key": "_default", "goto": _set_hometown}
    return text, options


def _set_hometown(caller, raw_string, **kwargs):
    town = raw_string.strip()
    if not town or len(town) < 2:
        caller.msg("|rHometown must be at least 2 characters.|n")
        return "node_hometown"
    caller.ndb._menutree.hometown = town
    return "node_gender"


# Gender options and their division rules
GENDER_OPTIONS = {
    "Male": {
        "division": "Men's Division",
        "desc": "Compete primarily for men's championships.",
        "flavor": "jacked physique",
    },
    "Female": {
        "division": "Women's Division",
        "desc": "Compete primarily for women's championships.",
        "flavor": "show-stopping attire",
    },
    "Non-Binary": {
        "division": "Open Division",
        "desc": "Booked 50/50 across both divisions, wherever the card needs you.",
        "flavor": "unique presence",
    },
    "Undisclosed": {
        "division": "Open Division",
        "desc": "Same rules as Non-Binary. Your wrestling does the talking.",
        "flavor": "enigmatic aura",
    },
}


def node_gender(caller, raw_string, **kwargs):
    """Choose gender / division."""
    text = (
        "\n|wGENDER / DIVISION|n\n"
        "------------------\n"
        "In the territories, divisions exist — but talent crosses all lines.\n"
        "Anyone can fight anyone. This determines where promoters slot you\n"
        "on most cards.\n\n"
        "  |w1|n. |cMale|n — Men's division booking. Compete primarily for\n"
        "     men's championships. Gear bonuses: \"jacked physique\" flavor.\n\n"
        "  |w2|n. |cFemale|n — Women's division booking. Compete primarily for\n"
        "     women's championships. Gear bonuses: \"show-stopping attire\" flavor.\n\n"
        "  |w3|n. |cNon-Binary|n — Booked 50/50 across both divisions, wherever\n"
        "     the card needs you. Compete for any championship.\n"
        "     Gear bonuses: \"unique presence\" flavor.\n\n"
        "  |w4|n. |cUndisclosed|n — Same rules as Non-Binary. Your wrestling\n"
        "     does the talking.\n\n"
        "Choose (1-4):"
    )
    options = (
        {"key": "1", "desc": "Male", "goto": (_set_gender, {"gender": "Male"})},
        {"key": "2", "desc": "Female", "goto": (_set_gender, {"gender": "Female"})},
        {"key": "3", "desc": "Non-Binary", "goto": (_set_gender, {"gender": "Non-Binary"})},
        {"key": "4", "desc": "Undisclosed", "goto": (_set_gender, {"gender": "Undisclosed"})},
    )
    return text, options


def _set_gender(caller, raw_string, gender="Undisclosed", **kwargs):
    caller.ndb._menutree.gender = gender
    return "node_style"


def node_style(caller, raw_string, **kwargs):
    """Choose wrestling style."""
    text = (
        "\n|wWRESTLING STYLE|n\n"
        "----------------\n"
        "Your style defines how you work in the ring and gives\n"
        "starting stat bonuses.\n\n"
    )
    for i, (style, bonuses) in enumerate(WRESTLING_STYLES.items(), 1):
        bonus_parts = []
        for stat, val in bonuses.items():
            if val > 0:
                bonus_parts.append(f"{STAT_NAMES[stat]} +{val}")
        bonus_str = ", ".join(bonus_parts)
        text += f"  |w{i}|n. |c{style}|n — {bonus_str}\n"

    text += "\nChoose your style (1-5):"

    options = []
    for i, style_name in enumerate(WRESTLING_STYLES.keys(), 1):
        options.append({
            "key": str(i),
            "desc": style_name,
            "goto": (_set_style, {"style": style_name}),
        })
    return text, options


def _set_style(caller, raw_string, style="All-Rounder", **kwargs):
    caller.ndb._menutree.style = style
    return "node_stats"


def node_stats(caller, raw_string, **kwargs):
    """Allocate 30 bonus points across stats."""
    menu = caller.ndb._menutree
    style = menu.style

    # Initialize allocation if not set
    if not hasattr(menu, "stat_alloc"):
        menu.stat_alloc = {"str": 0, "agi": 0, "tec": 0, "cha": 0, "tou": 0, "psy": 0}
        menu.points_remaining = 30

    style_bonuses = WRESTLING_STYLES.get(style, {})

    text = (
        f"\n|wSTAT ALLOCATION|n\n"
        f"----------------\n"
        f"Style: |c{style}|n\n"
        f"Points remaining: |w{menu.points_remaining}|n\n\n"
        f"All stats start at 5. Style bonuses and your allocated points\n"
        f"are added on top. Max 15 per stat at creation.\n\n"
    )

    stat_order = ["str", "agi", "tec", "cha", "tou", "psy"]
    for key in stat_order:
        base = 5
        style_bonus = style_bonuses.get(key, 0)
        allocated = menu.stat_alloc.get(key, 0)
        total = base + style_bonus + allocated
        parts = f"  Base 5"
        if style_bonus:
            parts += f" + |c{style_bonus}|n style"
        if allocated:
            parts += f" + |w{allocated}|n alloc"
        text += f"  |w{STAT_NAMES[key]:12s}|n {_format_stat_bar(total)} ({parts})\n"

    text += (
        f"\nTo allocate points, type: |w<stat> <points>|n\n"
        f"  Example: |wstr 5|n — adds 5 to Strength\n"
        f"  Type |wrandom|n to let fate decide your stats.\n"
        f"  Type |wreset|n to start over, |wdone|n when finished.\n"
    )

    options = {"key": "_default", "goto": _process_stat_input}
    return text, options


def _random_stat_allocation(style):
    """Distribute 30 points randomly across 6 stats, respecting cap 15 per stat at creation."""
    import random as _rand
    style_bonuses = WRESTLING_STYLES.get(style, {})
    alloc = {"str": 0, "agi": 0, "tec": 0, "cha": 0, "tou": 0, "psy": 0}
    remaining = 30
    stat_keys = list(alloc.keys())

    while remaining > 0:
        _rand.shuffle(stat_keys)
        distributed_any = False
        for key in stat_keys:
            if remaining <= 0:
                break
            current_total = 5 + style_bonuses.get(key, 0) + alloc[key]
            cap_room = 15 - current_total
            if cap_room <= 0:
                continue
            # Give 1-5 points (or whatever fits)
            give = min(_rand.randint(1, 5), cap_room, remaining)
            alloc[key] += give
            remaining -= give
            distributed_any = True
        if not distributed_any:
            break  # all stats capped

    return alloc, remaining


def _process_stat_input(caller, raw_string, **kwargs):
    menu = caller.ndb._menutree
    inp = raw_string.strip().lower()

    if inp == "done":
        if menu.points_remaining > 0:
            caller.msg(f"|rYou still have {menu.points_remaining} points to allocate.|n")
            return "node_stats"
        return "node_alignment"

    if inp == "random":
        alloc, leftover = _random_stat_allocation(menu.style)
        menu.stat_alloc = alloc
        menu.points_remaining = leftover
        style_bonuses = WRESTLING_STYLES.get(menu.style, {})
        caller.msg("|yFate has spoken! Here's what you got:|n")
        for key in ["str", "agi", "tec", "cha", "tou", "psy"]:
            total = 5 + style_bonuses.get(key, 0) + alloc[key]
            caller.msg(f"  {STAT_NAMES[key]:12s} {total}")
        caller.msg("|wType |yrandom|w to re-roll, |yreset|w to go manual, or |ydone|w to accept.|n")
        return "node_stats"

    if inp == "reset":
        menu.stat_alloc = {"str": 0, "agi": 0, "tec": 0, "cha": 0, "tou": 0, "psy": 0}
        menu.points_remaining = 30
        caller.msg("|yPoints reset.|n")
        return "node_stats"

    parts = inp.split()
    if len(parts) != 2:
        caller.msg("|rFormat: <stat> <points>  (e.g. str 5)|n")
        return "node_stats"

    stat_key = parts[0][:3]
    # Allow full names
    name_to_key = {
        "str": "str", "strength": "str",
        "agi": "agi", "agility": "agi",
        "tec": "tec", "technical": "tec", "tech": "tec",
        "cha": "cha", "charisma": "cha",
        "tou": "tou", "toughness": "tou", "tough": "tou",
        "psy": "psy", "psychology": "psy", "psych": "psy",
    }
    stat_key = name_to_key.get(parts[0], stat_key)

    if stat_key not in ("str", "agi", "tec", "cha", "tou", "psy"):
        caller.msg("|rValid stats: str, agi, tec, cha, tou, psy|n")
        return "node_stats"

    try:
        points = int(parts[1])
    except ValueError:
        caller.msg("|rPoints must be a number.|n")
        return "node_stats"

    if points < 0:
        caller.msg("|rPoints must be positive. Use 'reset' to start over.|n")
        return "node_stats"

    if points > menu.points_remaining:
        caller.msg(f"|rYou only have {menu.points_remaining} points left.|n")
        return "node_stats"

    style_bonuses = WRESTLING_STYLES.get(menu.style, {})
    current_total = 5 + style_bonuses.get(stat_key, 0) + menu.stat_alloc.get(stat_key, 0) + points
    if current_total > 15:
        max_add = 15 - (5 + style_bonuses.get(stat_key, 0) + menu.stat_alloc.get(stat_key, 0))
        caller.msg(f"|rThat would exceed 15. You can add at most {max(0, max_add)} more to {STAT_NAMES[stat_key]}.|n")
        return "node_stats"

    menu.stat_alloc[stat_key] += points
    menu.points_remaining -= points
    caller.msg(f"|g+{points} to {STAT_NAMES[stat_key]}.|n")
    return "node_stats"


def node_alignment(caller, raw_string, **kwargs):
    """Choose Face or Heel."""
    text = (
        "\n|wALIGNMENT|n\n"
        "----------\n"
        "Are you a hero or a villain?\n\n"
        "  |w1|n. |gFace|n (Babyface)\n"
        "     The good guy. Crowd cheers you. You sell, make the comeback,\n"
        "     win clean. Higher merch sales, fan loyalty. Restricted from\n"
        "     dirty tactics.\n\n"
        "  |w2|n. |rHeel|n\n"
        "     The villain. Crowd boos you (that's the point). You cheat,\n"
        "     talk trash, get heat. More creative freedom, can use foreign\n"
        "     objects. Less merch but better feuds.\n\n"
        "|x(Anti-Hero unlocks later at Midcarder rank.)|n\n\n"
        "Choose (1 or 2):"
    )
    options = (
        {"key": "1", "desc": "Face", "goto": (_set_alignment, {"align": "Face"})},
        {"key": "2", "desc": "Heel", "goto": (_set_alignment, {"align": "Heel"})},
    )
    return text, options


def _set_alignment(caller, raw_string, align="Face", **kwargs):
    caller.ndb._menutree.alignment = align
    return "node_starting_fed"


def node_starting_fed(caller, raw_string, **kwargs):
    """Choose starting backyard fed."""
    text = (
        "\n|wSTARTING FED|n\n"
        "-------------\n"
        "Every legend started somewhere. Pick your backyard fed.\n"
        "This is the most important early-game choice — it determines\n"
        "your pipeline to the big time.\n\n"
    )

    fed_keys = list(STARTING_FEDS.keys())
    for i, key in enumerate(fed_keys, 1):
        fed = STARTING_FEDS[key]
        text += (
            f"  |w{i}|n. |c{fed['abbrev']}|n — {fed['name']}\n"
            f"     Location: {fed['location']}\n"
            f"     Nearest school: {fed['nearest_school']}\n"
            f"     Nearest territory: {fed['nearest_territory']}\n"
            f"     |gPros|n: {fed['pros']}\n"
            f"     |rCons|n: {fed['cons']}\n\n"
        )

    text += "Choose your starting fed (1-6):"

    options = []
    for i, key in enumerate(fed_keys, 1):
        options.append({
            "key": str(i),
            "desc": STARTING_FEDS[key]["abbrev"],
            "goto": (_set_starting_fed, {"fed_key": key}),
        })
    return text, options


def _set_starting_fed(caller, raw_string, fed_key="fhwa", **kwargs):
    caller.ndb._menutree.starting_fed = fed_key
    return "node_finisher"


def node_finisher(caller, raw_string, **kwargs):
    """Name your finishing move."""
    text = (
        "\n|wFINISHING MOVE|n\n"
        "---------------\n"
        "Every wrestler needs a finisher — the move that puts them away.\n"
        "What's yours called?\n\n"
        "Examples: The Devastator, Gulf Coast Slam, Lone Star Lariat,\n"
        "Death Valley Driver, The Blackout, etc.\n\n"
        "Enter your finisher name:"
    )
    options = {"key": "_default", "goto": _set_finisher}
    return text, options


def _set_finisher(caller, raw_string, **kwargs):
    name = raw_string.strip()
    if not name or len(name) < 2:
        caller.msg("|rFinisher name must be at least 2 characters.|n")
        return "node_finisher"
    if len(name) > 40:
        caller.msg("|rFinisher name must be 40 characters or less.|n")
        return "node_finisher"
    caller.ndb._menutree.finisher_name = name
    return "node_finisher_type"


def node_finisher_type(caller, raw_string, **kwargs):
    """Choose finisher type."""
    text = (
        f"\n|wFINISHER TYPE|n\n"
        f"--------------\n"
        f"Finisher: |c{caller.ndb._menutree.finisher_name}|n\n\n"
        f"What kind of move is it?\n\n"
        f"  |w1|n. |cPower|n — Slams, bombs, drivers. Uses STR.\n"
        f"  |w2|n. |cTechnical|n — Submissions, locks. Uses TEC.\n"
        f"  |w3|n. |cAerial|n — Top rope, flying attacks. Uses AGI.\n"
        f"  |w4|n. |cShowstopper|n — Theatrics, dramatic. Uses CHA.\n\n"
        f"Choose (1-4):"
    )
    options = (
        {"key": "1", "desc": "Power", "goto": (_set_finisher_type, {"ftype": "power"})},
        {"key": "2", "desc": "Technical", "goto": (_set_finisher_type, {"ftype": "technical"})},
        {"key": "3", "desc": "Aerial", "goto": (_set_finisher_type, {"ftype": "aerial"})},
        {"key": "4", "desc": "Showstopper", "goto": (_set_finisher_type, {"ftype": "charisma"})},
    )
    return text, options


def _set_finisher_type(caller, raw_string, ftype="power", **kwargs):
    caller.ndb._menutree.finisher_type = ftype
    return "node_confirm"


def node_confirm(caller, raw_string, **kwargs):
    """Review and confirm character."""
    menu = caller.ndb._menutree
    style = menu.style
    style_bonuses = WRESTLING_STYLES.get(style, {})

    text = (
        "\n|w========================================|n\n"
        "|w         CHARACTER SUMMARY|n\n"
        "|w========================================|n\n\n"
        f"  Ring Name:  |c{menu.ring_name}|n\n"
        f"  Real Name:  |c{menu.real_name}|n\n"
        f"  Hometown:   |c{menu.hometown}|n\n"
        f"  Gender:     |c{menu.gender}|n"
        f" ({GENDER_OPTIONS[menu.gender]['division']})\n"
        f"  Style:      |c{style}|n\n"
        f"  Alignment:  "
    )

    if menu.alignment == "Face":
        text += "|gFace|n\n"
    else:
        text += "|rHeel|n\n"

    fed = STARTING_FEDS.get(menu.starting_fed, {})
    text += f"  Starting Fed: |c{fed.get('abbrev', '???')}|n — {fed.get('name', '???')}\n"
    text += f"  Finisher:   |c{menu.finisher_name}|n ({menu.finisher_type})\n\n"

    text += "  |wStats:|n\n"
    stat_order = ["str", "agi", "tec", "cha", "tou", "psy"]
    for key in stat_order:
        total = 5 + style_bonuses.get(key, 0) + menu.stat_alloc.get(key, 0)
        text += f"    {STAT_NAMES[key]:12s} {_format_stat_bar(total)}\n"

    text += (
        "\n|w========================================|n\n"
        "Is this correct?\n"
    )

    options = (
        {"key": "1", "desc": "Yes, create this wrestler", "goto": "node_finalize"},
        {"key": "2", "desc": "No, start over", "goto": "node_ring_name"},
    )
    return text, options


def node_finalize(caller, raw_string, **kwargs):
    """Apply all chargen choices to the character."""
    menu = caller.ndb._menutree

    # Set the ring name as the character key
    caller.key = menu.ring_name

    # Store identity
    caller.db.real_name = menu.real_name
    caller.db.hometown = menu.hometown
    caller.db.gender = menu.gender
    caller.db.wrestling_style = menu.style
    caller.db.alignment = menu.alignment
    caller.db.finisher_name = menu.finisher_name
    caller.db.finisher_type = menu.finisher_type

    # Starting fed
    fed_key = menu.starting_fed
    caller.db.territory = fed_key
    caller.db.tier = 1

    # Initialize traits
    caller.setup_traits()
    caller.apply_style_bonuses()
    caller.apply_bonus_points(menu.stat_alloc)

    # Mark chargen complete
    caller.db.chargen_complete = True

    # Move to starting location
    fed_data = STARTING_FEDS.get(fed_key, {})
    start_room = _find_start_room(fed_key)
    if start_room:
        caller.move_to(start_room, quiet=True)

    text = (
        "\n|w========================================|n\n"
        f"|w  {menu.ring_name} HAS ENTERED THE BUILDING|n\n"
        "|w========================================|n\n\n"
        f"You step out of a beat-up car into the parking lot of a\n"
        f"{fed_data.get('name', 'local wrestling fed')} in\n"
        f"{fed_data.get('location', 'somewhere')}.\n\n"
        f"The crowd tonight is maybe 40 people. The ring ropes are\n"
        f"held up with duct tape. Someone's uncle is doing commentary\n"
        f"into a RadioShack microphone.\n\n"
        f"This is where legends begin.\n\n"
        f"|wType 'look' to see your surroundings.|n\n"
        f"|wType 'stats' to see your character sheet.|n\n"
    )

    options = None  # Exit menu
    return text, options


def _find_start_room(fed_key):
    """Find the starting room for a given fed. Returns room object or None."""
    from evennia.utils.search import search_tag
    rooms = search_tag(f"start_{fed_key}", category="chargen")
    if rooms:
        return rooms[0]
    # Fallback: search by tag
    from evennia.utils.search import search_tag as _st
    rooms = _st(fed_key, category="territory")
    for room in rooms:
        if hasattr(room.db, 'room_type') and room.db.room_type in ("backyard", "parking"):
            return room
    # Last resort: find any room tagged with this territory
    if rooms:
        return rooms[0]
    return None
