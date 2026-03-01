# Kayfabe: Protect the Business

A professional wrestling territories MUD built on [Evennia 5.0.1](https://www.evennia.com/), designed to run behind a Mystic BBS rlogin bridge. Set in an alternate timeline where all wrestling eras coexist — from backyard VFW hall brawls to headlining Madison Square Garden.

## Overview

Players create wrestlers and climb through a 5-tier career system:

| Tier | Stage | Examples | Level Range |
|------|-------|----------|-------------|
| 1 | Backyard / Small Feds | FHWA, Gulf Coast CW, Garden State Grappling | 1-5 |
| 2 | Training Schools | Pensacola, Slaughterhouse, Beast Works | 5-15 |
| 3 | Regional Territories | Memphis, Mid-South, Mid-Atlantic, WCCW | 15-30 |
| 3.5 | Developmental | OVW, FCW, DSW, HWA | 25-35 |
| 4 | National / International | WWF, WCW, ECW, Japan, UK | 35+ |

## World Stats

- **166 rooms** across 31 territories
- **378 named NPC wrestlers** (renamed homages to real wrestlers)
- **16 NPC managers** (Bobby Haynes, Jimmy Montague, Phil "The Advocate" Eastman, etc.)
- **36+ randomly generated backyard NPCs** per build
- **11 in-game help topics**
- **2 global scripts** (NPC Scheduler, Economy Tick)

## Architecture

```
BBS User -> Mystic BBS (telnet:23) -> rlogin bridge (port 4023) -> Evennia (port 4000)
```

- **Framework**: Evennia 5.0.1 (Python 3.11, Django, Twisted)
- **Data storage**: Evennia AttributeProperty + TraitHandler (no custom Django models)
- **World building**: Python builder scripts (data-driven, version-controlled)
- **Character creation**: EvMenu launched on first puppet
- **Match system**: Script-based state machine (MatchScript)
- **NPC AI**: Ambient actions, promos, challenges via NPCSchedulerScript (5-min tick)
- **Economy**: Weekly tick via EconomyTickScript (30-min tick)

## Game Systems

### Wrestling Matches (Phase-Based)

Not real-time combat — cooperative storytelling with stat checks:

1. **Opening** — Technical exchanges, feeling out
2. **Heat** — Heel takes control, dominates
3. **Hope Spot** — Brief face comeback, gets cut off
4. **Comeback** — Face fires up, crowd goes wild
5. **Finish** — Finisher attempts, near falls, pin

Match quality (0-5 star rating) based on PSY + TEC + crowd heat + match length. Quality affects XP, money, and reputation.

### Six Core Stats

| Stat | Abbrev | Governs |
|------|--------|---------|
| Strength | STR | Power moves, breaking holds |
| Agility | AGI | High-flying, dodging, speed |
| Technical | TEC | Submissions, chain wrestling, counters |
| Charisma | CHA | Promos, crowd connection, merchandise |
| Toughness | TOU | Endurance, kicking out, stamina |
| Psychology | PSY | Match quality, timing, reading opponents |

### Alignment System

- **Face** (Babyface) — The good guy. Higher merch. Best promo: `fire`.
- **Heel** — The villain. More creative freedom. Can cheat, interfere. Best promo: `heat`.
- **Anti-Hero** — The wildcard. Unlocked at Midcarder rank. Can use all tactics without kayfabe penalty. Has a Rebel meter instead of standard kayfabe.

### Kayfabe Score (0-100)

The central mechanic. Tracks how well you protect the business — stay in character, never break the illusion. Random fan encounters during travel test your commitment. High kayfabe = better card positions and promoter trust. Low kayfabe = "boring" chants and roster cuts.

### Career Ranks

Greenhorn -> Jobber -> Enhancement -> Midcarder -> Upper Midcarder -> Main Eventer -> Champion -> Legend

### Manager System

Hire NPC managers for passive bonuses:
- CHA/PSY boosts to promos and match quality
- Heel managers can interfere (referee distraction, weapon pass)
- Manager can cut promos on your behalf (`promo manager`)
- Costs: weekly retainer ($75-$300) + match pay cut (15-25%)

### Economy

- **Match pay**: $5 (backyard) to $200+ (national), multiplied by card position
- **Side jobs**: Security, food, gym trainer, moving crew — risk scheduling conflicts
- **Gear tiers** (1-4): CHA bonus during matches ($100-$8,000)
- **Home gym** (1-4): Training stat bonus ($150-$10,000)
- **Vehicles** (1-4): Travel cost reduction ($200-$15,000)
- **Merchandise**: Passive weekly income at Midcarder+ based on CHA, kayfabe, rank

### Promoter Trust

Hidden per-territory stat (0-100). Determines card position (dark match to main event). Good matches increase trust. Missing shows (from side job conflicts) tanks it. Hit zero = roster cut.

### PvP

- `challenge <player>` — Propose a match
- `team <player>` — Form a tag team
- `betray <partner>` — Turn on your partner (massive crowd heat if timed well)
- `feud` — View active feuds (longer feuds = better blow-off match bonuses)

## Commands

### Wrestling
| Command | Description |
|---------|-------------|
| `wrestle <npc>` | Start a match against an NPC |
| `work` | Execute a wrestling move |
| `sell` | Let opponent hit you (builds match quality) |
| `hope` | Brief comeback attempt during heat segment |
| `comeback` | Fire up! CHA + crowd heat check |
| `finish` | Attempt your finishing move |
| `kickout` | Kick out of a pin |
| `card` | See who's available to wrestle |
| `moves` | List available wrestling moves |

### Promos
| Command | Description |
|---------|-------------|
| `promo fire` | Rally the crowd (Face) |
| `promo heat` | Insult the fans (Heel) |
| `promo challenge` | Call out an opponent |
| `promo shoot` | Break kayfabe (Anti-Hero, risky) |
| `promo manager` | Let your manager speak |

### Career
| Command | Description |
|---------|-------------|
| `stats` | Full character sheet |
| `rank` | Rank progression and career XP |
| `turn <alignment>` | Alignment turn (face/heel/antihero) |
| `titles` | View territory championships |

### Economy
| Command | Description |
|---------|-------------|
| `balance` | Financial status |
| `buy <category>` | Purchase gear, equipment, vehicle |
| `sidejob <type>` | Work a side job |

### Other
| Command | Description |
|---------|-------------|
| `train <stat>` | Train a stat at a gym |
| `travel <territory>` | Travel between territories |
| `hire <manager>` | Hire an NPC manager |
| `fire` | Release your manager |

## File Structure

```
commands/
  chargen.py           # EvMenu character creation (12 nodes)
  wrestling.py         # wrestle, work, sell, comeback, finish, kickout
  promo.py             # promo command (5 types)
  career.py            # stats, rank, turn, titles
  training.py          # train command
  travel.py            # travel between territories
  economy.py           # balance, buy, sidejob
  manager.py           # hire, fire, manager promo, interfere
  pvp.py               # challenge, accept, team, betray, feud
  default_cmdsets.py   # Wires all command sets

typeclasses/
  characters.py        # Wrestler typeclass (TraitHandler stats, alignment)
  rooms.py             # TerritoryRoom, ArenaRoom, GymRoom, etc.
  npcs.py              # NPCWrestler, NPCManager, BackyardNPC
  scripts.py           # MatchScript, NPCSchedulerScript, EconomyTickScript
  exits.py             # TerritoryExit
  accounts.py          # BBS-customized Account (auto-puppet)

world/
  build_world.py       # Master builder script
  territories.py       # Territory data hub (imports sub-modules)
  territories_backyard.py    # 6 Tier 1 backyard feds
  territories_schools.py     # 6 Tier 2 training schools
  territories_regional.py    # 9 Tier 3 regional territories
  territories_developmental.py # 4 Tier 3.5 developmental schools
  territories_national.py   # 5 Tier 4 national/international
  npc_data.py          # ~380 named NPC wrestler + 16 manager definitions
  npc_data_extended.py # Extended NPC roster data
  backyard_npcs.py     # Random NPC generator for Tier 1 feds
  moves.py             # Wrestling move database (30+ moves)
  rules.py             # Game mechanics, stat checks, match quality
  help_entries.py      # 11 in-game help topics

bbs_bridge/
  bridge.py            # rlogin -> Evennia telnet bridge
```

## Deployment

### Prerequisites

- Evennia 5.0.1 installed with Python 3.11 virtualenv
- Live instance at `/opt/evennia/live/`
- Symlinks: `typeclasses/`, `commands/`, `world/` -> this repo

### Build the World

```bash
cd /opt/evennia/live
source ../venv/bin/activate
evennia shell
>>> from world.build_world import build_world; build_world()
```

### Services (systemd)

| Service | Port | Description |
|---------|------|-------------|
| `evennia-live.service` | 4000 | Evennia MUD server |
| `evennia-bridge-live.service` | 4023 | rlogin bridge (BBS -> Evennia) |
| `evennia-dev.service` | 4010 | Dev instance (manual start) |
| `evennia-bridge-dev.service` | 4033 | Dev bridge (manual start) |

### Quick Deploy

```bash
cd /home/tsali/projects/evennia-bbs && git pull
cd /opt/evennia/live && source ../venv/bin/activate && evennia reboot
```

## NPC Roster Highlights

~380 named wrestlers across all territories, each a renamed homage:

- **Territory Era**: Rick Fontaine (Flair), Rusty Roads (Dusty), Hawk Hogan (Hulk), Brett Harmon (Bret Hart)
- **Pensacola Training**: Chief Afa Savea, Roman Savea, "Superfly" Jimmy Snooks
- **OVW Developmental**: The Prototype / Jack Cena, Brock Lester, C.M. Phillips
- **ECW**: "The Sandstorm" Sandy White, Tommy Dreaming, Rob Van Dyke
- **WCW**: "The Scorpion" Steve Borden, Goldburg, Rey Mysterioso
- **WWF Attitude**: Hunter Hearst Hampton, "The Showstopper" Shane Mitchell
- **Women's Division**: Trish Stratos, "The Rebel" Amy Dumas, Bull Nakamura
- **International**: Mitsuhiro Misawa, El Santo Dorado, Tiger Mask Hayashi
- **Original**: Reverend Pain, Rusty Chainz, Dex Rampage, Mama Bear Malone

16 managers including Bobby Haynes (Heenan), Jim Corwin (Cornette), Phil "The Advocate" Eastman (Heyman).

## License

Private. Not for public distribution.
