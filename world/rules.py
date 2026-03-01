"""
Kayfabe: Protect the Business — Game rules engine.

Core mechanics:
- Stat checks (d20 + stat modifier vs difficulty)
- Match quality calculation (star ratings 0-5)
- XP and leveling
- Rank progression
- Kayfabe scoring
- Alignment mechanics
- Training gains
- Promo resolution
"""

import random
import math

# --- Rank Progression ---

RANK_THRESHOLDS = {
    0: ("Greenhorn", 0),
    1: ("Jobber", 100),
    2: ("Enhancement", 300),
    3: ("Midcarder", 700),
    4: ("Upper Midcarder", 1500),
    5: ("Main Eventer", 3000),
    6: ("Champion", 6000),
    7: ("Legend", 12000),
}

TIER_LEVEL_RANGES = {
    1: (1, 5),
    2: (5, 15),
    3: (15, 30),
    3.5: (25, 35),
    4: (35, 50),
}


# --- Stat Checks ---

def stat_check(stat_value, difficulty, bonus=0):
    """
    Core stat check: d20 + stat_mod vs difficulty target.
    stat_mod = (stat_value - 10) / 2, floored.
    Returns (success: bool, roll: int, total: int, margin: int).
    """
    mod = (stat_value - 10) // 2
    roll = random.randint(1, 20)
    total = roll + mod + bonus
    margin = total - difficulty
    success = total >= difficulty
    return success, roll, total, margin


def opposed_check(attacker_stat, defender_stat, attacker_bonus=0, defender_bonus=0):
    """
    Opposed stat check. Both roll d20 + stat_mod.
    Returns (attacker_wins: bool, attacker_total: int, defender_total: int, margin: int).
    """
    a_mod = (attacker_stat - 10) // 2
    d_mod = (defender_stat - 10) // 2
    a_roll = random.randint(1, 20)
    d_roll = random.randint(1, 20)
    a_total = a_roll + a_mod + attacker_bonus
    d_total = d_roll + d_mod + defender_bonus
    margin = a_total - d_total
    return a_total > d_total, a_total, d_total, margin


# --- Match Quality ---

def calculate_match_quality(wrestler_a, wrestler_b, crowd_heat=50, match_length=5):
    """
    Calculate star rating for a match (0.0 - 5.0).

    Factors:
    - Average PSY of both wrestlers (psychology = match layout)
    - Average TEC (technical ability = execution)
    - Crowd heat (0-100, from promos, storylines, kayfabe)
    - Match length bonus (longer matches have more time to tell a story)
    - Random variance (some nights are just better)

    Returns (stars: float, breakdown: dict).
    """
    def _get_stat(w, key):
        if hasattr(w, 'get_stat'):
            return w.get_stat(key)
        return getattr(w, key, 5)

    avg_psy = (_get_stat(wrestler_a, "psy") + _get_stat(wrestler_b, "psy")) / 2
    avg_tec = (_get_stat(wrestler_a, "tec") + _get_stat(wrestler_b, "tec")) / 2
    avg_cha = (_get_stat(wrestler_a, "cha") + _get_stat(wrestler_b, "cha")) / 2

    # Base quality from psychology (0-2 stars)
    psy_contrib = min(avg_psy / 10.0, 2.0)

    # Technical execution (0-1.5 stars)
    tec_contrib = min(avg_tec / 13.0, 1.5)

    # Crowd heat contribution (0-1 star)
    heat_contrib = min(crowd_heat / 100.0, 1.0)

    # Match length bonus (short matches cap at 3 stars)
    length_bonus = min(match_length / 10.0, 0.5)

    # Random variance (-0.5 to +0.5)
    variance = random.uniform(-0.5, 0.5)

    # Charisma tie-breaker (0-0.25)
    cha_bonus = min(avg_cha / 80.0, 0.25)

    raw_stars = psy_contrib + tec_contrib + heat_contrib + length_bonus + cha_bonus + variance

    # Clamp to 0-5, round to nearest quarter
    stars = max(0.0, min(5.0, raw_stars))
    stars = round(stars * 4) / 4  # quarter-star increments

    breakdown = {
        "psychology": round(psy_contrib, 2),
        "technical": round(tec_contrib, 2),
        "crowd_heat": round(heat_contrib, 2),
        "length_bonus": round(length_bonus, 2),
        "charisma_bonus": round(cha_bonus, 2),
        "variance": round(variance, 2),
    }

    return stars, breakdown


def star_rating_display(stars):
    """Convert star rating to display string."""
    full = int(stars)
    frac = stars - full
    display = "*" * full
    if frac >= 0.75:
        display += "*"
    elif frac >= 0.5:
        display += "3/4"
    elif frac >= 0.25:
        display += "1/2"
    # Pad for readability
    return f"|y{display}|n ({stars:.2f})" if stars > 0 else "|xDUD|n (0.00)"


# --- XP and Leveling ---

def xp_for_match(stars, won, card_position="opener"):
    """Calculate XP earned from a match."""
    base_xp = int(stars * 20)  # 0-100 base from quality
    win_bonus = 15 if won else 5
    position_mult = {
        "dark": 0.5,
        "opener": 1.0,
        "midcard": 1.5,
        "semi_main": 2.0,
        "main_event": 3.0,
    }
    mult = position_mult.get(card_position, 1.0)
    return int((base_xp + win_bonus) * mult)


def xp_for_promo(quality):
    """XP from cutting a promo. quality = margin from stat check."""
    if quality >= 10:
        return 25  # amazing promo
    elif quality >= 5:
        return 15  # good promo
    elif quality >= 0:
        return 8   # decent promo
    else:
        return 3   # bombed


def xp_to_next_level(current_level):
    """XP needed to reach the next level."""
    return 50 + (current_level * 25)


def check_level_up(character):
    """Check if character has enough XP to level up. Apply if so. Returns levels gained."""
    levels_gained = 0
    while True:
        needed = xp_to_next_level(character.db.level)
        if character.db.xp >= needed:
            character.db.xp -= needed
            character.db.level += 1
            levels_gained += 1
        else:
            break
    return levels_gained


def check_rank_up(character):
    """Check if character qualifies for a rank promotion. Returns new rank or None."""
    current_idx = character.db.rank_index or 0
    next_idx = current_idx + 1
    if next_idx not in RANK_THRESHOLDS:
        return None

    rank_name, xp_threshold = RANK_THRESHOLDS[next_idx]

    # Check total career XP (wins * quality matters more than raw XP)
    total_career = (character.db.wins or 0) * 20 + (character.db.xp or 0)
    if total_career >= xp_threshold:
        character.db.rank_index = next_idx
        character.db.rank = rank_name
        return rank_name
    return None


# --- Kayfabe ---

def kayfabe_change(character, amount, reason=""):
    """Adjust kayfabe score, clamped 0-100."""
    old = character.db.kayfabe or 50
    new = max(0, min(100, old + amount))
    character.db.kayfabe = new
    return new - old  # actual change


def kayfabe_check(character, difficulty=10):
    """Check if character maintains kayfabe. Uses CHA + PSY."""
    cha = character.get_stat("cha")
    psy = character.get_stat("psy")
    avg = (cha + psy) // 2
    return stat_check(avg, difficulty)


# --- Training ---

def training_gain(character, stat_key, room_bonus=0):
    """
    Attempt to train a stat. Returns (gained: bool, amount: float, message: str).
    Training has diminishing returns at higher stat values.
    """
    current = character.get_stat(stat_key)

    # Diminishing returns: harder to gain at higher values
    # Base chance: 90% at stat 5, drops to 30% at stat 20
    chance = max(0.15, 1.0 - (current - 5) * 0.04)

    if random.random() > chance:
        return False, 0, "You push hard but don't make any gains today."

    # Gain amount: 0.5-1.0 base, + room bonus
    base_gain = random.uniform(0.3, 0.8)
    total_gain = base_gain + (room_bonus * 0.3)

    # Apply via trait
    trait = character.traits.get(stat_key)
    if trait:
        trait.base += total_gain

    return True, total_gain, f"You feel yourself getting stronger. (+{total_gain:.1f})"


# --- Promo Resolution ---

PROMO_TYPES = {
    "fire": {
        "name": "Fire Promo",
        "stat": "cha",
        "secondary": "psy",
        "difficulty": 10,
        "alignment": "Face",
        "desc": "You grab the mic and rally the crowd with passion and fire!",
        "success": "{name} delivers a FIRE promo! The crowd is on their feet!",
        "failure": "{name} stumbles over their words. The crowd politely claps.",
        "great": "{name} cuts the promo of a LIFETIME! The building is shaking!",
    },
    "heat": {
        "name": "Heat Promo",
        "stat": "cha",
        "secondary": "psy",
        "difficulty": 10,
        "alignment": "Heel",
        "desc": "You grab the mic and insult everyone in the building!",
        "success": "{name} generates massive HEAT! Trash is flying into the ring!",
        "failure": "{name} tries to get heat but the crowd just doesn't care.",
        "great": "{name} has the crowd ready to RIOT! Security is on standby!",
    },
    "challenge": {
        "name": "Challenge Promo",
        "stat": "cha",
        "secondary": "psy",
        "difficulty": 12,
        "alignment": None,  # any alignment
        "desc": "You call out your opponent by name!",
        "success": "{name} calls out {target}! The crowd wants this match!",
        "failure": "{name} issues a challenge but it falls flat.",
        "great": "{name} cuts a challenge promo so intense the crowd is DEMANDING this match!",
    },
    "shoot": {
        "name": "Shoot Promo",
        "stat": "psy",
        "secondary": "cha",
        "difficulty": 15,
        "alignment": "Anti-Hero",  # anti-hero preferred, others take kayfabe hit
        "desc": "You break the fourth wall and speak from the heart.",
        "success": "{name} goes OFF SCRIPT! The crowd doesn't know what's real anymore!",
        "failure": "{name} tries to shoot but it comes off as scripted. Awkward.",
        "great": "{name} delivers a worked-shoot that will be talked about for YEARS!",
    },
    "manager": {
        "name": "Manager Promo",
        "stat": "cha",
        "secondary": "psy",
        "difficulty": 10,
        "alignment": None,
        "desc": "Your manager takes the mic.",
        "success": "{manager} delivers a masterful promo on behalf of {name}!",
        "failure": "{manager} fumbles the promo. Not their best night.",
        "great": "{manager} cuts a LEGENDARY promo! {name} doesn't even need to talk!",
    },
}


def resolve_promo(character, promo_type, target_name="", manager_name=""):
    """
    Resolve a promo attempt.
    Returns (quality: str, margin: int, xp: int, kayfabe_delta: int, message: str).
    quality: "great" / "success" / "failure"
    """
    ptype = PROMO_TYPES.get(promo_type)
    if not ptype:
        return "failure", 0, 0, 0, "Unknown promo type."

    # Get stats
    primary = character.get_stat(ptype["stat"])
    secondary = character.get_stat(ptype["secondary"])
    bonus = secondary // 4  # secondary stat adds partial bonus

    # Alignment bonus/penalty
    alignment = character.db.alignment
    pref_align = ptype["alignment"]
    align_bonus = 0
    kayfabe_delta = 0

    if pref_align:
        if alignment == pref_align:
            align_bonus = 3  # alignment match
        elif pref_align == "Anti-Hero" and alignment != "Anti-Hero":
            align_bonus = -3  # shooting without being anti-hero is risky
            kayfabe_delta = -5  # breaks kayfabe
        elif alignment == "Anti-Hero":
            align_bonus = 1  # anti-heroes get a small bonus to everything

    # Face doing heel promo or vice versa — kayfabe hit
    if pref_align == "Face" and alignment == "Heel":
        kayfabe_delta = -3
    elif pref_align == "Heel" and alignment == "Face":
        kayfabe_delta = -3

    success, roll, total, margin = stat_check(
        primary, ptype["difficulty"], bonus=bonus + align_bonus
    )

    name = character.key
    fmt = {"name": name, "target": target_name, "manager": manager_name}

    if margin >= 10:
        quality = "great"
        msg = ptype["great"].format(**fmt)
        xp = xp_for_promo(margin)
        kayfabe_delta += 3
    elif success:
        quality = "success"
        msg = ptype["success"].format(**fmt)
        xp = xp_for_promo(margin)
        kayfabe_delta += 1
    else:
        quality = "failure"
        msg = ptype["failure"].format(**fmt)
        xp = xp_for_promo(margin)
        kayfabe_delta -= 1

    return quality, margin, xp, kayfabe_delta, msg


# --- Match Payoff ---

def match_payoff(tier, card_position, stars, won):
    """Calculate dollar payoff for a match."""
    base_pay = {1: 5, 2: 15, 3: 50, 3.5: 75, 4: 200}
    base = base_pay.get(tier, 10)

    position_mult = {
        "dark": 0.25,
        "opener": 0.5,
        "midcard": 1.0,
        "semi_main": 1.5,
        "main_event": 2.5,
    }
    mult = position_mult.get(card_position, 0.5)

    quality_bonus = stars * 10
    win_bonus = base * 0.25 if won else 0

    return int((base * mult) + quality_bonus + win_bonus)


# --- Fan Encounter Events ---

FAN_ENCOUNTERS = [
    {
        "key": "gas_station",
        "name": "Gas Station Spot",
        "desc": (
            "You're getting gas at a highway rest stop when a fan spots you.\n"
            "They recognize you from last week's show."
        ),
        "choices": [
            {
                "key": "stay",
                "desc": "Stay in character",
                "kayfabe": 3,
                "msg": "You stay in character, {align_action}. The fan eats it up. Kayfabe protected.",
            },
            {
                "key": "break",
                "desc": "Be yourself",
                "kayfabe": -5,
                "msg": "You break character and chat like a normal person. Nice... but the mystique is gone.",
            },
            {
                "key": "ignore",
                "desc": "Ignore them",
                "kayfabe": 0,
                "msg": "You keep your head down and pump your gas. The fan is disappointed but kayfabe is safe.",
            },
        ],
    },
    {
        "key": "restaurant",
        "name": "Restaurant Ambush",
        "desc": (
            "You're eating at a diner when a mark sees you sitting with a wrestler\n"
            "you're feuding with on TV. They look confused."
        ),
        "choices": [
            {
                "key": "brawl",
                "desc": "Stage a confrontation",
                "kayfabe": 5,
                "msg": "You flip the table and start yelling at your 'rival.' The mark is SHOOK. Kayfabe PROTECTED.",
            },
            {
                "key": "explain",
                "desc": "Explain it's a show",
                "kayfabe": -8,
                "msg": "You explain that wrestling is a work. The mark looks betrayed. Kayfabe: EXPOSED.",
            },
            {
                "key": "leave",
                "desc": "Leave separately",
                "kayfabe": 1,
                "msg": "Your 'rival' gets up and leaves first. You wait five minutes. Close call.",
            },
        ],
    },
    {
        "key": "kid_fan",
        "name": "Kid Fan",
        "desc": (
            "A little kid spots you in the parking lot. If you're a heel,\n"
            "the kid looks scared. If you're a face, they're starstruck."
        ),
        "choices": [
            {
                "key": "character",
                "desc": "Stay in character",
                "kayfabe": 4,
                "msg_face": "You kneel down and tell the kid to say their prayers and eat their vitamins. The kid's eyes go wide.",
                "msg_heel": "You snarl at the kid and they hide behind their parent. You're a monster... but kayfabe lives.",
            },
            {
                "key": "nice",
                "desc": "Be nice (break character if heel)",
                "kayfabe_face": 2,
                "kayfabe_heel": -5,
                "msg_face": "You sign an autograph and make the kid's year. Being a face rules.",
                "msg_heel": "You smile and wave at the kid. Sweet... but a fan with a camera just saw the heel being nice.",
            },
        ],
    },
    {
        "key": "gym_encounter",
        "name": "Gym Encounter",
        "desc": (
            "A fan spots you at the gym training with someone you're feuding\n"
            "with on screen. They pull out a camera."
        ),
        "choices": [
            {
                "key": "separate",
                "desc": "Move to different areas",
                "kayfabe": 2,
                "msg": "You and your 'rival' split up. The fan lowers the camera, unsure what they saw.",
            },
            {
                "key": "confront",
                "desc": "Stage a gym confrontation",
                "kayfabe": 5,
                "msg": "You get in your rival's face, shoving equipment aside. The fan's video goes viral. Kayfabe GOLD.",
            },
            {
                "key": "ignore",
                "desc": "Don't care",
                "kayfabe": -3,
                "msg": "You keep spotting each other like nothing's wrong. The fan posts the video. 'Wrestling is fake lol'",
            },
        ],
    },
]


# --- Promoter Trust ---

def get_promoter_trust(character, territory_key):
    """Get the character's trust level with a territory promoter (0-100, default 50)."""
    trust = character.db.promoter_trust or {}
    return trust.get(territory_key, 50)


def change_promoter_trust(character, territory_key, amount, reason=""):
    """Adjust promoter trust for a territory, clamped 0-100."""
    trust = character.db.promoter_trust or {}
    old = trust.get(territory_key, 50)
    new = max(0, min(100, old + amount))
    trust[territory_key] = new
    character.db.promoter_trust = trust
    return new - old


def get_card_position(character, territory_key):
    """
    Determine card position based on rank, trust, and level.
    Returns one of: dark, opener, midcard, semi_main, main_event
    """
    trust = get_promoter_trust(character, territory_key)
    rank_idx = character.db.rank_index or 0
    level = character.db.level or 1

    # Base position from rank
    if rank_idx <= 1:
        base = "dark"
    elif rank_idx == 2:
        base = "opener"
    elif rank_idx == 3:
        base = "midcard"
    elif rank_idx == 4:
        base = "semi_main"
    else:
        base = "main_event"

    # Trust modifier: low trust demotes you, high trust promotes
    positions = ["dark", "opener", "midcard", "semi_main", "main_event"]
    idx = positions.index(base)

    if trust < 20:
        idx = max(0, idx - 2)
    elif trust < 40:
        idx = max(0, idx - 1)
    elif trust >= 80:
        idx = min(len(positions) - 1, idx + 1)

    return positions[idx]


# --- Titles ---

TERRITORY_TITLES = {
    # Tier 3 regional titles
    "memphis": "Memphis Heavyweight Championship",
    "midsouth": "Mid-South North American Championship",
    "midatlantic": "NWA Mid-Atlantic Championship",
    "florida": "Florida Heavyweight Championship",
    "georgia": "NWA Georgia Championship",
    "wccw": "World Class Championship",
    "awa": "AWA World Heavyweight Championship",
    "stampede": "Stampede North American Championship",
    "pnw": "Pacific Northwest Championship",
    # Tier 3.5 developmental titles
    "ovw": "OVW Television Championship",
    "fcw": "FCW Championship",
    "dsw": "DSW Championship",
    "hwa": "HWA Championship",
    # Tier 4 national/international titles
    "wwf": "WWF Championship",
    "wcw": "WCW World Heavyweight Championship",
    "ecw": "ECW World Championship",
    "uk": "World of Sport Championship",
    "japan": "IWGP Heavyweight Championship",
}

# Women's championship variants (territories with women's divisions)
TERRITORY_TITLES_WOMENS = {
    "wwf": "WWF Women's Championship",
    "wcw": "WCW Women's Championship",
    "ecw": "ECW Women's Championship",
    "japan": "IWGP Women's Championship",
    "awa": "AWA Women's Championship",
    "memphis": "Memphis Women's Championship",
}


def random_fan_encounter():
    """Return a random fan encounter dict, or None (40% chance of encounter)."""
    if random.random() < 0.4:
        return random.choice(FAN_ENCOUNTERS)
    return None
