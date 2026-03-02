"""
Kayfabe: Protect the Business — Match Commentary System.

Provides color commentary during matches when an announcer NPC is present.
Commentary fires ~30% of the time per move to avoid spam.
"""

import random


COMMENTARY = {
    "opening": {
        "success": [
            "And {attacker} connects! Nice start to this one.",
            "Beautiful execution by {attacker}. This kid can work.",
            "{attacker} takes the early advantage with that maneuver!",
            "Textbook! {attacker} showing what they can do in this opening exchange.",
            "The crowd appreciates that one — {attacker} is crisp tonight.",
            "{attacker} sets the pace early! {defender} needs to regroup.",
        ],
        "fail": [
            "{attacker} goes for it but {defender} was ready! Smart counter.",
            "Missed! {attacker} whiffs and {defender} takes advantage.",
            "Not quite — {attacker} is a little off tonight.",
            "{defender} saw that coming a mile away.",
            "Sloppy execution there by {attacker}. The nerves maybe getting to them.",
        ],
    },
    "heat": {
        "success": [
            "{attacker} is just PUNISHING {defender} right now!",
            "Methodical offense by {attacker}. They're picking {defender} apart.",
            "{attacker} is in complete control! This is getting ugly.",
            "Devastating! {defender} is in real trouble here!",
            "The crowd is BOOING as {attacker} continues the assault!",
            "{attacker} is working over {defender} like a seasoned pro.",
        ],
        "fail": [
            "{defender} gets a shot in! Is this the opening they need?",
            "Wait — {attacker} makes a mistake and {defender} capitalizes!",
            "{defender} refuses to go quietly! There's still fight in them!",
            "Reversal! But {attacker} quickly regains control.",
        ],
    },
    "hope": {
        "success": [
            "{attacker} fires back! The crowd is stirring!",
            "Signs of life from {attacker}! But can they sustain it?",
            "{attacker} with a flurry! The fans are trying to rally behind them!",
            "HOPE SPOT! {attacker} lands one but {defender} cuts them right off!",
        ],
        "fail": [
            "{attacker} tries to fight back but gets shut down immediately!",
            "Not yet! The crowd groans as {attacker}'s hope is snuffed out.",
            "{defender} saw the comeback coming and put a stop to it!",
        ],
    },
    "comeback": {
        "success": [
            "{attacker} is FIRING UP! The crowd is going CRAZY!",
            "MOMENTUM SHIFT! {attacker} is feeding off this crowd!",
            "{attacker} is on a roll! {defender} can't stop them now!",
            "The building is SHAKING! {attacker} has the crowd in the palm of their hand!",
            "HERE COMES {attacker}! This is what wrestling is all about!",
            "UNBELIEVABLE! {attacker} is mounting the comeback of a lifetime!",
        ],
        "fail": [
            "{defender} stops the comeback in its tracks!",
            "OH NO! {attacker} had the momentum but {defender} cuts them off!",
            "So close! The crowd deflates as {attacker}'s rally stalls.",
        ],
    },
    "finish": {
        "success": [
            "THIS COULD BE IT! {attacker} connects with a HUGE shot!",
            "NEAR FALL! The crowd thought that was three!",
            "{attacker} is going for the kill! This match is almost over!",
            "INCREDIBLE! {attacker} hits it flush! Cover—!",
            "What a match we're witnessing! {attacker} with another big shot!",
            "The crowd is on their feet! {attacker} smells blood!",
        ],
        "fail": [
            "{defender} KICKS OUT! The crowd ERUPTS!",
            "HOW DID {defender} SURVIVE THAT?!",
            "NOT YET! {defender} refuses to stay down!",
            "{attacker} can't believe it! They thought that was the finish!",
        ],
    },
}

# Special commentary for finisher attempts
FINISHER_COMMENTARY = {
    "hit": [
        "IT'S OVER! {attacker} hits the {finisher}! COVER!",
        "{attacker} NAILS IT! The {finisher}! ONE! TWO! THREE!",
        "THE {finisher}! Nobody gets up from that!",
    ],
    "kickout": [
        "THE CROWD ERUPTS! {defender} kicked out of the {finisher}!",
        "UNBELIEVABLE! {defender} survives the {finisher}!",
        "HOW?! How did {defender} kick out of that?!",
    ],
}


def get_commentary(phase, success, attacker_name, defender_name, announcer_name=None):
    """
    Get a commentary line for a move. Returns formatted string or None.
    Only fires ~30% of the time to avoid spam.
    """
    if random.random() > 0.30:
        return None

    phase_lines = COMMENTARY.get(phase, {})
    key = "success" if success else "fail"
    lines = phase_lines.get(key, [])
    if not lines:
        return None

    line = random.choice(lines)
    line = line.format(attacker=attacker_name, defender=defender_name)

    if announcer_name:
        return f'|m[{announcer_name}]: "{line}"|n'
    return f'|m[Commentary]: "{line}"|n'


def get_finisher_commentary(hit, attacker_name, defender_name, finisher_name, announcer_name=None):
    """
    Get commentary for a finisher attempt. Always fires (big moment).
    """
    key = "hit" if hit else "kickout"
    lines = FINISHER_COMMENTARY.get(key, [])
    if not lines:
        return None

    line = random.choice(lines)
    line = line.format(
        attacker=attacker_name,
        defender=defender_name,
        finisher=finisher_name,
    )

    if announcer_name:
        return f'|m[{announcer_name}]: "{line}"|n'
    return f'|m[Commentary]: "{line}"|n'


def find_announcer_in_room(room):
    """
    Check if there's an announcer NPC in the room.
    Returns the announcer's name or None.
    """
    if not room:
        return None
    for obj in room.contents:
        if hasattr(obj, 'db') and getattr(obj.db, 'role', None) == "announcer":
            return obj.key
    return None
