# Kayfabe: Protect the Business

A professional wrestling territories MUD built on [Evennia 5.0.1](https://www.evennia.com/), designed to run behind a Mystic BBS rlogin bridge. Set in an alternate timeline where all wrestling eras coexist — from backyard VFW hall brawls to headlining Madison Square Garden.

**Play now on BBS PEPSICOLA:**
- Telnet: `bbs.cultofjames.org` port `2023`
- TLS: `bbs.cultofjames.org` port `992`
- From the BBS main menu, press **D** for Doors, then **K** for Kayfabe

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
- **381 named NPC wrestlers** (renamed homages to real wrestlers + 1 real person with permission)
- **17 NPC managers**
- **36+ randomly generated backyard NPCs** per build
- **11 in-game help topics**
- **3 global scripts** (NPC Scheduler, Economy Tick, Fatigue)
- **Multi-character support** (up to 10 wrestlers per account)

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
- **Bridge**: Custom asyncio rlogin bridge with line buffering, bridge-side echo, IAC negotiation, ANSI-aware word wrap, UTF-8 to ASCII transliteration

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

### Lodging System

- **Inns**: Territory-specific lodging (Tier 1-4), rest clears fatigue + stat bonuses
- **Player Houses**: Buy a house in any territory ($500-$15,000)
- **House Upgrades**: Home Gym, Practice Ring, Trophy Case, Hot Tub, Party Deck
- **Message Boards**: Post/read messages at inns and houses
- **`gohome`**: Teleport to your house from anywhere

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
| `work` | Execute a wrestling move (your offense) |
| `sell` | Let opponent hit you (builds match quality) |
| `hope` | Brief comeback attempt during heat segment |
| `comeback` | Fire up! CHA + crowd heat check |
| `finish` | Attempt your finishing move |
| `kickout` | Kick out of a pin attempt |
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

### Lodging
| Command | Description |
|---------|-------------|
| `rest` | Rest at inn or house (clears fatigue) |
| `board` | Read message board |
| `post <msg>` | Post to message board |
| `buyhouse` | Purchase a house in current territory |
| `gohome` | Teleport to your house |
| `upgrade` | Buy house upgrades |

### Character Management
| Command | Description |
|---------|-------------|
| `charselect` | List and switch between your wrestlers |
| `charcreate` | Create a new wrestler (up to 10) |

### Other
| Command | Description |
|---------|-------------|
| `train <stat>` | Train a stat at a gym |
| `travel <territory>` | Travel between territories |
| `hire <manager>` | Hire an NPC manager |
| `fire` | Release your manager |
| `brawl <target>` | Start a backstage brawl |

## File Structure

```
commands/
  chargen.py           # EvMenu character creation (12 nodes)
  charselect.py        # Character selection/creation (multi-char support)
  command.py           # Base command class (prompt, no-match, no-input handlers)
  wrestling.py         # wrestle, work, sell, comeback, finish, kickout
  promo.py             # promo command (5 types)
  career.py            # stats, rank, turn, titles
  training.py          # train command
  travel.py            # travel between territories
  economy.py           # balance, buy, sidejob
  manager.py           # hire, fire, manager promo, interfere
  pvp.py               # challenge, accept, team, betray, feud
  lodging.py           # rest, board, post, buyhouse, gohome, upgrade
  brawl.py             # backstage brawl command
  default_cmdsets.py   # Wires all command sets

typeclasses/
  characters.py        # Wrestler typeclass (TraitHandler stats, alignment)
  rooms.py             # TerritoryRoom, ArenaRoom, GymRoom, InnRoom, PlayerHouse, etc.
  npcs.py              # NPCWrestler, NPCManager, BackyardNPC
  scripts.py           # MatchScript, NPCSchedulerScript, EconomyTickScript
  exits.py             # Exit with destination preview on look
  accounts.py          # BBS-customized Account (auto-puppet, multi-char)
  objects.py           # ObjectParent base

world/
  build_world.py       # Master builder script
  territories.py       # Territory data hub (imports sub-modules)
  territories_backyard.py    # 6 Tier 1 backyard feds
  territories_schools.py     # 6 Tier 2 training schools
  territories_regional.py    # 9 Tier 3 regional territories
  territories_developmental.py # 4 Tier 3.5 developmental schools
  territories_national.py   # 5 Tier 4 national/international
  npc_data.py          # 381 named NPC wrestler + 17 manager definitions
  npc_data_extended.py # Extended NPC roster data
  backyard_npcs.py     # Random NPC generator for Tier 1 feds
  moves.py             # Wrestling move database (30+ moves)
  rules.py             # Game mechanics, stat checks, match quality
  help_entries.py      # 11 in-game help topics

bbs_bridge/
  bridge.py            # rlogin -> Evennia telnet bridge (asyncio)
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

---

## Territories & Rosters

30 territories, 194 rooms, 381 named wrestlers, 17 managers, and 36+ randomly generated backyard NPCs.

---

### Tier 1 — Backyard Feds

Small-time operations in VFW halls, backyards, and converted buildings. $5 admission, folding chairs, and dreams. Each has 5 rooms: parking lot, venue, locker room, motel, and travel hub. NPCs are randomly generated on each world build — a rotating cast of local talent with colorful gimmicks.

#### Gulf Coast Championship Wrestling (GCCW) — Pensacola, FL

A gutted auto body shop with a regulation ring donated by the Savea family. Sandy gravel lot, industrial fans pushing Gulf humidity around. VHS camcorder on a tripod records every show — these tapes sometimes find the right people. *Randomly generated NPCs.*

#### Federal Hills Wrestling Alliance (FHWA) — Shepherdsville, KY

A VFW hall off the highway with a gravel parking lot and a hand-painted sign. 40-person capacity, metal bleachers, and a ring that's seen better decades. The crowd knows their wrestling though. *Randomly generated NPCs.*

#### Garden State Grappling (GSG) — Vineland, NJ

A strip mall storefront converted into a wrestling venue. The Jersey crowd are smart marks who will chant "boring" if you don't bring it. Word is a WWF scout has been seen in the area. *Randomly generated NPCs.*

#### Bayou Brawling Alliance (BBA) — Shreveport, LA

A muddy field behind a tin-roofed barn. Hay bale seating, pickup trucks parked ring-side, and mosquitoes the size of small birds. What it lacks in polish it makes up for in violence. *Randomly generated NPCs.*

#### Lone Star Underground (LSU) — Fort Worth, TX

A stockyard arena in a converted livestock auction barn. No rules, no script, and the crowd throws beer cans when they're happy. Texas-sized everything — including the bumps. *Randomly generated NPCs.*

#### Peach State Championship (PSC) — Macon, GA

An American Legion hall with $5 admission and boiled peanuts at the concession stand. Close enough to Atlanta that TBS cameras might wander by someday. The Georgia heat is free. *Randomly generated NPCs.*

---

### Tier 2 — Training Schools

Where wrestlers learn the craft. Each school has a head trainer with a distinct philosophy. 5-10 rooms including training floor, ring, motel, and travel hub.

#### Pensacola Wrestling School (Samoan Training Grounds) — Pensacola, FL

Chief Afa and Sika Savea's compound on the beach. "NO WEAKLINGS" painted on the gym wall. The Anoa'i bloodline trains here — Samoan Drop is the first move you learn, and the last one you forget. 10 rooms, 20 named NPCs.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Chief Afa Savea | Afa Anoa'i | Trainer | Face | 40 | Samoan Drop |
| Chief Sika Savea | Sika Anoa'i | Trainer | Face | 40 | Samoan Drop |
| Master Matsuda | Hiro Matsuda | Trainer | Heel | 40 | Leg Break |
| High Chief Pita Maivia | Peter Maivia | Trainer | Face | 35 | Headbutt |
| "Superfly" Jimmy Snooks | Jimmy Snuka | Wrestler | Face | 30 | Superfly Splash |
| Brutus "The Blade" Beefsteak | Brutus Beefcake | Wrestler | Face | 22 | Sleeper |
| Luna Vasquez | Luna Vachon | Wrestler | Heel | 20 | Moonsault |
| "The Savage" Eddo Fatu | Umaga | Wrestler | Heel | 22 | Samoan Spike |
| "The Mountain" Tua Savea | Yokozuna | Wrestler | Heel | 20 | Banzai Drop |
| "Big Sola" Fatu | Rikishi | Wrestler | Face | 18 | Stinkface |
| Samu Savea | Samu | Wrestler | Heel | 18 | Diving Headbutt |
| Gene "The Machine" Snitzky | Gene Snitsky | Wrestler | Heel | 16 | Pumphandle Slam |
| Roman Savea | Roman Reigns | Wrestler | Face | 15 | Spear |
| Jay & Jimmy Fatu | The Usos | Wrestler | Face | 15 | Superkick |
| "The Kid" Billy Kidwell | Billy Kidman | Wrestler | Face | 15 | Shooting Star Press |
| Malia Hoskins | Tamina Snuka | Wrestler | Heel | 14 | Superfly Splash |
| Nia Fane | Nia Jax | Wrestler | Heel | 14 | Leg Drop |
| Solo Savea | Solo Sikoa | Wrestler | Heel | 12 | Samoan Spike |
| "Coconut" Jimmy Snooks Jr. | Jimmy Snuka Jr. | Wrestler | Face | 12 | Superfly Splash |
| "Samoan Storm" Manu Savea | Manu | Wrestler | Face | 10 | Samoan Drop |

#### Viktor Kovalenko's Slaughterhouse — North Andover, MA

A freezing New England warehouse where Viktor Kovalenko (Killer Kowalski) breaks you down and builds you back. Brutal strength training. Many quit. The ones who survive are ready for anything. 6 rooms.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Viktor Kovalenko | Killer Kowalski | Trainer | Heel | 40 | Kowalski Claw |

#### Beast Works Academy — Westville, NJ

Larry Sharpton (Larry Sharpe) runs a power wrestler factory that feeds directly into the WWF and Mid-Atlantic territories. If you can't slam, you can't stay. 5 rooms.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Larry Sharpton | Larry Sharpe | Trainer | Face | 35 | Boston Crab |

#### The Funking Conservatory — Ocala, FL

Dory Funk Sr.'s horse ranch turned wrestling academy. Technical chain wrestling is the curriculum. You learn to work a hold before you learn to throw a punch. 5 rooms.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Dory Funk Sr. | Dory Funk Jr. | Trainer | Face | 40 | Spinning Toe Hold |

#### The Dungeon of Holds — Tampa, FL

Boris Malenko's basement. Catch wrestling, submission focus, and an old man who can still stretch anyone in the room. The most technically demanding school in the game. 5 rooms.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Boris Malenko | Boris Malenko | Trainer | Heel | 40 | Russian Legsweep |

#### The Proving Grounds — Eldon, MO

Harley Race's ranch. NWA all-rounder style — you learn to do everything because a champion has to. Psychology emphasis: if the crowd doesn't care, neither does Harley. 5 rooms. *Randomly generated NPCs.*

---

### Tier 3 — Regional Territories

The real business. TV deals, arena shows, and promoters who control your career. 6-8 rooms including arena, backstage, gym, bar, promoter's office, hotel, and travel hub.

#### Memphis Championship Wrestling — Memphis, TN

Mid-South Coliseum. The promo capital of wrestling — if you can't talk, you can't work Memphis. Beale Street bars, late-night studio tapings, and Jerry Crowley sitting on a throne daring you to take it. 8 rooms.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Jerry Crowley | Jerry Lawler | Wrestler | Anti-Hero | 35 | Piledriver |
| Bill Brisbane | Bill Dundee | Wrestler | Heel | 28 | Diving Headbutt |
| Jimmy Gallant | Jimmy Valiant | Wrestler | Face | 25 | Elbow Drop |
| Jacqueline Morrow | Jacqueline | Wrestler | Face | 25 | DDT |
| Mama Bear Malone | original | Wrestler | Anti-Hero | 25 | Bear Hug Slam |
| Gary Young | Gary Young | Wrestler | Heel | 20 | Kingmaker |
| Tom Pritchard | Tom Prichard | Wrestler | Heel | 22 | Kingmaker |
| Andy Coughlin | Andy Kaufman | Wrestler | Heel | 10 | Slap |
| Lance Rosemont | Lance Russell | Announcer | Face | 1 | — |

#### Mid-South Wrestling — Shreveport, LA

Hirsch Memorial Coliseum. Bill Watts runs this territory with an iron fist — no top-rope moves, no nonsense. Stiff workers, legit tough guys, and the best tag team division in the country. 7 rooms.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Harley Reece | Harley Race | Wrestler | Heel | 38 | Diving Headbutt |
| "Billion Dollar Man" Ted DiMarco | Ted DiBiase | Wrestler | Heel | 37 | Million Dollar Dream |
| "Dr. Damage" Stan Williamson | Dr. Death Steve Williams | Wrestler | Face | 35 | Oklahoma Stampede |
| Salvage Yard Hound | Junkyard Dog | Wrestler | Face | 33 | Thump |
| "Mr. Magnificent" Paul Orndoff | Paul Orndorff | Wrestler | Heel | 32 | Piledriver |
| Buzzsaw Jim Dugan | Hacksaw Jim Duggan | Wrestler | Face | 30 | Three-Point Clothesline |
| "Iron" Mike Rotunda | Mike Rotundo | Wrestler | Heel | 30 | Airplane Spin |
| Bobby Eaton Jr. | Bobby Eaton | Wrestler | Heel | 30 | Rocket Launcher |
| Stan Lake | Stan Lane | Wrestler | Heel | 28 | Rocket Launcher |
| Ricky Gibson | Ricky Morton | Wrestler | Face | 28 | Double Dropkick |
| Robert Fulton | Robert Gibson | Wrestler | Face | 26 | Double Dropkick |
| Reverend Pain | original | Wrestler | Heel | 25 | Last Rites |
| The Butcher King | original | Wrestler | Heel | 25 | Meat Hook |
| Rusty Chainz | original | Wrestler | Anti-Hero | 22 | Chain Reaction |
| Backwoods Beauregard | original | Wrestler | Face | 20 | Gator Splash |
| Tex Slazenger | Tex Slazenger | Wrestler | Heel | 18 | Texas Stampede |
| Shanghai Pierce | Shanghai Pierce | Wrestler | Heel | 18 | Texas Stampede |
| Jim Roth | Jim Ross | Announcer | Face | 1 | — |

#### Mid-Atlantic Championship Wrestling — Charlotte, NC

Greensboro Coliseum. The NWA world title lives here. Rick Fontaine struts through the arena like he owns the place — because he does. Technical wrestling, blood feuds, and 60-minute broadways. 8 rooms.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Rick Fontaine | Ric Flair | Wrestler | Heel | 40 | Figure-Four Leglock |
| Ricky Riverdale | Ricky Steamboat | Wrestler | Face | 38 | Deep Body Press |
| Beastly & Havok | Road Warriors | Wrestler | Anti-Hero | 38 | Doomsday Device |
| Art Alderson | Arn Anderson | Wrestler | Heel | 35 | Spinebuster |
| Art Alderson (Tag) | Arn Anderson (Enforcers) | Wrestler | Heel | 35 | Spike Piledriver |
| Lex Lugar | Lex Luger | Wrestler | Face | 34 | Torture Rack |
| Tyler Blanford | Tully Blanchard | Wrestler | Heel | 33 | Slingshot Suplex |
| Magnus T.A. | Magnum T.A. | Wrestler | Face | 33 | Belly-to-Belly Suplex |
| Chief Thunderhawk | Wahoo McDaniel | Wrestler | Face | 32 | Tomahawk Chop |
| Hawk Ellering | Hawk (Road Warriors) | Wrestler | Anti-Hero | 32 | Doomsday Device |
| Animal Ellering | Animal (Road Warriors) | Wrestler | Anti-Hero | 32 | Doomsday Device |
| Larry Zablonski (Tag) | Larry Zbyszko (Enforcers) | Wrestler | Heel | 30 | Spike Piledriver |
| Sergeant Steele | original | Wrestler | Heel | 22 | Court Martial |
| Rip Morgan | Rip Morgan | Wrestler | Heel | 16 | Vertical Suplex |
| George Southard | George South | Wrestler | Heel | 14 | Slam |
| Italian Stallion | Italian Stallion | Wrestler | Face | 14 | Dropkick |

#### World Class Championship Wrestling (WCCW) — Dallas, TX

The Sportatorium. The Von Adler family dynasty — three brothers carrying the territory on their backs against the Freebirds. Texas heat, Texas crowds, and Texas-sized grudge matches. 7 rooms.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Terry Bronco | Terry Funk | Wrestler | Anti-Hero | 38 | Spinning Toe Hold |
| Kerry Von Adler | Kerry Von Erich | Wrestler | Face | 36 | Iron Claw |
| Kevin Von Adler | Kevin Von Erich | Wrestler | Face | 35 | Tornado Punch |
| Terry "Boom Boom" Gordon | Terry Gordy | Wrestler | Heel | 35 | Powerbomb |
| Mitchell "PS" Hale | Michael Hayes | Wrestler | Heel | 33 | DDT |
| David Von Adler | David Von Erich | Wrestler | Face | 30 | Iron Claw |
| Chris Adkins | Chris Adams | Wrestler | Heel | 30 | Superkick |
| Buddy Robards | Buddy Roberts | Wrestler | Heel | 28 | Eye Rake |

#### American Wrestling Association (AWA) — Minneapolis, MN

Minneapolis Auditorium. Vernon Gavin built this territory on legitimacy — real athletes, real competition, real wrestling. The old guard resists change, but the talent keeps coming. 8 rooms.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Vernon Gavin | Verne Gagne | Wrestler | Face | 38 | Sleeper Hold |
| Nick Buckminster | Nick Bockwinkel | Wrestler | Heel | 36 | Piledriver |
| Kurt Hennison | Curt Hennig | Wrestler | Heel | 36 | Perfectplex |
| "Ravishing" Rick Rood | Rick Rude | Wrestler | Heel | 34 | Rude Awakening |
| The Grinder | The Crusher | Wrestler | Face | 30 | Bolo Punch |
| Rabid Dog Vachon | Mad Dog Vachon | Wrestler | Heel | 30 | Biting |
| Larry Zablonski | Larry Zbyszko | Wrestler | Heel | 30 | Swinging Neckbreaker |
| "Iron Horse" Pete Buckley | original | Wrestler | Face | 28 | Iron Horse Lariat |
| Tom Zenk | Tom Zenk | Wrestler | Face | 22 | Superkick |
| Col. DeBeers | Col. DeBeers | Wrestler | Heel | 22 | Armbar |
| Dakota Hollis | original | Wrestler | Face | 22 | Hollis Hold |
| Gorgeous Gary Grand | original | Wrestler | Heel | 22 | Grand Finale |
| Pat Tanaka | Pat Tanaka | Wrestler | Face | 20 | Savate Kick |
| Paul Diamante | Paul Diamond | Wrestler | Face | 20 | German Suplex |
| Mike Enos | Mike Enos | Wrestler | Heel | 18 | Powerslam |
| Wayne Bloom | Wayne Bloom | Wrestler | Heel | 18 | Big Boot |
| Boris Zhukov | Boris Zhukov | Wrestler | Heel | 16 | Russian Headbutt |

#### Stampede Wrestling — Calgary, AB, Canada

Victoria Pavilion. The Harmon family dungeon produces the toughest workers in the business. Stuart Harmon stretches you in the basement until you either tap or earn your spot. Calgary winters build character. 6 rooms.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Brett Harmon | Bret Hart | Wrestler | Face | 42 | Sharpshooter |
| Stuart Harmon | Stu Hart | Trainer | Face | 40 | Stretching |
| Oliver Harmon | Owen Hart | Wrestler | Heel | 35 | Enziguiri |
| Davey Bull Smythe | British Bulldog | Wrestler | Face | 34 | Running Powerslam |
| Dynamo Keith | Dynamite Kid | Wrestler | Heel | 33 | Diving Headbutt |
| Jim "The Anvil" Niedhardt | Jim Neidhart | Wrestler | Heel | 28 | Hart Attack |
| Jacques Roget | Jacques Rougeau | Wrestler | Heel | 25 | Bombe de Roget |
| Raymond Roget | Raymond Rougeau | Wrestler | Heel | 24 | Bombe de Roget |
| Davey Richardson | Davey Boy Smith Jr. | Wrestler | Face | 22 | Running Powerslam |
| Rex Niedhardt | fictional Neidhart | Wrestler | Heel | 18 | Double Powerslam |
| Anvil Niedhardt Jr. | fictional Neidhart | Wrestler | Heel | 16 | Double Powerslam |

#### Georgia Championship Wrestling (GCW) — Atlanta, GA

The Omni. The only regional territory with national TV on TBS. Gordon Stoley calls the action with a voice like bourbon and wisdom. Getting on Georgia TV can change your career overnight. 7 rooms.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Tommy Richmond | Tommy Rich | Wrestler | Face | 28 | Thesz Press |
| Iceberg Jackson | original | Wrestler | Heel | 25 | Glacier Slam |
| The Phantom Rider | original | Wrestler | Anti-Hero | 25 | Ghost Driver |
| Gordon Stoley | Gordon Solie | Announcer | Face | 1 | — |

#### Championship Wrestling from Florida — Tampa, FL

Tampa Armory. Stiff workers and Florida humidity. Rusty Roads is the common man's champion — he bleeds, he sweats, and the fans love him for it. A proving ground for NWA hopefuls. 7 rooms.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Rusty Roads | Dusty Rhodes | Wrestler | Face | 38 | Bionic Elbow |
| Barry Wyndham | Barry Windham | Wrestler | Face | 34 | Superplex |
| "Megastar" Billy Grayham | Superstar Billy Graham | Wrestler | Heel | 33 | Bear Hug |
| Keith Solomon | Kevin Sullivan | Wrestler | Heel | 30 | Double Stomp |
| Wildcat Willie | original | Wrestler | Face | 22 | Wildcat Claw |

#### Pacific Northwest Wrestling (PNW) — Portland, OR

Portland Sports Arena. A worker's territory where in-ring ability matters more than gimmicks. The Pacific Northwest crowd is quiet until you earn their respect — then they're yours for life. 7 rooms.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Roddy Viper | Roddy Piper | Wrestler | Heel | 38 | Sleeper Hold |
| Ladykiller Buddy Bloom | Buddy Rose | Wrestler | Heel | 28 | DDT |
| Typhoon Sato | original | Wrestler | Face | 25 | Tidal Wave |

---

### Tier 3.5 — Developmental Territories

The last stop before the big leagues. TV tapings every week, smaller arenas (250-400 capacity), and scouts watching every match. Get called up or get cut.

#### Ohio Valley Wrestling (OVW) — Louisville, KY

Davis Arena, a converted warehouse in Louisville. Jim Corwin watches from backstage with a tennis racket and strong opinions. VHS tape study sessions, promos graded on a curve, and the phone call that changes everything. The pipeline to WWF. 8 rooms, 22 named NPCs.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| "Nightmare" Danny Dusk | Danny Davis | Authority | Face | 30 | — |
| Al Frost | Al Snow | Wrestler | Face | 28 | Snow Plow |
| Brock Lester | Brock Lesnar | Wrestler | Heel | 22 | F-5 |
| Simon Deen | Nova | Trainer | Face | 22 | Kryptonite Krunch |
| The Prototype | John Cena | Wrestler | Face | 20 | FU |
| C.M. Phillips | CM Punk | Wrestler | Anti-Hero | 20 | GTS |
| Leviathan | Batista | Wrestler | Heel | 18 | Bautiste Bomb |
| Randy Viper | Randy Orton | Wrestler | Heel | 18 | RKO |
| Sheldon Banks | Shelton Benjamin | Wrestler | Face | 18 | T-Bone Suplex |
| Bobby Lash | Bobby Lashley | Wrestler | Face | 18 | Dominator |
| Beth Fenix | Beth Phoenix | Wrestler | Face | 18 | Glam Slam |
| Mike Kennedy | Mr. Kennedy | Wrestler | Heel | 16 | Green Bay Plunge |
| Cody Rhoades | Cody Rhodes | Wrestler | Face | 16 | Cross Rhodes |
| Kofi Kingsley | Kofi Kingston | Wrestler | Face | 16 | Trouble in Paradise |
| Nick Nemeth | Dolph Ziggler | Wrestler | Heel | 16 | Zig Zag |
| Mike Mizanin | The Miz | Wrestler | Heel | 16 | Skull Crushing Finale |
| Mickie Jameson | Mickie James | Wrestler | Face | 16 | Mickie-DT |
| **"The East End Villain" Josh Ashcraft** | **Josh Ashcraft** | **Announcer** | **Heel** | **16** | **F-5** |
| Ted DiBrasi Jr. | Ted DiBiase Jr | Wrestler | Heel | 14 | Dream Street |
| Nick Dunsmore | Eugene | Wrestler | Face | 14 | Stunner |
| Rico Constantine | Rico | Wrestler | Heel | 14 | Spin Kick |
| Jim Corwin | Jim Cornette | Authority | Heel | 1 | Tennis Racket |

> **Note**: "The East End Villain" Josh Ashcraft is used with permission. He is a real wrestler, manager, and color commentator at OVW 1:1 in Louisville, KY. In-game he serves as color commentator (announcer) at Davis Arena AND is available as an Anti-Hero manager who will manage anyone to greatness. 15+ years in OVW across refereeing, managing (Legacy of Brutality stable), wrestling, and commentary.

#### Florida Championship Wrestling (FCW) — Tampa, FL

Production truck parked outside a strip mall arena. Monday night tapings, ring psychology drills, and a roster hungry to prove they belong. The modern developmental model — TV-ready or go home. 6 rooms.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| "Iron Steve" Keirn | Steve Keirn | Trainer | Face | 30 | — |
| Seth Blackburn | Seth Rollins | Wrestler | Face | 18 | Blackout |
| Dean Amberson | Dean Ambrose | Wrestler | Anti-Hero | 18 | Dirty Deeds |
| Bray Rotunda | Bray Wyatt | Wrestler | Heel | 18 | Sister Abigail |
| Naomi Fatu | Naomi | Wrestler | Face | 14 | Rear View |

#### Deep South Wrestling (DSW) — McDonough, GA

A warehouse with no AC where "Sergeant" Bill DeMott runs boot camp. Physical toughness is the only curriculum. If you can survive the Georgia heat and DeMott's drills, you can survive anything. 6 rooms.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| "Big Red" Knox | Kane | Trainer | Anti-Hero | 35 | Chokeslam |
| "Sergeant" Bill DeMott | Bill DeMott | Trainer | Heel | 28 | No Laughing Matter |
| Bobby Lash Jr. | Bobby Lashley (DSW) | Wrestler | Face | 16 | Dominator |
| Cody Rhoades Jr. | Cody Rhodes (DSW) | Wrestler | Face | 14 | Cross Rhodes |

#### Heartland Wrestling Association (HWA) — Cincinnati, OH

Les Thatcher's classroom. Promo labs, psychology seminars, and a trainer who has forgotten more about wrestling than most people will ever learn. The cerebral approach to developmental. 7 rooms.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Les Thatcher | Les Thatcher | Trainer | Face | 30 | — |
| Brian "The Dragon" Danielson | Bryan Danielson | Wrestler | Face | 18 | Cattle Mutilation |
| Nick Nemeth Jr. | Dolph Ziggler (HWA) | Wrestler | Heel | 14 | Zig Zag |

---

### Tier 4 — National / International

The biggest stages in the world. Sold-out arenas, national TV, and the pressure of performing for millions. This is where legends are made — or broken.

#### World Wrestling Federation (WWF) — New York, NY

Madison Square Garden. 20,000 seats, national TV, and the machine that turns wrestlers into superstars. The biggest roster in the game — from Hawk Hogan at the top to Gillberg at the very bottom. 8 rooms, 77 named NPCs.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Hawk Hogan | Hulk Hogan | Wrestler | Face | 45 | Atomic Leg Drop |
| "Ice Cold" Steve Austen | Steve Austin | Wrestler | Anti-Hero | 44 | Stone Cold Stunner |
| The Gravedigger | Undertaker | Wrestler | Anti-Hero | 44 | Tombstone Piledriver |
| "The Foundation" Dwayne Maivia | The Rock | Wrestler | Anti-Hero | 44 | Rock Bottom |
| Bruno Sammarco | Bruno Sammartino | Wrestler | Face | 42 | Bear Hug |
| Antoine the Giant | Andre the Giant | Wrestler | Anti-Hero | 42 | Sitdown Splash |
| Hunter Hearst Hampton | Triple H | Wrestler | Heel | 42 | Pedigree |
| "The Showstopper" Shane Mitchell | Shawn Michaels | Wrestler | Face | 42 | Sweet Chin Music |
| "Wild Man" Randy Salvatore | Randy Savage | Wrestler | Heel | 40 | Flying Elbow Drop |
| Kirk Engleton | Kurt Angle | Wrestler | Heel | 40 | Ankle Lock |
| The Supreme Savage | Ultimate Warrior | Wrestler | Face | 38 | Gorilla Press Splash |
| "The Inferno" Kane Blackwell | Kane | Wrestler | Anti-Hero | 38 | Chokeslam |
| Mick "Cactus" Manley | Mick Foley | Wrestler | Anti-Hero | 36 | Mandible Claw |
| Jake "The Serpent" Rollins | Jake Roberts | Wrestler | Anti-Hero | 36 | DDT |
| Adam "Razor" Copperton | Edge | Wrestler | Heel | 35 | Spear |
| "Big Diesel" Kevin Nash | Diesel | Wrestler | Face | 35 | Jacknife Powerbomb |
| "The Bad Guy" Razor Ramone | Scott Hall | Wrestler | Anti-Hero | 35 | Razor's Edge |
| Sycho Sid Vega | Sycho Sid | Wrestler | Heel | 33 | Powerbomb |
| Trish Stratos | Trish Stratus | Wrestler | Face | 30 | Stratusfaction |
| Marcus Henderson | Mark Henry | Wrestler | Face | 30 | World's Strongest Slam |
| Farooq Simms | Ron Simmons | Wrestler | Face | 30 | Dominator |
| The Fabulous Moolah Franklin | Fabulous Moolah | Wrestler | Heel | 30 | Backbreaker |
| "The Ninth Wonder" Joan Laurer | Chyna | Wrestler | Anti-Hero | 30 | Pedigree |
| Christian Cabot | Christian | Wrestler | Heel | 30 | Killswitch |
| Jeff Rainbow | Jeff Hardy | Wrestler | Anti-Hero | 30 | Swanton Bomb |
| Matt Rainbow | Matt Hardy | Wrestler | Face | 28 | Twist of Fate |
| "The Rebel" Amy Dumas | Lita | Wrestler | Anti-Hero | 28 | Litasault |
| Alundra Blaze | Madusa | Wrestler | Face | 28 | German Suplex |
| Kenny Starling | Ken Shamrock | Wrestler | Anti-Hero | 28 | Ankle Lock |
| Demolition Axe | Demolition Ax | Wrestler | Heel | 26 | Decapitation |
| Wendy Richmond | Wendi Richter | Wrestler | Face | 25 | Suplex |
| "Lightning" Sean Walton | X-Pac | Wrestler | Heel | 25 | X-Factor |
| "Bad Ass" Billy Gunther | Billy Gunn | Wrestler | Face | 25 | Fameasser |
| Road Dog Jesse Jamison | Road Dogg | Wrestler | Face | 25 | Shake Rattle & Roll |
| IRS Ellison | IRS | Wrestler | Heel | 25 | Write-Off |
| Victoria Varon | Victoria | Wrestler | Heel | 25 | Widow's Peak |
| Sensuous Sherry Valentine | Sherri Martel | Wrestler | Heel | 25 | Loaded Purse Shot |
| Gail Storm | Gail Kim | Wrestler | Face | 25 | Eat Defeat |
| Tara Vengeance | Tara | Wrestler | Anti-Hero | 25 | Widow's Peak |
| Crush | Demolition Crush | Wrestler | Heel | 24 | Decapitation Elbow |
| Demolition Smash | Demolition Smash | Wrestler | Heel | 24 | Decapitation Elbow |
| Vince Valentine | Val Venis | Wrestler | Face | 22 | Money Shot |
| Dante Lowe | D'Lo Brown | Wrestler | Face | 22 | Lo Down |
| Titan Andrews | Test | Wrestler | Face | 22 | Big Boot |
| The 1-2-3 Kid Sterling | 1-2-3 Kid | Wrestler | Face | 22 | Spinning Heel Kick |
| Molly Holloway | Molly Holly | Wrestler | Face | 22 | Molly-Go-Round |
| Papa Shaun | Papa Shango | Wrestler | Heel | 22 | Shoulderbreaker |
| Doink the Joker | Doink the Clown | Wrestler | Face | 22 | Whoopee Cushion |
| Crush Kona | Crush | Wrestler | Heel | 22 | Kona Crush |
| Brian Knox | Brian Knobbs | Wrestler | Heel | 22 | Pit Stop |
| Jerry Saggs | Jerry Sags | Wrestler | Heel | 22 | Pit Stop |
| Melina Vega | Melina | Wrestler | Heel | 22 | Split-Legged Facebuster |
| Ivory Keys | Ivory | Wrestler | Face | 22 | Vertical Suplex |
| Savio Vega Rios | Savio Vega | Wrestler | Face | 20 | Caribbean Kick |
| Adam Bomb Blaster | Adam Bomb | Wrestler | Heel | 20 | Atomic Drop |
| Kama Mustafa | Kama | Wrestler | Heel | 20 | T-Bone Suplex |
| Tori Steele | Tori | Wrestler | Face | 20 | Hurricanrana |
| Sable Monroe | Sable | Wrestler | Heel | 18 | Sable Bomb |
| The Mountie Marchand | The Mountie | Wrestler | Heel | 18 | Cattle Prod |
| Iron Mike Sharpe | Iron Mike Sharpe | Wrestler | Heel | 18 | Loaded Forearm |
| Pretty Boy Roma | Paul Roma | Wrestler | Heel | 18 | Diving Fistdrop |
| Henry Godwin Jr. | Henry Godwin | Wrestler | Heel | 18 | Slop Drop |
| Beau Bevins | Beau Beverly | Wrestler | Heel | 18 | Double Flapjack |
| Blake Bevins | Blake Beverly | Wrestler | Heel | 18 | Double Flapjack |
| Frankie Firestorm | original | Wrestler | Heel | 18 | Firestorm Suplex |
| Nikolai Volkov II | original | Wrestler | Heel | 18 | Iron Curtain |
| Layla Royale | Layla | Wrestler | Heel | 18 | Layout |
| Skinner Gator | Skinner | Wrestler | Heel | 16 | Gator Roll |
| Repo Rex | Repo Man | Wrestler | Heel | 16 | Repo Clutch |
| Duke Droese | Duke Droese | Wrestler | Face | 16 | Trash Compactor |
| Christy Hemsworth | Christy Hemme | Wrestler | Face | 16 | Spinning DDT |
| Brooklyn Steve Lombardi | Brooklyn Brawler | Wrestler | Heel | 14 | Jawbreaker |
| SD Jones | SD Jones | Wrestler | Face | 14 | Headbutt |
| Nidia Santos | Nidia | Wrestler | Face | 14 | Bulldog |
| Aksana Voss | Aksana | Wrestler | Heel | 14 | Ground Cobra |
| Miss Kitty Quinn | The Kat | Wrestler | Heel | 12 | Low Blow Kick |
| Duane Gill | Gillberg | Wrestler | Face | 8 | Jackhammer |
| Barry Hardy | Barry Hardy | Wrestler | Face | 8 | Small Package |

#### World Championship Wrestling (WCW) — Atlanta, GA

CNN Center. Turner money, Monday Night Wars, and the deepest cruiserweight division on the planet. From "The Scorpion" Steve Borden to Lodi holding a sign in the crowd — everyone has a spot. 8 rooms, 57 named NPCs.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| "The Scorpion" Steve Borden | Sting | Wrestler | Face | 40 | Scorpion Deathlock |
| "The Lionheart" Chris Jerichord | Chris Jericho | Wrestler | Heel | 38 | Walls of Jerichord |
| "The Great" Keiji Mutoh | Great Muta | Wrestler | Anti-Hero | 38 | Shining Wizard |
| Goldburg | Goldberg | Wrestler | Face | 38 | Spear |
| Shinya Hashimori | Shinya Hashimoto | Wrestler | Anti-Hero | 36 | Brainbuster |
| Genichiro Tendoh | Genichiro Tenryu | Wrestler | Anti-Hero | 36 | Powerbomb |
| Diamond Dallas Pierce | DDP | Wrestler | Face | 35 | Diamond Cutter |
| "Big Poppa" Scotty Steinberg | Scott Steiner | Wrestler | Heel | 35 | Steinberg Recliner |
| Masahiro Choono | Masahiro Chono | Wrestler | Heel | 35 | STF |
| Riki Choshu Maru | Riki Choshu | Wrestler | Face | 35 | Sasori-gatame |
| "The Colossus" Paul Whitmore | Big Show | Wrestler | Anti-Hero | 35 | Chokeslam |
| Booker Washington | Booker T | Wrestler | Face | 34 | Scissors Kick |
| Rey Mysterioso | Rey Mysterio | Wrestler | Face | 34 | 619 |
| Ricky Steinberg | Rick Steiner | Wrestler | Face | 30 | Steinberg Bulldog |
| "The Iceman" Dean Malone | Dean Malenko | Wrestler | Face | 30 | Texas Cloverleaf |
| Satoshi Nishimoto | Satoshi Kojima | Wrestler | Face | 30 | Lariat |
| K-Dogg Konner | Konnan | Wrestler | Anti-Hero | 28 | Tequila Sunrise |
| Perry Sattler | Perry Saturn | Wrestler | Anti-Hero | 28 | Rings of Sattler |
| Ultimo Fuego | Ultimo Dragon | Wrestler | Face | 28 | Asai Moonsault |
| Negro Navarro | Negro Navarro | Wrestler | Anti-Hero | 28 | La Nudo Lagunero |
| Buff Bagman | Buff Bagwell | Wrestler | Heel | 25 | Blockbuster |
| Vampiro Diablo | Vampiro | Wrestler | Anti-Hero | 25 | Nail in the Coffin |
| Psicosis Loco | Psicosis | Wrestler | Heel | 25 | Guillotine Leg Drop |
| Juventud Guerrera Jr. | Juventud Guerrera | Wrestler | Face | 25 | Juvi Driver |
| La Parka Esqueleto | La Parka | Wrestler | Anti-Hero | 25 | Corkscrew Plancha |
| Chris Kannonball | Chris Kanyon | Wrestler | Anti-Hero | 25 | Flatliner |
| Blue Panther Reyes | Blue Panther | Wrestler | Heel | 25 | La Tapatia |
| Johnny Ace Laurens | Johnny Ace | Wrestler | Heel | 25 | Ace Crusher |
| "Stunning" Stan Vega | Stunning Steve Austin | Wrestler | Heel | 25 | Stun Gun |
| "The Cat" Ernest Mills | Ernest Miller | Wrestler | Heel | 22 | Feliner |
| Chavo Garza Jr. | Chavo Guerrero Jr. | Wrestler | Heel | 22 | Gory Neckbreaker |
| Hector Garza | Hector Garza | Wrestler | Face | 22 | Corkscrew Plancha |
| Silver King Reyes | Silver King | Wrestler | Heel | 22 | Silver Bomb |
| Kronik Adams | Brian Adams | Wrestler | Heel | 22 | High Times |
| Kronik Clark | Bryan Clark | Wrestler | Heel | 22 | High Times |
| Elix Skipper | Elix Skipper | Wrestler | Heel | 22 | Powerplex |
| Norman Smilez | Norman Smiley | Wrestler | Face | 22 | Big Wiggle Crossface |
| Jinsei Shintaro | Hakushi | Wrestler | Face | 22 | Praying Powerbomb |
| Johnny B. Badd Jr. | Marc Mero | Wrestler | Face | 22 | Badd Day |
| El Hijo del Aguila | fictional | Wrestler | Face | 22 | Super Hurricanrana |
| Volador Blanco | Volador Jr. | Wrestler | Face | 22 | Spanish Fly |
| "Das Wunderkind" Alex Berlyn | Alex Wright | Wrestler | Heel | 20 | European Uppercut Rush |
| Diamond Stud | Diamond Stud | Wrestler | Heel | 20 | Diamond Death Drop |
| El Dandy Oro | El Dandy | Wrestler | Face | 20 | La Magistral |
| Kaz Hayashi | Kaz Hayashi | Wrestler | Face | 20 | Final Cut |
| Heavy Metal Reyes | Heavy Metal | Wrestler | Anti-Hero | 20 | Metal Driver |
| Shane Helms | Shane Helms | Wrestler | Face | 20 | Three Count Splash |
| Scotty Riggs | Scotty Riggs | Wrestler | Face | 18 | Double Dropkick |
| Marcus Bagwell | Marcus Bagwell | Wrestler | Face | 18 | Double Dropkick |
| Scotty Flamingo | Scotty Flamingo | Wrestler | Heel | 18 | DDT |
| Vinnie Vegas | Vinnie Vegas | Wrestler | Heel | 18 | Side Slam |
| Super Calo Vega | Super Calo | Wrestler | Face | 18 | Springboard Crossbody |
| Blitzkrieg Flyer | Blitzkrieg | Wrestler | Face | 18 | Spiral Bomb |
| Shannon Morez | Shannon Moore | Wrestler | Face | 18 | Three Count Splash |
| Crowbar Crowe | Crowbar | Wrestler | Anti-Hero | 18 | Crowbar Driver |
| Tank Abbot | Tank Abbott | Wrestler | Heel | 18 | KO Punch |
| Latin Loverboy | Latin Lover | Wrestler | Face | 18 | Love Handle |
| Lizmark Jr. | Lizmark Jr. | Wrestler | Face | 20 | Top Rope Moonsault |
| Mascara Sagrada | Mascara Sagrada | Wrestler | Face | 18 | Headscissors Takedown |
| Torri Wilkins | Torrie Wilson | Wrestler | Face | 16 | Slop Drop |
| Stacy Kincaid | Stacy Keibler | Wrestler | Face | 16 | High Kick |
| Evan Courageous | Evan Karagias | Wrestler | Face | 16 | Springboard Moonsault |
| Lenny Lanes | Lenny Lane | Wrestler | Heel | 16 | Fameasser |
| Mike Randels | Mike Sanders | Wrestler | Heel | 16 | 3.0 Neckbreaker |
| Kwee-Wee Weston | Kwee-Wee | Wrestler | Heel | 16 | Rage |
| Big Josh | Big Josh | Wrestler | Face | 16 | Northern Suplex |
| PN News | P.N. News | Wrestler | Face | 14 | Rapmaster Splash |
| Rick Fuller | Rick Fuller | Wrestler | Heel | 14 | Full Nelson |
| Mean Mike | Mean Mike | Wrestler | Heel | 14 | Double Slam |
| Tough Tom | Tough Tom | Wrestler | Heel | 14 | Double Slam |
| Lodi Picket | Lodi | Wrestler | Heel | 12 | Flapjack |
| Sgt. Buddy Lee Parker | Buddy Lee Parker | Wrestler | Heel | 12 | Clothesline |

#### Extreme Championship Wrestling (ECW) — Philadelphia, PA

The Bingo Hall. 1,200 rabid fans who throw chairs and chant profanity. No rules, no limits, and a roster that will do anything to get a reaction. The most dangerous territory in the game. 7 rooms, 44 named NPCs.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Eddie Guerrera | Eddie Guerrero | Wrestler | Anti-Hero | 38 | Frog Splash |
| "The Crippler" Chris Benning | Chris Benoit | Wrestler | Heel | 36 | Crossface |
| Mick "Cactus" Manley | Mick Foley | Wrestler | Anti-Hero | 36 | Mandible Claw |
| Rob Van Dyke | Rob Van Dam | Wrestler | Anti-Hero | 34 | Five Star Frog Splash |
| The Dudleys | Dudley Boyz | Wrestler | Anti-Hero | 30 | 3D |
| Raven Darkholme | Raven | Wrestler | Anti-Hero | 30 | Evenflow DDT |
| Sabu al-Rashid | Sabu | Wrestler | Anti-Hero | 30 | Triple Jump Moonsault |
| "The Sandstorm" Sandy White | Sandman | Wrestler | Anti-Hero | 28 | White Russian Legsweep |
| Tommy Dreaming | Tommy Dreamer | Wrestler | Face | 28 | Dreamer DDT |
| Shane Dalton | Shane Douglas | Wrestler | Heel | 28 | Belly-to-Belly Suplex |
| Taz Simmons | Taz | Wrestler | Anti-Hero | 28 | Taz-mission |
| Mike Awesome Powers | Mike Awesome | Wrestler | Heel | 28 | Awesome Bomb |
| Jerry Lydon | Jerry Lynn | Wrestler | Face | 28 | Cradle Piledriver |
| Lance Tempest | Lance Storm | Wrestler | Face | 28 | Canadian Maple Leaf |
| Amazing Kong | Amazing Kong | Wrestler | Heel | 28 | Implant Buster |
| New Jack Carter | New Jack | Wrestler | Anti-Hero | 25 | 187 |
| Jazz Carlisle | Jazz | Wrestler | Heel | 25 | STF |
| Too Cold Scorpio | 2 Cold Scorpio | Wrestler | Face | 25 | Funky Moonsault |
| Yoshihiro Tajima | Yoshihiro Tajiri | Wrestler | Anti-Hero | 25 | Buzzsaw Kick |
| Chris Danvers | Christopher Daniels | Wrestler | Heel | 25 | Powerplex |
| Justin Credulous | Justin Credible | Wrestler | Heel | 22 | That's Incredible |
| Sarita Vega | Sarita | Wrestler | Face | 22 | Tornado DDT |
| "Dynamite" Yuki Tanaka | fictional joshi | Wrestler | Face | 22 | Rolling Clutch |
| Elix Skipper | Elix Skipper | Wrestler | Heel | 22 | Powerplex |
| ODB McBride | ODB | Wrestler | Anti-Hero | 22 | BAM |
| Little Spike Dudley | Spike Dudley | Wrestler | Face | 20 | Acid Drop |
| Mikey Whiplash | Mikey Whipwreck | Wrestler | Face | 20 | Whippersnapper |
| Balls Maloney | Balls Mahoney | Wrestler | Anti-Hero | 20 | New Jersey Jam |
| Flash Funk Jr. | Flash Funk | Wrestler | Face | 20 | Funky Moonsault |
| Dex Rampage | original | Wrestler | Anti-Hero | 20 | Rampage Bomb |
| Cactus Joe | original | Wrestler | Anti-Hero | 20 | Cactusbomb |
| Madison Royals | Madison Rayne | Wrestler | Heel | 20 | Cross Rayne |
| Roxxi Laveau | Roxxi Laveaux | Wrestler | Anti-Hero | 20 | Voodoo Drop |
| Vito Guido | Vito | Wrestler | Heel | 20 | Mob Hit |
| Johnny Stamboli | Johnny Stamboli | Wrestler | Heel | 20 | Mob Hit |
| Dawn Martine | Dawn Marie | Wrestler | Heel | 18 | Spinning Neckbreaker |
| Daffney Crane | Daffney | Wrestler | Heel | 18 | The Wail |
| Super Nova | Nova | Wrestler | Face | 18 | Novacaine |
| Danny Doring | Danny Doring | Wrestler | Face | 18 | Lancaster Bomb |
| Roadkill Hess | Roadkill | Wrestler | Face | 18 | Lancaster Bomb |
| Rex Headhunter | Headhunter 1 | Wrestler | Heel | 18 | Bounty Collected |
| Pike Headhunter | Headhunter 2 | Wrestler | Heel | 18 | Bounty Collected |
| Axl Rotton | Axl Rotten | Wrestler | Heel | 18 | Chair Shot |
| Big Dick Tanaka | Big Dick Dudley | Wrestler | Heel | 18 | Chokeslam |
| DJ Vicious | original | Wrestler | Heel | 18 | Drop the Bass |
| Velvet Skye | Velvet Sky | Wrestler | Face | 18 | In Your Face |
| Danny Doring Solo | Danny Doring | Wrestler | Face | 16 | Bareback |
| Ian Rotton | Ian Rotten | Wrestler | Anti-Hero | 16 | Piledriver |
| Francine Raines | Francine | Wrestler | Heel | 14 | Low Blow |

#### All Japan / New Japan Pro Wrestling — Tokyo, Japan

Nippon Budokan. The workrate capital of the world — 30-minute classics are the norm, not the exception. Strict hierarchy, stiff strikes, and a roster that includes the best joshi wrestlers alive. Lucha libre crossover talent rounds out the international flavor. 7 rooms, 45 named NPCs.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Mitsuhiro Misawa | Mitsuharu Misawa | Wrestler | Face | 40 | Emerald Flowsion |
| Kenta Kobashi-do | Kenta Kobashi | Wrestler | Face | 40 | Burning Lariat |
| Antonio Inagi | Antonio Inoki | Wrestler | Face | 40 | Enziguiri |
| Stan Hanssen | Stan Hansen | Wrestler | Anti-Hero | 38 | Western Lariat |
| Giant Bamba | Giant Baba | Wrestler | Face | 38 | Running Neckbreaker |
| Jumbo Tsukuda | Jumbo Tsuruta | Wrestler | Face | 38 | Knee Lift |
| Toshiaki Kawada | Toshiaki Kawada | Wrestler | Heel | 38 | Ganso Bomb |
| Akira Taue | Akira Taue | Wrestler | Heel | 35 | Dynamic Bomb |
| El Santo Dorado | El Santo | Wrestler | Face | 35 | La de a Caballo |
| Riki Choshu Maru | Riki Choshu | Wrestler | Face | 35 | Sasori-gatame |
| El Hijo del Diablo | Mil Mascaras | Wrestler | Face | 32 | Plancha |
| Tiger Mask Hayashi | Tiger Mask | Wrestler | Face | 32 | Tiger Suplex |
| Manami Toyoda | Manami Toyota | Wrestler | Face | 32 | Japanese Ocean Cyclone Suplex |
| Bull Nakamura | Bull Nakano | Wrestler | Heel | 30 | Guillotine Leg Drop |
| Aja Kongo | Aja Kong | Wrestler | Heel | 30 | Uraken |
| Hayabusa Takeda | Hayabusa | Wrestler | Face | 30 | Phoenix Splash |
| Lioness Asuka | Lioness Asuka | Wrestler | Face | 28 | Running Powerbomb |
| Kyoko Imai | Kyoko Inoue | Wrestler | Heel | 28 | Japanese Ocean Cyclone |
| Devil Masaki | Devil Masami | Wrestler | Heel | 28 | Devil Screwdriver |
| Cutie Yoshida | Cutie Suzuki | Wrestler | Face | 25 | Bridging German |
| El Fuego Negro | original | Wrestler | Face | 22 | Black Fire Splash |
| La Mascara Gris | original | Wrestler | Anti-Hero | 22 | El Tormento |
| The Crimson Phoenix | original | Wrestler | Face | 22 | Phoenix Splash |
| "Dynamite" Yuki Tanaka | fictional joshi | Wrestler | Face | 22 | Rolling Clutch |
| Jinsei Shintaro | Hakushi | Wrestler | Face | 22 | Praying Powerbomb |
| El Hijo del Aguila | fictional | Wrestler | Face | 22 | Super Hurricanrana |
| Volador Blanco | Volador Jr. | Wrestler | Face | 22 | Spanish Fly |
| Sarita Vega | Sarita | Wrestler | Face | 22 | Tornado DDT |
| La Diabla | fictional luchadora | Wrestler | Heel | 22 | Devil's Wings |
| Rosa Blanca | fictional luchadora | Wrestler | Face | 20 | La Magistral |
| Serpentina | fictional luchadora | Wrestler | Heel | 20 | Boa Constrictor |
| Candy Okamura | Candy Okutsu | Wrestler | Face | 20 | Moonsault |
| Lizmark Jr. | Lizmark Jr. | Wrestler | Face | 20 | Top Rope Moonsault |
| Heavy Metal Reyes | Heavy Metal | Wrestler | Anti-Hero | 20 | Metal Driver |
| Latin Loverboy | Latin Lover | Wrestler | Face | 18 | Love Handle |
| Mascara Sagrada | Mascara Sagrada | Wrestler | Face | 18 | Headscissors Takedown |
| Amazing Kong | Amazing Kong | Wrestler | Heel | 28 | Implant Buster |
| Negro Navarro | Negro Navarro | Wrestler | Anti-Hero | 28 | La Nudo Lagunero |
| Blue Panther Reyes | Blue Panther | Wrestler | Heel | 25 | La Tapatia |
| Johnny Ace Laurens | Johnny Ace | Wrestler | Heel | 25 | Ace Crusher |
| Satoshi Nishimoto | Satoshi Kojima | Wrestler | Face | 30 | Lariat |
| "The Great" Keiji Mutoh | Great Muta | Wrestler | Anti-Hero | 38 | Shining Wizard |
| Shinya Hashimori | Shinya Hashimoto | Wrestler | Anti-Hero | 36 | Brainbuster |
| Masahiro Choono | Masahiro Chono | Wrestler | Heel | 35 | STF |
| Genichiro Tendoh | Genichiro Tenryu | Wrestler | Anti-Hero | 36 | Powerbomb |

#### World of Sport Wrestling — London, UK

Royal Albert Hall. Technical chain wrestling, catch-as-catch-can, and a British crowd that appreciates the craft. From the enormous Large Lad to the technical wizardry of Johnny Sinclair — a different style entirely. 6 rooms, 9 named NPCs.

| Name | Based On | Role | Alignment | Level | Finisher |
|------|----------|------|-----------|-------|----------|
| Pat Finney | Fit Finlay | Wrestler | Heel | 32 | Celtic Cross |
| Lord William Regalton | William Regal | Wrestler | Heel | 32 | Power of the Punch |
| Johnny Sinclair | Johnny Saint | Wrestler | Face | 30 | Chain Wrestling |
| Large Lad | Big Daddy | Wrestler | Face | 30 | Belly Splash |
| Colossal Haymaker | Giant Haystacks | Wrestler | Heel | 30 | Splash |
| Nigel McGuinn | Nigel McGuinness | Wrestler | Face | 28 | Tower of London |
| Professor Pain | original | Wrestler | Heel | 28 | Lesson Learned |
| Davey Dingo | fictional British | Wrestler | Anti-Hero | 20 | London Calling |
| Billy Blokes | fictional British | Wrestler | Anti-Hero | 20 | London Calling |

---

### NPC Managers (17)

| Name | Based On | Territory | Alignment | Style | CHA | PSY | Retainer | Cut |
|------|----------|-----------|-----------|-------|-----|-----|----------|-----|
| Bobby Haynes | Bobby Heenan | AWA | Heel | Cowardly genius | 18 | 17 | $150/wk | 25% |
| Jimmy Montague | Jimmy Hart | Memphis | Heel | Fast-talking megaphone | 16 | 14 | $100/wk | 20% |
| "Captain" Lou Albanese | Captain Lou Albano | WWF | Heel | Wild and unpredictable | 15 | 13 | $120/wk | 20% |
| Paul Barrington | Paul Bearer | WWF | Heel | Supernatural | 14 | 16 | $130/wk | 20% |
| Miss Elizabeth Salvatore | Miss Elizabeth | WWF | Face | Elegant distraction | 17 | 12 | $120/wk | 15% |
| Freddy Blaze | Freddie Blassie | WWF | Heel | Cane-wielding old school | 16 | 14 | $110/wk | 20% |
| Jim Corwin | Jim Cornette | OVW | Heel | Tennis racket screamer | 19 | 20 | $200/wk | 25% |
| Percival Ellison | Paul Ellering | Mid-Atlantic | Face | Intellectual strategist | 13 | 18 | $140/wk | 20% |
| Sonny King | Skandor Akbar | Mid-South | Heel | Mastermind | 15 | 16 | $130/wk | 20% |
| Mr. Fuji Tanaka | Mr. Fuji | WWF | Heel | Devious | 13 | 15 | $100/wk | 20% |
| Phil "The Advocate" Eastman | Paul Heyman | ECW | Anti-Hero | Master strategist | 20 | 19 | $300/wk | 25% |
| Sensuous Sherry Valentine (Mgr) | Sherri Martel | WWF | Heel | Physical interference | 16 | 13 | $110/wk | 20% |
| Gary Sharp | Gary Hart | WCCW | Heel | Mastermind booker | 15 | 17 | $140/wk | 20% |
| James Dixon | J.J. Dillon | Mid-Atlantic | Heel | Corporate fixer | 14 | 16 | $130/wk | 20% |
| Sunshine Summers | Sunny | WWF | Face | Distraction specialist | 18 | 11 | $120/wk | 15% |
| Terri Goldwyn | Terri Runnels | WWF | Heel | Plays both sides | 15 | 13 | $100/wk | 20% |
| **"The East End Villain" Josh Ashcraft** | **Josh Ashcraft** | **OVW** | **Anti-Hero** | **East End street-smart villain** | **17** | **16** | **$150/wk** | **20%** |

---

## Changelog

### 2026-03-02 — Multi-Character, Bridge UX, Josh Ashcraft

**Added:**
- Multi-character support: up to 10 wrestlers per account (`charselect`, `charcreate`)
- Lodging system: inns, player houses, upgrades, message boards (`rest`, `board`, `post`, `buyhouse`, `gohome`, `upgrade`)
- Brawl command for backstage fights
- "The East End Villain" Josh Ashcraft NPC (with permission) — OVW announcer, wrestler, and manager
- Custom base Command class with `> ` prompt after every command
- `__nomatch_command`: unknown commands show error + "Press ENTER to continue" + room refresh
- `__noinput_command`: empty ENTER refreshes the room
- `card` and `board` commands show "Press ENTER to continue" then refresh room
- Yellow-highlighted exit directions for visibility
- Room display groups characters by type (Wrestlers, Managers, Trainers, Promoters, Players)
- Exit look shows destination room name + description preview

**Fixed:**
- Bridge: added bridge-side echo (BBS users can see what they type)
- Bridge: proper IAC negotiation (DONT/WONT responses to Evennia telnet options)
- Bridge: line buffering with local backspace handling (no more garbled commands)
- Bridge: ANSI-aware word wrap at 78 columns (no more mid-word line breaks)
- Bridge: UTF-8 to ASCII transliteration (em dashes, curly quotes work on CP437 terminals)
- Bridge: clear screen on login, strips stale session data before KAYFABE banner
- Bridge: drains all post-login puppet output before switching to bidirectional mode
- Login: accounts use `self.characters` instead of broken key-based search (ring names no longer break login)
- Match: added perspective headers ("YOUR OFFENSE:", "YOU SELL:", etc.)
- Match: pin/kickout rework — NPC pins during finish phase, kickout only during active pin
- Match: available commands shown after every match action
- Timezone: message board timestamps now Central time (America/Chicago), 12-hour format
- Removed hardcoded "Exits:" from 18 room descriptions (was showing duplicate exits)
- Fixed TerritoryRoom/ChargenRoom/PlayerHouse inheritance to use Room base class

**Contributors:**
- RAI (RAI) — design, testing, OVW permission
- Claude Code (Anthropic) — implementation

## License

Private. Not for public distribution.
