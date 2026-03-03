"""
Kayfabe: Protect the Business — Injury System.

~5% chance per match, modified by TOU, move types, match intensity.
Injuries cause stat penalties and heal over game weeks.
Resting at inn/house speeds recovery.
"""

import random


INJURY_TYPES = {
    "shoulder": {
        "name": "Shoulder Injury",
        "stat_penalty": "str",
        "desc": "You've separated your shoulder. Power moves are excruciating.",
        "recovery_desc": "Your shoulder is feeling better. Almost back to full strength.",
    },
    "knee": {
        "name": "Knee Injury",
        "stat_penalty": "agi",
        "desc": "You've tweaked your knee. Every step in the ring is agony.",
        "recovery_desc": "The knee is stabilizing. You can move without wincing now.",
    },
    "neck": {
        "name": "Neck Injury",
        "stat_penalty": "tec",
        "desc": "A bad bump caught your neck wrong. Technical execution is compromised.",
        "recovery_desc": "The stiffness in your neck is easing. Technique coming back.",
    },
    "concussion": {
        "name": "Concussion",
        "stat_penalty": "psy",
        "desc": "You're seeing stars. Match psychology is fuzzy at best.",
        "recovery_desc": "The fog is clearing. Your ring awareness is returning.",
    },
    "back": {
        "name": "Back Injury",
        "stat_penalty": "tou",
        "desc": "Your back seized up. Taking bumps is going to be rough.",
        "recovery_desc": "The back spasms have stopped. You can take bumps again.",
    },
}

SEVERITY_LEVELS = {
    1: {"name": "Minor", "penalty": 2, "weeks": 1, "color": "|y"},
    2: {"name": "Moderate", "penalty": 4, "weeks": 2, "color": "|Y"},
    3: {"name": "Serious", "penalty": 6, "weeks": 4, "color": "|r"},
    4: {"name": "Severe", "penalty": 8, "weeks": 6, "color": "|R"},
}


def check_injury(character, match_intensity=50):
    """
    Roll for injury after a match.
    Base ~5% chance, modified by TOU and match intensity.

    Args:
        character: Wrestler character
        match_intensity: 0-100 (crowd_heat or move_count proxy)

    Returns:
        injury dict or None
    """
    tou = character.get_stat("tou") if hasattr(character, 'get_stat') else 10
    existing = character.db.injury

    # Base 5%, +1% per 20 intensity, -0.5% per TOU point above 10
    base_chance = 0.05
    intensity_mod = (match_intensity / 20) * 0.01
    tou_mod = max(0, (tou - 10)) * 0.005
    # Already injured wrestlers are more fragile
    fragile_mod = 0.03 if existing else 0.0

    chance = max(0.01, base_chance + intensity_mod - tou_mod + fragile_mod)

    if random.random() > chance:
        return None

    # Determine injury type
    injury_key = random.choice(list(INJURY_TYPES.keys()))
    injury_type = INJURY_TYPES[injury_key]

    # Determine severity (weighted toward minor)
    severity_roll = random.random()
    if severity_roll < 0.50:
        severity = 1
    elif severity_roll < 0.80:
        severity = 2
    elif severity_roll < 0.95:
        severity = 3
    else:
        severity = 4

    sev_info = SEVERITY_LEVELS[severity]

    injury = {
        "type": injury_key,
        "name": injury_type["name"],
        "severity": severity,
        "severity_name": sev_info["name"],
        "weeks_remaining": sev_info["weeks"],
        "stat_penalty": injury_type["stat_penalty"],
        "penalty_amount": sev_info["penalty"],
    }

    return injury


def apply_injury(character, injury):
    """
    Apply an injury to a character. Stores in character.db.injury.
    """
    character.db.injury = injury

    sev_info = SEVERITY_LEVELS[injury["severity"]]
    injury_type = INJURY_TYPES[injury["type"]]

    msg = (
        f"\n|r*** INJURY ***|n\n"
        f"  {sev_info['color']}{sev_info['name']} {injury_type['name']}|n\n"
        f"  {injury_type['desc']}\n"
        f"  |rPenalty: -{injury['penalty_amount']} {injury['stat_penalty'].upper()}|n\n"
        f"  |yRecovery: ~{injury['weeks_remaining']} game week{'s' if injury['weeks_remaining'] != 1 else ''}|n\n"
    )
    character.msg(msg)

    # Dirt sheet: log injury
    from world.dirtsheet import log_event
    log_event("injury",
              name=character.key,
              injury_type=injury_type["name"].lower(),
              severity=sev_info["name"].lower())


def process_injury_recovery(character, is_resting=False):
    """
    Process one week of injury recovery for a character.
    Called from EconomyTickScript.

    Args:
        character: Wrestler character
        is_resting: True if in safe lodging (speeds recovery)

    Returns:
        True if injury healed this tick, False otherwise
    """
    injury = character.db.injury
    if not injury:
        return False

    # Decrement weeks
    weeks = injury.get("weeks_remaining", 0)
    if is_resting:
        weeks -= 2  # Rest speeds recovery
    else:
        weeks -= 1

    if weeks <= 0:
        # Healed
        injury_type = INJURY_TYPES.get(injury["type"], {})
        character.db.injury = None
        if character.sessions.count():
            character.msg(
                f"|g*** INJURY HEALED ***|n\n"
                f"  {injury_type.get('recovery_desc', 'You have recovered from your injury.')}\n"
            )
        return True
    else:
        injury["weeks_remaining"] = weeks
        character.db.injury = injury
        return False


def get_injury_stat_penalty(character, stat_key):
    """
    Get the stat penalty from an active injury.
    Returns the penalty amount (positive number to subtract) or 0.
    """
    injury = character.db.injury
    if not injury:
        return 0
    if injury.get("stat_penalty") == stat_key:
        return injury.get("penalty_amount", 0)
    return 0


def format_injury_status(character):
    """Format injury info for display."""
    injury = character.db.injury
    if not injury:
        return None

    sev_info = SEVERITY_LEVELS.get(injury["severity"], SEVERITY_LEVELS[1])
    return (
        f"{sev_info['color']}{sev_info['name']} {injury.get('name', 'Injury')}|n"
        f" (-{injury.get('penalty_amount', 0)} {injury.get('stat_penalty', '???').upper()},"
        f" {injury.get('weeks_remaining', 0)} week{'s' if injury.get('weeks_remaining', 0) != 1 else ''} left)"
    )
