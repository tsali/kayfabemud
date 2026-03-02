"""
Kayfabe: Protect the Business — Territory data definitions.

All territories are defined here or imported from sub-modules:
- territories_backyard.py: BBA, PSC, GSG, LSU (Tier 1)
- territories_schools.py: 5 additional training schools (Tier 2)
- territories_regional.py: 8 regional territories (Tier 3)
- territories_developmental.py: OVW, FCW, DSW, HWA (Tier 3.5)
- territories_national.py: WWF, WCW, ECW, UK, Japan (Tier 4)

FHWA, GCCW, Pensacola, and Memphis are defined directly below.
"""

# Each territory is a dict with rooms list. Each room has:
#   key, name, desc, typeclass, room_type, tags, extras (stat_bonus, etc.)

TERRITORIES = {}

# ============================================================
# TIER 1 — BACKYARD FEDS
# ============================================================

TERRITORIES["fhwa"] = {
    "name": "Federal Hills Wrestling Association",
    "abbrev": "FHWA",
    "tier": 1,
    "location": "Shepherdsville, KY",
    "rooms": [
        {
            "key": "fhwa_parking",
            "name": "FHWA Parking Lot",
            "typeclass": "typeclasses.rooms.BackyardFedRoom",
            "tags": [("fhwa", "territory"), ("start_fhwa", "chargen")],
            "desc": (
                "A gravel parking lot behind the Shepherdsville VFW hall. Pickup "
                "trucks and beaters line the edges. A hand-painted plywood sign "
                "reads: 'FHWA WRESTLING TONIGHT — $3 ADMISSION'. You can hear a "
                "crowd of maybe forty people inside, stamping on metal bleachers.\n\n"
                "A cooler full of off-brand soda sits by the back door. Someone's "
                "kid is doing backflips off a stack of pallets.\n\n"
                "|wExits: |nsouth|w to the venue, |nnorth|w to the road.|n"
            ),
        },
        {
            "key": "fhwa_venue",
            "name": "VFW Hall — FHWA Arena",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("fhwa", "territory")],
            "extras": {"capacity": 50},
            "desc": (
                "The VFW hall has been converted into the world's saddest wrestling "
                "venue. A 12-foot ring sits in the middle of the room, ropes held "
                "taut with bungee cords and duct tape. Metal folding chairs surround "
                "it on three sides. The fourth side has a folding table for the "
                "'announce team' — one guy with a RadioShack microphone.\n\n"
                "An American flag hangs behind the ring. The ceiling is low enough "
                "that nobody's doing any top-rope moves. The crowd is a mix of "
                "locals, a few kids, and someone's grandma who thinks this is bingo "
                "night.\n\n"
                "Type |wcard|n to see tonight's lineup. |wwrestle <name>|n to get in the ring.\n\n"
                "|wExits: |nnorth|w to the parking lot, |nwest|w to the locker room.|n"
            ),
        },
        {
            "key": "fhwa_locker",
            "name": "VFW Storage Room — Locker Area",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("fhwa", "territory")],
            "desc": (
                "The 'locker room' is the VFW's storage closet. Mops, cleaning "
                "supplies, and a broken pool table share the space with duffel bags "
                "full of wrestling gear. A cracked mirror leans against the wall.\n\n"
                "The other wrestlers — a mix of locals with homemade gimmicks — "
                "are changing into their gear. Someone's taping their fists with "
                "electrical tape.\n\n"
                "|wExits: |neast|w back to the arena.|n"
            ),
        },
        {
            "key": "fhwa_road",
            "name": "Route 61 — Heading Out",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("fhwa", "territory")],
            "extras": {"destinations": ["gccw", "bba", "psc", "gsg", "lsu", "pensacola"]},
            "desc": (
                "Route 61 stretches north toward Louisville and south toward "
                "nowhere. Your car (if you can call it that) idles at the "
                "intersection.\n\n"
                "From here you could drive to any of the other small feds, "
                "or — if a training school has noticed you — head that way.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("south;s", "fhwa_parking", "fhwa_venue"),
        ("north;n", "fhwa_venue", "fhwa_parking"),
        ("west;w", "fhwa_venue", "fhwa_locker"),
        ("east;e", "fhwa_locker", "fhwa_venue"),
        ("north;n", "fhwa_parking", "fhwa_road"),
        ("south;s", "fhwa_road", "fhwa_parking"),
    ],
    "exit_descs": {
        ("fhwa_parking", "south"): "Through the back door you can see the VFW hall — a low-ceilinged room with a 12-foot ring in the middle.",
        ("fhwa_venue", "north"): "The back door leads out to the gravel parking lot. Pickup trucks idle under a hand-painted plywood sign.",
        ("fhwa_venue", "west"): "A doorway leads to the VFW storage room where wrestlers are changing into their gear.",
        ("fhwa_locker", "east"): "Through the doorway you can see the ring and the crowd of forty on metal bleachers.",
        ("fhwa_parking", "north"): "Route 61 stretches north toward Louisville and south toward nowhere. Your car idles at the intersection.",
        ("fhwa_road", "south"): "The gravel lot behind the VFW hall. A hand-painted sign reads: 'FHWA WRESTLING TONIGHT'.",
    },
}

TERRITORIES["gccw"] = {
    "name": "Gulf Coast Championship Wrestling",
    "abbrev": "GCCW",
    "tier": 1,
    "location": "Pensacola, FL",
    "rooms": [
        {
            "key": "gccw_parking",
            "name": "GCCW Parking Lot",
            "typeclass": "typeclasses.rooms.BackyardFedRoom",
            "tags": [("gccw", "territory"), ("start_gccw", "chargen")],
            "desc": (
                "A sandy parking lot behind a corrugated metal building on the "
                "outskirts of Pensacola. The Gulf humidity hits you like a wall. "
                "Spanish moss hangs from a live oak at the edge of the lot.\n\n"
                "A hand-lettered banner reads: 'GCCW — SATURDAY NIGHT WARS'. "
                "The building looks like it used to be an auto body shop. A few "
                "rusty cars and one lifted truck sit in the gravel.\n\n"
                "|wExits: |nsouth|w to the venue, |nnorth|w to the road.|n"
            ),
        },
        {
            "key": "gccw_venue",
            "name": "The Body Shop — GCCW Arena",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("gccw", "territory")],
            "extras": {"capacity": 60},
            "desc": (
                "The former auto body shop has been gutted and fitted with a "
                "regulation-size ring — the one thing GCCW didn't cheap out on, "
                "because the Savea family donated it. The concrete floor is "
                "covered with rubber mats around the ring apron.\n\n"
                "Plastic chairs and wooden bleachers line the walls. Industrial "
                "fans push the hot Florida air around without actually cooling "
                "anything. A VHS camcorder on a tripod records every show — "
                "these tapes sometimes find their way to the right people.\n\n"
                "Type |wcard|n to see tonight's lineup. |wwrestle <name>|n to get in the ring.\n\n"
                "|wExits: |nnorth|w to the parking lot, |nwest|w to the locker room.|n"
            ),
        },
        {
            "key": "gccw_locker",
            "name": "The Cage — Locker Area",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("gccw", "territory")],
            "desc": (
                "The locker area is a chain-link cage in the back of the building "
                "— literally a fenced-off corner with a bench and some hooks on "
                "the wall. 'The Cage' is what the boys call it.\n\n"
                "A cooler of water bottles sits on the floor (no Gatorade — "
                "that's for the main event guys). A whiteboard on the wall shows "
                "tonight's card in dry-erase marker.\n\n"
                "|wExits: |neast|w back to the arena.|n"
            ),
        },
        {
            "key": "gccw_road",
            "name": "Highway 98 — Heading Out",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("gccw", "territory")],
            "extras": {"destinations": ["fhwa", "bba", "psc", "gsg", "lsu", "pensacola"]},
            "desc": (
                "Highway 98 runs along the Gulf Coast, connecting Pensacola to "
                "the rest of the panhandle and beyond. The salt air mixes with "
                "exhaust.\n\n"
                "The Samoan Training Grounds is just across town if you've been "
                "invited. Otherwise, the road leads to other small feds or "
                "wherever else you can get a booking.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("south;s", "gccw_parking", "gccw_venue"),
        ("north;n", "gccw_venue", "gccw_parking"),
        ("west;w", "gccw_venue", "gccw_locker"),
        ("east;e", "gccw_locker", "gccw_venue"),
        ("north;n", "gccw_parking", "gccw_road"),
        ("south;s", "gccw_road", "gccw_parking"),
    ],
    "exit_descs": {
        ("gccw_parking", "south"): "Through the open bay doors you can see the converted auto body shop — a regulation-size ring sits inside.",
        ("gccw_venue", "north"): "The bay doors open to the sandy parking lot. Spanish moss hangs from the live oak at the edge.",
        ("gccw_venue", "west"): "A chain-link cage in the back corner — the locker area the boys call 'The Cage'.",
        ("gccw_locker", "east"): "Through the chain-link you can see the ring and the crowd on plastic chairs and wooden bleachers.",
        ("gccw_parking", "north"): "Highway 98 runs along the Gulf Coast, connecting Pensacola to the rest of the panhandle.",
        ("gccw_road", "south"): "The sandy parking lot behind the corrugated metal building. The Gulf humidity hits you like a wall.",
    },
}

# ============================================================
# TIER 2 — TRAINING SCHOOLS
# ============================================================

TERRITORIES["pensacola"] = {
    "name": "Samoan Training Grounds",
    "abbrev": "Pensacola",
    "tier": 2,
    "location": "Pensacola, FL",
    "rooms": [
        {
            "key": "pens_entrance",
            "name": "Pensacola Beach — Training Center Entrance",
            "typeclass": "typeclasses.rooms.TrainingSchoolRoom",
            "tags": [("pensacola", "territory"), ("start_pensacola", "chargen")],
            "desc": (
                "White sand stretches to the Gulf of Mexico. The training center "
                "sits a block from the beach — a low concrete building with a "
                "hand-painted sign: 'SAVEA WRESTLING ACADEMY — NO WEAKLINGS'.\n\n"
                "Chief Afa's pickup truck is parked out front. Through the open "
                "bay doors you can hear the sound of bodies hitting canvas and "
                "someone shouting in Samoan."
            ),
        },
        {
            "key": "pens_floor",
            "name": "Training Center — Main Floor",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("pensacola", "territory")],
            "extras": {"stat_bonus": "str", "bonus_amount": 1},
            "desc": (
                "The main training floor is a no-frills gym built for making "
                "wrestlers. A full-size ring dominates the center. Weight racks "
                "line the walls — heavy iron, no chrome machines. The floor is "
                "bare concrete with rubber mats around the ring.\n\n"
                "Chief Afa watches from a folding chair in the corner, arms "
                "crossed, face unreadable. Chief Sika spots someone on the "
                "bench press, barking instructions.\n\n"
                "A sign on the wall reads: '500 SQUATS BEFORE YOU TOUCH THE RING'."
            ),
        },
        {
            "key": "pens_pit",
            "name": "The Pit — Outdoor Training Area",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("pensacola", "territory")],
            "extras": {"stat_bonus": "tou", "bonus_amount": 2},
            "desc": (
                "Behind the training center, a sandy enclosure surrounded by "
                "cinder blocks — The Pit. This is where the Saveas separate the "
                "wrestlers from the wannabes.\n\n"
                "The Florida sun beats down mercilessly. No shade. No water "
                "breaks until the Chief says so. Trainees practice bumps in the "
                "sand, run drills until they puke, and learn that toughness isn't "
                "a stat — it's a lifestyle.\n\n"
                "|yTraining here gives a Toughness bonus.|n"
            ),
        },
        {
            "key": "pens_ring",
            "name": "Training Center — The Ring",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("pensacola", "territory")],
            "extras": {"capacity": 20},
            "desc": (
                "The training ring. Standard 16-foot, tight ropes, hard canvas. "
                "No padding under the apron — you learn to fall right or you feel "
                "it for a week.\n\n"
                "Trainees rotate through drills: lockups, chain wrestling, bumps, "
                "rope running. Chief Sika calls spots while Afa evaluates silently. "
                "The ones who can't hack it are usually gone by the second week."
            ),
        },
        {
            "key": "pens_afa_house",
            "name": "Afa's House",
            "typeclass": "typeclasses.rooms.UniqueRoom",
            "tags": [("pensacola", "territory")],
            "desc": (
                "A modest house on a quiet Pensacola street. The living room is "
                "a shrine to Samoan wrestling dynasty — photos cover every wall. "
                "The Wild Samoans tag team championships. High Chief Peter Maivia "
                "in his prime. Young Savea boys in training.\n\n"
                "A massive wooden kava bowl sits on the coffee table. The couch "
                "has seen better days but has hosted every trainee who ever "
                "graduated. Getting invited here means the Chief sees something "
                "in you."
            ),
        },
        {
            "key": "pens_civic",
            "name": "Pensacola Civic Center",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("pensacola", "territory")],
            "extras": {"capacity": 200},
            "desc": (
                "The Pensacola Civic Center — a real venue with real seats. This "
                "is where the training school holds its monthly shows, open to "
                "the public. Scouts from regional territories sometimes attend.\n\n"
                "Performing here is the final test. If you can work a match in "
                "front of a paying crowd and not embarrass yourself, you might "
                "be ready for the territories."
            ),
        },
        {
            "key": "pens_boardwalk",
            "name": "Pensacola Boardwalk",
            "typeclass": "typeclasses.rooms.BarRoom",
            "tags": [("pensacola", "territory")],
            "desc": (
                "The boardwalk runs along the beach, lined with tourist shops, "
                "fried fish joints, and dive bars. Trainees come here on their "
                "rare nights off to drink cheap beer and compare bruises.\n\n"
                "Every now and then a fan recognizes someone from the monthly "
                "show — a small reminder that this might actually become real."
            ),
        },
        {
            "key": "pens_tiki",
            "name": "Tiki Bar",
            "typeclass": "typeclasses.rooms.BarRoom",
            "tags": [("pensacola", "territory")],
            "desc": (
                "A thatched-roof open-air bar on the beach. Christmas lights "
                "year-round. Jimmy Buffett on the jukebox. Drinks are cheap and "
                "the bartender doesn't ask questions about your bruises.\n\n"
                "This is where trainees blow off steam and swap road stories "
                "with anyone who'll listen. Occasionally a veteran passing "
                "through will sit at the bar and drop knowledge if you buy the "
                "first round."
            ),
        },
        {
            "key": "pens_motel",
            "name": "Beachside Motel",
            "typeclass": "typeclasses.rooms.TerritoryRoom",
            "tags": [("pensacola", "territory")],
            "desc": (
                "A one-story motel a block from the beach. Peeling paint, "
                "window AC units that might work, and a neon 'VACANCY' sign "
                "that's been on since 1987.\n\n"
                "Most trainees share rooms to split the $29/night rate. The "
                "walls are thin enough to hear your neighbor's alarm clock. "
                "The ice machine works about half the time."
            ),
        },
        {
            "key": "pens_road",
            "name": "Highway 98 — Leaving Pensacola",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("pensacola", "territory")],
            "extras": {"destinations": ["gccw", "memphis", "florida", "georgia", "midsouth"]},
            "desc": (
                "The highway stretches away from Pensacola. If you've graduated "
                "the training school, the territories are calling. If not, well, "
                "there's always the backyard feds to sharpen up.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        # Entrance row: Afa's House - Entrance - Civic Center
        ("north;n", "pens_entrance", "pens_road"),
        ("south;s", "pens_road", "pens_entrance"),
        ("south;s", "pens_entrance", "pens_floor"),
        ("north;n", "pens_floor", "pens_entrance"),
        ("west;w", "pens_entrance", "pens_afa_house"),
        ("east;e", "pens_afa_house", "pens_entrance"),
        ("east;e", "pens_entrance", "pens_civic"),
        ("west;w", "pens_civic", "pens_entrance"),
        # Floor row: Pit - Floor - Ring
        ("west;w", "pens_floor", "pens_pit"),
        ("east;e", "pens_pit", "pens_floor"),
        ("east;e", "pens_floor", "pens_ring"),
        ("west;w", "pens_ring", "pens_floor"),
        # Boardwalk row: Boardwalk - Tiki Bar
        ("south;s", "pens_floor", "pens_boardwalk"),
        ("north;n", "pens_boardwalk", "pens_floor"),
        ("east;e", "pens_boardwalk", "pens_tiki"),
        ("west;w", "pens_tiki", "pens_boardwalk"),
        # Motel south of boardwalk
        ("south;s", "pens_boardwalk", "pens_motel"),
        ("north;n", "pens_motel", "pens_boardwalk"),
    ],
}

# ============================================================
# TIER 3 — REGIONAL TERRITORIES
# ============================================================

TERRITORIES["memphis"] = {
    "name": "Memphis Championship Wrestling",
    "abbrev": "Memphis",
    "tier": 3,
    "location": "Memphis, TN",
    "rooms": [
        {
            "key": "mem_arena",
            "name": "The Mid-South Coliseum",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("memphis", "territory"), ("start_memphis", "chargen")],
            "extras": {"capacity": 2000},
            "desc": (
                "The Mid-South Coliseum — Memphis's temple of wrestling. Every "
                "Monday night, this place fills up for championship wrestling on "
                "television. The hard camera is set up at the north end. The "
                "announce table sits ringside, where Lance Rosemont calls the "
                "action in his measured, credible voice.\n\n"
                "Tonight the card is stacked. The crowd is already loud. Memphis "
                "fans are the smartest in the business — they know good work "
                "when they see it, and they'll eat alive anyone who can't cut "
                "a promo."
            ),
        },
        {
            "key": "mem_backstage",
            "name": "Coliseum Backstage",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("memphis", "territory")],
            "desc": (
                "The backstage area of the Coliseum is cramped but electric. "
                "Wrestlers pace back and forth, rehearsing promos and stretching. "
                "A TV monitor shows the live broadcast — if you're booked "
                "tonight, you'd better be watching the match before yours.\n\n"
                "Jerry Crowley holds court in the corner, regaling anyone who'll "
                "listen with stories about working Andy Coughlin. The booker's "
                "door is closed — cards don't write themselves."
            ),
        },
        {
            "key": "mem_gym",
            "name": "Memphis Wrestling Gym",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("memphis", "territory")],
            "extras": {"stat_bonus": "cha", "bonus_amount": 1},
            "desc": (
                "The Memphis wrestling gym sits above a laundromat on Union Avenue. "
                "It's where the boys train during the week and where new talent "
                "gets evaluated. The ring here is smaller than the Coliseum's — "
                "14 feet, tight ropes, forces you to work close.\n\n"
                "Memphis is a talker's territory. The gym wall has a mirror and a "
                "microphone on a stand — promo practice is as important as bumps. "
                "A sign reads: 'IF YOU CAN'T TALK, YOU CAN'T DRAW'.\n\n"
                "|yTraining here gives a Charisma bonus.|n"
            ),
        },
        {
            "key": "mem_beale",
            "name": "Beale Street",
            "typeclass": "typeclasses.rooms.UniqueRoom",
            "tags": [("memphis", "territory")],
            "desc": (
                "Beale Street — the soul of Memphis. Blues music pours out of "
                "every doorway. Neon signs flicker above BBQ joints, juke joints, "
                "and bars that've been here since before anyone alive can remember.\n\n"
                "Wrestlers are minor celebrities here. The locals know the Monday "
                "night guys. A good heel can't walk two blocks without getting "
                "booed by someone who saw the show. A good face gets free drinks. "
                "Memphis is the last territory where kayfabe still lives in the "
                "streets."
            ),
        },
        {
            "key": "mem_studio",
            "name": "Channel 5 TV Studio",
            "typeclass": "typeclasses.rooms.TerritoryRoom",
            "tags": [("memphis", "territory")],
            "extras": {"room_type": "studio"},
            "desc": (
                "The Channel 5 TV studio where Memphis Championship Wrestling "
                "tapes its Saturday morning show. Small studio, two cameras, "
                "the set is just a desk and a backdrop with the MCW logo.\n\n"
                "This is where angles get made. Interview segments, contract "
                "signings, surprise attacks — more careers have been made in "
                "this cramped studio than in the Coliseum ring. If you can get "
                "TV time here, the whole territory sees your face."
            ),
        },
        {
            "key": "mem_office",
            "name": "Promoter's Office",
            "typeclass": "typeclasses.rooms.PromoterOffice",
            "tags": [("memphis", "territory")],
            "extras": {"promoter_name": "Jerry Crowley"},
            "desc": (
                "A cluttered office in the back of the Coliseum. Stacks of "
                "8x10 glossies, a rotary phone, and a calendar with the month's "
                "cards written in pencil (because they change constantly).\n\n"
                "The promoter sits behind a metal desk with a Crown Royal "
                "bottle acting as a paperweight. This is where you get booked, "
                "get paid, or get told you're working the opener for the "
                "foreseeable future."
            ),
        },
        {
            "key": "mem_travel",
            "name": "I-40 / I-55 Interchange",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("memphis", "territory")],
            "extras": {"destinations": ["midsouth", "georgia", "florida", "midatlantic", "pensacola"]},
            "desc": (
                "The interstate interchange where I-40 meets I-55 — Memphis's "
                "gateway to everywhere. East to Nashville, south to Mississippi "
                "and the Gulf, west to the Delta.\n\n"
                "If you've earned your spot in Memphis, the other territories "
                "know your name. If you haven't... well, there's always the "
                "backyard feds.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        # Travel north of arena
        ("north;n", "mem_arena", "mem_travel"),
        ("south;s", "mem_travel", "mem_arena"),
        # Gym west, Beale east of arena
        ("west;w", "mem_arena", "mem_gym"),
        ("east;e", "mem_gym", "mem_arena"),
        ("east;e", "mem_arena", "mem_beale"),
        ("west;w", "mem_beale", "mem_arena"),
        # Backstage south of arena
        ("south;s", "mem_arena", "mem_backstage"),
        ("north;n", "mem_backstage", "mem_arena"),
        # Office west, Studio east of backstage
        ("west;w", "mem_backstage", "mem_office"),
        ("east;e", "mem_office", "mem_backstage"),
        ("east;e", "mem_backstage", "mem_studio"),
        ("west;w", "mem_studio", "mem_backstage"),
    ],
}

# ============================================================
# IMPORT ALL OTHER TERRITORIES
# ============================================================

from world.territories_backyard import BACKYARD_TERRITORIES
from world.territories_schools import SCHOOL_TERRITORIES
from world.territories_regional import REGIONAL_TERRITORIES
from world.territories_developmental import DEVELOPMENTAL_TERRITORIES
from world.territories_national import NATIONAL_TERRITORIES

TERRITORIES.update(BACKYARD_TERRITORIES)
TERRITORIES.update(SCHOOL_TERRITORIES)
TERRITORIES.update(REGIONAL_TERRITORIES)
TERRITORIES.update(DEVELOPMENTAL_TERRITORIES)
TERRITORIES.update(NATIONAL_TERRITORIES)
