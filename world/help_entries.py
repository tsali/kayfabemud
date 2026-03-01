"""
Kayfabe: Protect the Business — Help entries.

Creates in-game help topics using Evennia's help system.
Called from build_world.py during world creation.
"""

from evennia.help.models import HelpEntry
from evennia.utils import logger


HELP_ENTRIES = [
    {
        "key": "kayfabe",
        "category": "Game Guide",
        "text": """
|wKAYFABE: PROTECT THE BUSINESS|n

Welcome to Kayfabe — a professional wrestling territories MUD set in an
alternate timeline where all eras coexist.

|cThe Concept|n
You are a professional wrestler climbing through the ranks, from backyard
brawls in VFW halls to headlining Madison Square Garden. Your goal: protect
the business. Stay in character. Put on great matches. Build your legacy.

|cCore Systems|n
  |wWrestling|n  — Phase-based matches (opening, heat, hope, comeback, finish)
  |wPromos|n    — Cut promos to build crowd heat and earn XP
  |wTraining|n  — Train stats at territory gyms
  |wKayfabe|n   — Protect the business (stay in character in public)
  |wEconomy|n   — Earn money from matches, buy gear, work side jobs
  |wManagers|n  — Hire NPC managers for CHA/PSY bonuses
  |wTravel|n    — Move between territories as you climb the ranks
  |wPvP|n       — Challenge other players, form tag teams, betray partners

|cGetting Started|n
After creating your wrestler, you'll start in a small backyard fed.
Win matches and get noticed. A scout will invite you to a training school.
Graduate and head to a regional territory. Eventually, get "The Call" to
the big leagues.

Type |whelp <topic>|n to learn more about any system.
""",
    },
    {
        "key": "stats",
        "category": "Game Guide",
        "text": """
|wSTATS — The Six Core Attributes|n

Every wrestler has six stats that determine their abilities:

  |cStrength (STR)|n  — Power moves, breaking holds, raw force
  |cAgility (AGI)|n   — High-flying, dodging, speed, aerial moves
  |cTechnical (TEC)|n — Submissions, chain wrestling, counters
  |cCharisma (CHA)|n  — Promos, crowd connection, merchandise
  |cToughness (TOU)|n — Endurance, kicking out, stamina, taking bumps
  |cPsychology (PSY)|n — Match quality, timing, reading opponents

|cHow Stats Work|n
Stats start at 5 and can reach 30. Style bonuses are applied at chargen.
You allocate 30 bonus points during character creation.

Stats affect dice checks: d20 + (stat - 10) / 2 vs difficulty.

|cTraining|n
Use |wtrain <stat>|n in gym rooms to improve stats. Each territory gym
gives a bonus to a specific stat. Home gym equipment adds to all training.
Training has diminishing returns at higher stat values.

|cGear Bonuses|n
Better ring gear adds CHA bonus. Better home gym equipment adds to training.
""",
    },
    {
        "key": "ranks",
        "category": "Game Guide",
        "text": """
|wRANK PROGRESSION|n

Your career rank reflects your standing in the wrestling world:

  |xGreenhorn|n       —   0 career XP (just starting out)
  |xJobber|n          — 100 career XP (losing to make others look good)
  |wEnhancement|n     — 300 career XP (competitive losses, occasional wins)
  |cMidcarder|n       — 700 career XP (solid worker, regular TV time)
  |cUpper Midcarder|n — 1500 career XP (title contender, featured feuds)
  |yMain Eventer|n    — 3000 career XP (top of the card, headline shows)
  |YChampion|n        — 6000 career XP (title holder, industry legend)
  |RLegend|n          — 12000 career XP (all-time great, Hall of Fame)

Career XP = (wins * 20) + accumulated XP from matches and promos.

|cCommands|n
  |wrank|n  — View your rank progression and career XP
  |wstats|n — View your full character sheet
""",
    },
    {
        "key": "wrestling",
        "category": "Game Guide",
        "text": """
|wWRESTLING MATCHES|n

Matches are phase-based cooperative storytelling with stat checks.

|cMatch Phases|n
  1. |wOpening|n    — Technical exchanges, feeling out the opponent
  2. |rHeat|n       — The heel takes control, works over the face
  3. |yHope Spot|n  — Brief comeback attempt, gets cut off
  4. |gComeback|n   — The face fires up, crowd goes wild
  5. |wFinish|n     — Both wrestlers throw everything, someone goes down

|cMatch Commands|n
  |wwork|n      — Execute a wrestling move (attack)
  |wsell|n      — Let your opponent hit you (builds match quality)
  |whope|n      — Brief comeback attempt during heat segment
  |wcomeback|n  — Fire up! CHA + crowd heat check
  |wfinish|n    — Attempt your finishing move
  |wkickout|n   — Kick out of a pin attempt

|cMatch Quality|n
Star ratings (0-5 stars) are based on both wrestlers' PSY + TEC +
crowd heat + match length. Higher star ratings = more XP and money.

|cStarting a Match|n
  |wwrestle <npc>|n    — Challenge an NPC wrestler
  |wchallenge <player>|n — Challenge another player (PvP)
  |wcard|n             — See who's available to wrestle
""",
    },
    {
        "key": "promos",
        "category": "Game Guide",
        "text": """
|wPROMO SYSTEM|n

Promos are how you build heat and connect with the crowd.

|cPromo Types|n
  |wpromo fire|n      — Rally the crowd (Face preferred)
  |wpromo heat|n      — Insult the fans (Heel preferred)
  |wpromo challenge|n — Call out an opponent (any alignment)
  |wpromo shoot|n     — Break kayfabe, speak truth (Anti-Hero, risky)
  |wpromo manager|n   — Let your manager speak for you

|cHow It Works|n
Promos use CHA + PSY stat checks. Using the promo type that matches your
alignment gives a +3 bonus. Using the wrong type gives a penalty and
may cost kayfabe.

|cRewards|n
  Great promo (margin 10+): 25 XP, +3 kayfabe
  Good promo (success):     15 XP, +1 kayfabe
  Decent promo (marginal):   8 XP
  Bombed (failure):          3 XP, -1 kayfabe

|cManager Promos|n
If you have a manager, |wpromo manager|n uses their CHA instead of yours.
Great for wrestlers with low CHA who hire silver-tongued managers.
""",
    },
    {
        "key": "economy",
        "category": "Game Guide",
        "text": """
|wECONOMY|n

Money is earned from matches and side jobs, spent on gear and travel.

|cMatch Pay|n (base by tier)
  Tier 1 (Backyard): $5  |  Tier 2 (Training): $15
  Tier 3 (Regional): $50 |  Tier 3.5 (Developmental): $75
  Tier 4 (National): $200
Pay is multiplied by card position (dark 0.25x to main event 2.5x)
and increased by star rating.

|cSide Jobs|n (|wsidejob|n command)
  Security ($20-40, +TOU, 15% conflict risk)
  Food ($10-25, safe, 10% conflict risk)
  Gym trainer ($25-45, +STR, 15% conflict risk)
  Moving crew ($30-55, +TOU, 20% conflict risk)
Warning: conflicts can make you miss shows, tanking promoter trust.

|cPurchases|n (|wbuy|n command)
  Gear (tiers 1-4): CHA bonus during matches
  Home gym (tiers 1-4): training stat bonus
  Vehicle (tiers 1-4): travel cost reduction

|cMerchandise|n
At Midcarder rank+, you earn passive weekly merch income based on
CHA, kayfabe score, rank, and gear tier.

|cCommands|n
  |wbalance|n  — Check your finances
  |wbuy|n      — Purchase gear, equipment, vehicles
  |wsidejob|n  — Work a side job
""",
    },
    {
        "key": "territories",
        "category": "Game Guide",
        "text": """
|wTERRITORIES|n

The wrestling world is divided into territories across four tiers.

|cTier 1 — Backyard Feds|n (Starting point)
  FHWA, GCCW, GSG, BBA, LSU, PSC
  Tiny operations — VFW halls, backyards, county fairgrounds.
  Win matches and get noticed by a scout.

|cTier 2 — Training Schools|n
  Pensacola, Slaughterhouse, Beast Works, Conservatory,
  Dungeon of Holds, Proving Grounds
  Learn fundamentals. Build stats. Earn your diploma.

|cTier 3 — Regional Territories|n
  Memphis, Mid-South, Mid-Atlantic, Florida, Georgia,
  World Class, AWA, Stampede, Pacific NW
  Crowd work, gimmicks, promos, territory titles.

|cTier 3.5 — Developmental|n (Optional but recommended)
  OVW, FCW, DSW, HWA
  Camera work, mic polish, ring presence. Grants permanent
  CHA+2 and PSY+2 bonuses you can't get elsewhere.

|cTier 4 — National / International|n
  WWF, WCW, ECW, UK, Japan
  Main events, world championships, legend status.

|cTravel|n
  |wtravel|n — See available destinations and costs
  |wtravel <territory>|n — Travel to a territory
""",
    },
    {
        "key": "managers",
        "category": "Game Guide",
        "text": """
|wMANAGER SYSTEM|n

NPC managers can be hired to boost your career.

|cBonuses|n
  CHA boost — Manager's CHA adds partial bonus to promo checks
  PSY boost — Manager's PSY adds partial bonus to match quality
  Interference — Heel managers can distract the referee
  Promo delegation — Manager cuts promos on your behalf

|cCosts|n
  Retainer: Weekly fee ($50-$300 depending on manager)
  Match cut: 15-25% of your match payoff goes to the manager
  If you can't afford the retainer, the manager drops you.

|cCommands|n
  |whire <manager>|n     — Hire an available manager
  |wfire|n               — Release your current manager
  |wpromo manager|n      — Manager cuts a promo for you
  |winterfere|n          — Signal manager to interfere (heel, risk of DQ)

|cAlignment Restrictions|n
  Some managers only work with heels, some with faces.
  Anti-Heroes can hire any manager.
  One manager at a time per wrestler.
""",
    },
    {
        "key": "alignment",
        "category": "Game Guide",
        "text": """
|wALIGNMENT — Face / Heel / Anti-Hero|n

Your alignment defines your character's role in wrestling stories.

|gFace (Babyface)|n
  The good guy. Crowd cheers you. Higher merchandise sales.
  Best promo type: |wfire|n
  Cannot use dirty tactics without kayfabe penalty.

|rHeel|n
  The villain. Crowd boos you (that's the goal).
  Best promo type: |wheat|n
  Can use foreign objects, low blows, manager interference.
  Less merch, but more creative freedom.

|yAnti-Hero|n
  The wildcard. Play by your own rules.
  Unlocked at |cMidcarder|n rank — use |wturn antihero|n.
  Can use both face and heel promo styles.
  Dirty tactics without kayfabe penalty.
  Has a Rebel meter instead of standard kayfabe.

|cAlignment Turns|n
  |wturn face|n     — Become a babyface
  |wturn heel|n     — Become a villain
  |wturn antihero|n — Go rogue (requires Midcarder rank)
  Good turns generate massive crowd heat. Bad turns tank momentum.

|cKayfabe Score|n (0-100, starts at 50)
  70+: Promoters trust you, better card spots, fans believe
  30-: Promoters see you as unreliable, fans chant "boring"
  Random fan encounters test your commitment to character.
""",
    },
    {
        "key": "pvp",
        "category": "Game Guide",
        "text": """
|wPLAYER vs PLAYER|n

Real players can wrestle each other, form teams, and betray partners.

|cCommands|n
  |wchallenge <player>|n — Propose a match against another player
  |waccept|n             — Accept a pending challenge
  |wteam <player>|n      — Propose forming a tag team
  |wbetray <partner>|n   — Turn on your partner (massive crowd heat)
  |wfeud|n               — View your current feuds

|cTag Teams|n
  Tag teams share reputation bonuses and can enter tag matches.
  Choose your own tag team name. Combine finishers for a tag finisher.

|cBetrayals|n
  Turning on a partner generates MASSIVE crowd heat if timed well.
  The betrayed partner gets a sympathy pop (crowd support boost).
  Poorly timed betrayals tank both wrestlers' reputations.

|cFeuds|n
  Player feuds develop through challenges, promos, and betrayals.
  Longer, better-built feuds produce higher match quality bonuses.
  Blow-off matches (the final match) get bonus star ratings.
""",
    },
    {
        "key": "training",
        "category": "Game Guide",
        "text": """
|wTRAINING|n

Train your stats at gym rooms to improve your wrestler.

|cUsage|n
  |wtrain <stat>|n — Train a stat (str, agi, tec, cha, tou, psy)

|cGym Bonuses|n
Each territory gym gives a bonus to a specific stat:
  Memphis: CHA       Mid-South: STR      Mid-Atlantic: TEC
  Florida: TOU       Georgia: CHA        World Class: AGI
  AWA: TEC           Stampede: TOU       Pacific NW: PSY
  OVW: CHA           FCW: PSY            DSW: TOU
  HWA: CHA           WWF: CHA            WCW: AGI
  ECW: TOU           UK: TEC             Japan: TEC

|cDiminishing Returns|n
Training is easier at low stat values and gets harder as stats increase.
Base chance: ~90% at stat 5, drops to ~30% at stat 20.

|cHome Gym|n
Buy home gym equipment (|wbuy equipment|n) for an additional training
bonus that applies everywhere.
""",
    },
]


def create_help_entries():
    """Create all in-game help entries. Safe to call multiple times."""
    created = 0
    updated = 0

    for entry_data in HELP_ENTRIES:
        existing = HelpEntry.objects.filter(db_key=entry_data["key"])
        if existing.exists():
            obj = existing[0]
            obj.db_help_category = entry_data["category"]
            obj.db_entrytext = entry_data["text"].strip()
            obj.save()
            updated += 1
        else:
            HelpEntry.objects.create(
                db_key=entry_data["key"],
                db_help_category=entry_data["category"],
                db_entrytext=entry_data["text"].strip(),
            )
            created += 1

    logger.log_info(
        f"    Help entries: {created} created, {updated} updated"
    )
