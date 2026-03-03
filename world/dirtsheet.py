"""
Kayfabe: Protect the Business — Dirt Sheet Newsletter System.

Auto-generated weekly newsletter summarizing game events.
Events are logged from match results, injuries, rank-ups,
title changes, contracts, and stable activity.
"""

import random
import time
from evennia.scripts.scripts import DefaultScript
from evennia.utils import logger


def _get_dirtsheet_script():
    """Find or create the DirtSheetScript."""
    from evennia.scripts.models import ScriptDB
    try:
        return ScriptDB.objects.get(db_key="dirtsheet")
    except ScriptDB.DoesNotExist:
        script = DirtSheetScript.objects.create(db_key="dirtsheet")
        script.db.events = []
        script.db.current_issue = None
        script.db.archive = []
        script.db.week = 0
        return script
    except ScriptDB.MultipleObjectsReturned:
        return ScriptDB.objects.filter(db_key="dirtsheet").first()


def log_event(event_type, **data):
    """
    Log a game event to the dirt sheet.

    Args:
        event_type: One of match_result, title_change, injury, rank_up, contract, stable
        **data: Event-specific data (names, territories, details, etc.)
    """
    script = _get_dirtsheet_script()
    events = script.db.events or []
    events.append({
        "type": event_type,
        "time": time.time(),
        "data": data,
    })
    script.db.events = events


# Flavor text pools for the wrestling journalist voice
_MATCH_FLAVOR = [
    "Sources say the crowd was electric for this one.",
    "Our ringside correspondent reports an absolute classic.",
    "Multiple sources confirm: this was the real deal.",
    "The locker room was buzzing about this one afterward.",
    "Word backstage is this match stole the show.",
    "We're told the boys in the back gave a standing ovation.",
]

_TITLE_FLAVOR = [
    "A new era begins!",
    "The landscape of the territory just changed forever.",
    "We're told the locker room is in shock.",
    "Sources close to the promotion call it a seismic shift.",
]

_INJURY_FLAVOR = [
    "Road agents are concerned about the timeline.",
    "We're told the injury happened late in the match.",
    "Insiders say the worker is in good spirits despite the setback.",
]

_RANK_FLAVOR = [
    "The wrestling world is taking notice.",
    "Promoters across the territories are watching closely.",
    "Sources say multiple territories have expressed interest.",
]

_CONTRACT_FLAVOR = [
    "Terms of the deal were not disclosed.",
    "We're told both sides are excited about the arrangement.",
    "Insiders say the deal was done quickly.",
]

_STABLE_FLAVOR = [
    "The power dynamics in the territory just shifted.",
    "Sources say this has been in the works for weeks.",
]


def _star_display(stars):
    """Convert star rating to asterisk display."""
    full = int(stars)
    half = stars - full >= 0.25
    quarter = stars - full >= 0.125 and not half
    s = "*" * full
    if half:
        s += "1/2"
    elif quarter:
        s += "1/4"
    return s


def generate_newsletter(week_number, events):
    """
    Transform raw events into a wrestling journalist newsletter.

    Args:
        week_number: Current game week number
        events: List of event dicts from the past week

    Returns:
        dict with week, stories (list of str), generated_at
    """
    stories = []

    # Match of the week (highest star match)
    match_events = [e for e in events if e["type"] == "match_result"]
    if match_events:
        best = max(match_events, key=lambda e: e["data"].get("stars", 0))
        d = best["data"]
        stars = d.get("stars", 0)
        star_str = _star_display(stars)
        winner = d.get("winner", "???")
        loser = d.get("loser", "???")
        territory = d.get("territory", "parts unknown")
        flavor = random.choice(_MATCH_FLAVOR)
        stories.append(
            f"MATCH OF THE WEEK: {winner} def. {loser} "
            f"({star_str}) at {territory.upper()}\n"
            f"  {flavor}"
        )
        # Runner-up matches
        others = sorted(match_events, key=lambda e: e["data"].get("stars", 0), reverse=True)[1:3]
        for m in others:
            md = m["data"]
            stories.append(
                f"NOTABLE MATCH: {md.get('winner', '???')} def. {md.get('loser', '???')} "
                f"({_star_display(md.get('stars', 0))}) at {md.get('territory', '???').upper()}"
            )

    # Title changes
    title_events = [e for e in events if e["type"] == "title_change"]
    for e in title_events:
        d = e["data"]
        stories.append(
            f"TITLE CHANGE: {d.get('winner', '???')} captures the "
            f"{d.get('title_name', 'Championship')}!\n"
            f"  {random.choice(_TITLE_FLAVOR)}"
        )

    # Injuries
    injury_events = [e for e in events if e["type"] == "injury"]
    for e in injury_events:
        d = e["data"]
        stories.append(
            f"INJURY REPORT: {d.get('name', '???')} is nursing a "
            f"{d.get('injury_type', 'unknown')} injury ({d.get('severity', 'unknown')}).\n"
            f"  {random.choice(_INJURY_FLAVOR)}"
        )

    # Rank ups
    rank_events = [e for e in events if e["type"] == "rank_up"]
    for e in rank_events:
        d = e["data"]
        stories.append(
            f"RISING STAR: {d.get('name', '???')} promoted to {d.get('new_rank', '???')}.\n"
            f"  {random.choice(_RANK_FLAVOR)}"
        )

    # Contracts
    contract_events = [e for e in events if e["type"] == "contract"]
    for e in contract_events:
        d = e["data"]
        stories.append(
            f"SIGNED: {d.get('name', '???')} inks a deal with "
            f"{d.get('territory', '???')} (${d.get('pay', 0)}/week).\n"
            f"  {random.choice(_CONTRACT_FLAVOR)}"
        )

    # Stables
    stable_events = [e for e in events if e["type"] == "stable"]
    for e in stable_events:
        d = e["data"]
        action = d.get("action", "formed")
        if action == "formed":
            stories.append(
                f"NEW FACTION: {d.get('name', '???')} has been formed by "
                f"{d.get('leader', '???')}!\n"
                f"  {random.choice(_STABLE_FLAVOR)}"
            )
        elif action == "disbanded":
            stories.append(
                f"FACTION NEWS: {d.get('name', '???')} has been disbanded.\n"
                f"  {random.choice(_STABLE_FLAVOR)}"
            )

    if not stories:
        stories.append("A quiet week in the wrestling world. No major news to report.")

    return {
        "week": week_number,
        "stories": stories,
        "generated_at": time.time(),
    }


def format_newsletter(issue):
    """Format a newsletter issue for display."""
    if not issue:
        return "No dirt sheet available yet. Check back after the next game week."

    week = issue.get("week", 0)
    stories = issue.get("stories", [])

    header = (
        f"\n|w{'=' * 50}|n\n"
        f"|w  THE DIRT SHEET -- Week {week}|n\n"
        f"|w{'=' * 50}|n\n"
    )

    body = ""
    for story in stories:
        body += f"\n  {story}\n"

    footer = f"\n|w{'=' * 50}|n"

    return header + body + footer


def process_dirtsheet(week_number):
    """
    Called at the end of each EconomyTickScript tick.
    Generates the newsletter from accumulated events, archives the old one.
    """
    script = _get_dirtsheet_script()
    events = script.db.events or []

    # Generate this week's newsletter
    issue = generate_newsletter(week_number, events)

    # Archive the old current issue
    old_issue = script.db.current_issue
    if old_issue:
        archive = script.db.archive or []
        archive.append(old_issue)
        if len(archive) > 20:
            archive = archive[-20:]
        script.db.archive = archive

    # Set new current issue and clear events
    script.db.current_issue = issue
    script.db.events = []
    script.db.week = week_number


class DirtSheetScript(DefaultScript):
    """
    Global script that stores dirt sheet events and newsletter issues.
    Data-only script (no repeating interval).
    """

    def at_script_creation(self):
        self.key = "dirtsheet"
        self.desc = "Dirt Sheet newsletter event store"
        self.persistent = True
        self.interval = 0  # Data store only

        self.db.events = []  # Events accumulated this week
        self.db.current_issue = None  # Current week's newsletter
        self.db.archive = []  # Past issues (max 20)
        self.db.week = 0
