"""
Kayfabe: Protect the Business — Random NPC generator for Tier 1 backyard feds.

Generates low-level NPCs with silly ring names and randomized low stats.
"""

import random

# Backyard NPC name parts
FIRST_NAMES = [
    "Folding Chair", "Backyard", "Trampoline", "Parking Lot", "Basement",
    "Garbage Can", "Duct Tape", "Plywood", "Barbed Wire", "Thumbtack",
    "Shopping Cart", "Table Top", "Ladder Match", "Steel Cage", "Dumpster",
    "Concrete", "Mattress", "Kiddie Pool", "Lawnmower", "Chainsaw",
    "Weed Whacker", "Propane", "Hibachi", "Sprinkler", "Garden Hose",
]

LAST_NAMES = [
    "Phil", "Steve", "Betty", "Jim", "Dave",
    "Mike", "Tony", "Eddie", "Bobby", "Tommy",
    "Rick", "Jack", "Hank", "Earl", "Duke",
    "Bubba", "Slim", "Tiny", "Big Boy", "Kid",
    "Junior", "Ace", "Spike", "Tank", "Flash",
]

EPITHETS = [
    "The Human Highlight Reel",
    "The Extreme Machine",
    "The Hardcore Legend",
    "The Deathmatch King",
    "The Backyard Butcher",
    "The Living Weapon",
    "The Pain Train",
    "Mr. Monday Night",
    "The Future of Wrestling",
    "The People's Champ",
    "The Last Outlaw",
    "The One Man Wrecking Crew",
    "The Innovator of Violence",
    "Two-Time Backyard Champion",
    "The Rated-R Superstar",
]

FINISHER_NAMES = [
    "The Trash Compactor",
    "Lawn Dart",
    "Backyard Bomb",
    "The Recycler",
    "Pavement Princess",
    "The Can Opener",
    "Table Flip",
    "The Eviction Notice",
    "Dumpster Dive",
    "The Yard Sale",
    "Sprinkler Splash",
    "The Weed Whacker",
    "Garage Door Slam",
    "The Basement DDT",
    "Trampoline Torpedo",
]

ALIGNMENTS = ["Face", "Heel"]


def generate_backyard_npc():
    """
    Generate a random backyard NPC data dict.
    Returns dict suitable for spawning a BackyardNPC.
    """
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    ring_name = f"{first} {last}"

    # Sometimes add an epithet
    if random.random() < 0.3:
        epithet = random.choice(EPITHETS)
        ring_name = f'"{epithet}" {last}'

    # Low stats: 3-8 each
    stats = {
        "str": random.randint(3, 8),
        "agi": random.randint(3, 8),
        "tec": random.randint(2, 6),
        "cha": random.randint(2, 7),
        "tou": random.randint(3, 8),
        "psy": random.randint(1, 5),
    }

    return {
        "ring_name": ring_name,
        "alignment": random.choice(ALIGNMENTS),
        "finisher_name": random.choice(FINISHER_NAMES),
        "finisher_type": random.choice(["power", "technical", "aerial", "charisma"]),
        "level": random.randint(1, 5),
        "stats": stats,
    }


def generate_fed_roster(fed_key, count=6):
    """Generate a roster of random NPCs for a backyard fed."""
    roster = []
    used_names = set()
    for _ in range(count):
        npc = generate_backyard_npc()
        # Avoid duplicate names
        while npc["ring_name"] in used_names:
            npc = generate_backyard_npc()
        used_names.add(npc["ring_name"])
        npc["home_territory"] = fed_key
        roster.append(npc)
    return roster
