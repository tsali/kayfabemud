# Changelog — Kayfabe: Protect the Business

## v0.3a — 2026-03-02

### Added
- Dirt Sheet weekly newsletter system — auto-generated from game events
  - Match results (3+ stars), title changes, injuries, rank-ups, contracts, stable activity
  - `dirtsheet` command to read current issue
  - `dirtsheet list` to browse archived issues (up to 20)
  - Wrestling journalist flavor text and star rating display
- Move Library / Vet Mentorship system
  - 27 new signature moves with `learned_only` gate (difficulty 5-7, damage 4-8)
  - 21 veteran NPCs assigned teachable signature movesets
  - Rapport system: build reputation with vets by wrestling in their territory (+5/+10) and training near them (+2)
  - `learn` command to discover nearby vets, view their moves, and study under them
  - Rapport thresholds: 20 (first move), 50 (second), 80 (third)
  - `moves` command shows [LOCKED] / [KNOWN] tags on signature moves
  - `work <move>` blocked in matches for unlearned signature moves with helpful message
  - Rapport decay: -1/week if not in vet's territory

### Fixed
- Chargen reconnect bug: players who disconnect before choosing a starting federation now resume at fed selection instead of being stuck at Behind the Curtain
- Vet name matching: partial names (e.g. "afa") correctly match full NPC names (e.g. "Chief Afa Savea")
- Duplicate "injury" text in dirt sheet injury reports
- NPCs now persist signature_moves attribute on spawn (was only in data file, not on live objects)

---

## v0.2a — 2026-03-01

### Added
- Social commands: `who`, `ooc`, `emote`, `finger`, `dirtsheet`
- Stables system: form factions, recruit members, stable bonuses
- Contract system: sign with territories, weekly pay, contract terms
- Championship system: territory titles, title matches, championship history
- Show system: weekly cards, match booking, show results
- Injury system: match injuries, recovery time, injury severity
- Backstage system: locker room interactions, heat, politics
- Tutorial: "Learning the Ropes" guided first match
- Commentary system: play-by-play and color commentary during matches
- Merch display: character merchandise and sales
- Chargen improvements: input prompts, compact fed list, `chardelete` command

---

## v0.1a — 2026-02-28

### Added
- Core wrestling match engine (5 phases: opening, heat, hope, comeback, finish)
- Character creation with ring name, real name, hometown, gender, style, alignment, finisher
- 5 wrestling styles with stat bonuses (Brawler, Technical, High-Flyer, Showman, All-Rounder)
- 6 core stats: Strength, Agility, Technical, Charisma, Toughness, Psychology
- 44 base wrestling moves with type, difficulty, damage, and stat requirements
- 5 territory tiers: Backyard, Developmental, Regional, National, Global
- ~400 NPCs across all territories and eras
- Training schools with stat training and room bonuses
- XP and leveling system
- Kayfabe score mechanic
- Economy system with weekly pay ticks
- BBS bridge (rlogin) for Mystic BBS integration
- Compass navigation and in-game maps
- Multi-character support with `charcreate` / `charselect`
- Lodging system (rest at inns, buy houses)
- Gender/division system
