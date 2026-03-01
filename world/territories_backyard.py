"""
Kayfabe: Protect the Business — Tier 1 Backyard Fed territories (BBA, PSC, GSG, LSU).
FHWA and GCCW are in the main territories.py.
"""

BACKYARD_TERRITORIES = {}

# ============================================================
# BBA — Bayou Brawling Alliance (Shreveport, LA)
# ============================================================

BACKYARD_TERRITORIES["bba"] = {
    "name": "Bayou Brawling Alliance",
    "abbrev": "BBA",
    "tier": 1,
    "location": "Shreveport, LA",
    "rooms": [
        {
            "key": "bba_parking",
            "name": "BBA Parking Lot",
            "typeclass": "typeclasses.rooms.BackyardFedRoom",
            "tags": [("bba", "territory"), ("start_bba", "chargen")],
            "desc": (
                "A muddy field behind a tin-roofed barn on the outskirts of "
                "Shreveport. Pickup trucks with Louisiana plates line the "
                "tree line. Mosquitoes the size of quarters patrol the air.\n\n"
                "A hand-spray-painted banner on a bedsheet reads: "
                "'BBA — BAYOU BRAWLIN' — TONIGHT'. A cooler of Abita beer "
                "sits in the bed of someone's truck. The sound of bodies "
                "hitting plywood carries through the humid night air."
            ),
        },
        {
            "key": "bba_venue",
            "name": "The Barn — BBA Arena",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("bba", "territory")],
            "extras": {"capacity": 40},
            "desc": (
                "An honest-to-God barn converted into a wrestling venue. "
                "Hay bales serve as seating. The ring is built from lumber "
                "and ropes strung between four telephone poles sunk in "
                "concrete. The canvas is a tarp stretched tight.\n\n"
                "The crowd is rowdy — these are oil field workers and "
                "swamp people who want to see a fight. A single bare bulb "
                "swings above the ring. Someone brought a camcorder but "
                "the lens keeps fogging in the humidity."
            ),
        },
        {
            "key": "bba_locker",
            "name": "The Stalls — Locker Area",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("bba", "territory")],
            "desc": (
                "The 'locker room' is a row of horse stalls in the back of "
                "the barn. It smells like hay and old leather. Wrestlers "
                "change behind blankets hung from the rafters.\n\n"
                "The conditions are brutal but the competition is stiffer "
                "than you'd expect. These boys hit hard and stiff — "
                "Shreveport style doesn't believe in pulling punches."
            ),
        },
        {
            "key": "bba_road",
            "name": "I-20 West — Heading Out",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("bba", "territory")],
            "extras": {"destinations": ["fhwa", "gccw", "psc", "gsg", "lsu", "proving_grounds", "midsouth"]},
            "desc": (
                "Interstate 20 stretches west toward Texas and east toward "
                "Mississippi. Shreveport sits right in the middle of "
                "wrestling country — Mid-South territory is close.\n\n"
                "If someone from the Proving Grounds or Mid-South has seen "
                "your work, the road opens up. Otherwise, it's another "
                "night in the barn.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("parking", "bba_parking", "bba_venue"),
        ("barn", "bba_parking", "bba_venue"),
        ("locker", "bba_venue", "bba_locker"),
        ("stalls", "bba_venue", "bba_locker"),
        ("ring", "bba_locker", "bba_venue"),
        ("out", "bba_venue", "bba_parking"),
        ("road", "bba_parking", "bba_road"),
        ("back", "bba_road", "bba_parking"),
    ],
}

# ============================================================
# PSC — Peach State Championship (Macon, GA)
# ============================================================

BACKYARD_TERRITORIES["psc"] = {
    "name": "Peach State Championship",
    "abbrev": "PSC",
    "tier": 1,
    "location": "Macon, GA",
    "rooms": [
        {
            "key": "psc_parking",
            "name": "PSC Parking Lot",
            "typeclass": "typeclasses.rooms.BackyardFedRoom",
            "tags": [("psc", "territory"), ("start_psc", "chargen")],
            "desc": (
                "A cracked asphalt lot behind the Macon American Legion hall. "
                "Peach trees line the fence. Georgia heat shimmers off the "
                "blacktop even after sundown.\n\n"
                "A posterboard sign duct-taped to a sawhorse reads: "
                "'PSC WRESTLING — ADMISSION $5 — KIDS FREE'. A few dozen "
                "cars sit in the lot. Someone's selling boiled peanuts from "
                "the tailgate of a station wagon."
            ),
        },
        {
            "key": "psc_venue",
            "name": "American Legion Hall — PSC Arena",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("psc", "territory")],
            "extras": {"capacity": 75},
            "desc": (
                "The American Legion hall doubles as the PSC's home base. "
                "A decent ring sits in the center — reportedly bought from "
                "a defunct Georgia Championship Wrestling show. The ropes "
                "are real, the turnbuckles padded.\n\n"
                "The crowd skews older — people who remember watching TBS "
                "studio wrestling. They know what good work looks like and "
                "they expect it. National TV territory Georgia is just up "
                "I-75, and scouts from TBS sometimes pass through Macon."
            ),
        },
        {
            "key": "psc_locker",
            "name": "Kitchen — Locker Area",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("psc", "territory")],
            "desc": (
                "The Legion hall kitchen serves as the locker room. "
                "Wrestlers change between the industrial sink and the "
                "walk-in cooler (which mercifully still works). A folding "
                "table holds rolls of athletic tape and a first aid kit.\n\n"
                "The boys here are talkers — PSC is a promo territory. "
                "If you can work the mic, you'll get noticed. If you can't, "
                "you'll spend every show in the opener."
            ),
        },
        {
            "key": "psc_road",
            "name": "I-75 North — Heading Out",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("psc", "territory")],
            "extras": {"destinations": ["fhwa", "gccw", "bba", "gsg", "lsu", "conservatory", "georgia"]},
            "desc": (
                "Interstate 75 runs north to Atlanta and the Georgia "
                "territory — national TV, TBS studios, the big time. "
                "South leads to Florida and the Conservatory.\n\n"
                "Macon is close enough to Atlanta that a good VHS tape "
                "can get you noticed fast. The question is whether you're "
                "ready for what comes next.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("parking", "psc_parking", "psc_venue"),
        ("hall", "psc_parking", "psc_venue"),
        ("locker", "psc_venue", "psc_locker"),
        ("kitchen", "psc_venue", "psc_locker"),
        ("ring", "psc_locker", "psc_venue"),
        ("out", "psc_venue", "psc_parking"),
        ("road", "psc_parking", "psc_road"),
        ("back", "psc_road", "psc_parking"),
    ],
}

# ============================================================
# GSG — Garden State Grappling (Vineland, NJ)
# ============================================================

BACKYARD_TERRITORIES["gsg"] = {
    "name": "Garden State Grappling",
    "abbrev": "GSG",
    "tier": 1,
    "location": "Vineland, NJ",
    "rooms": [
        {
            "key": "gsg_parking",
            "name": "GSG Parking Lot",
            "typeclass": "typeclasses.rooms.BackyardFedRoom",
            "tags": [("gsg", "territory"), ("start_gsg", "chargen")],
            "desc": (
                "A strip mall parking lot in Vineland, New Jersey. The "
                "Garden State Grappling runs out of a rented storefront "
                "between a nail salon and a check-cashing place.\n\n"
                "Despite the humble setting, the proximity to New York "
                "makes this the most competitive backyard fed in the game. "
                "WWF scouts have been known to drive down from the city. "
                "A hand-lettered sign in the window reads: 'GSG — LIVE "
                "WRESTLING — FRIDAY NIGHTS'."
            ),
        },
        {
            "key": "gsg_venue",
            "name": "The Storefront — GSG Arena",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("gsg", "territory")],
            "extras": {"capacity": 60},
            "desc": (
                "A gutted retail space with a ring jammed into the center. "
                "The drop ceiling tiles have been removed to give enough "
                "headroom for top-rope moves. Fluorescent lights buzz "
                "overhead.\n\n"
                "The crowd is mostly Jersey guys who think they know the "
                "business — smart marks who'll chant 'boring' if you rest "
                "too long. A VHS camera on a tripod captures every show. "
                "Larry Sharpton from the Beast Works sometimes sends a "
                "student to scout."
            ),
        },
        {
            "key": "gsg_locker",
            "name": "Back Room — Locker Area",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("gsg", "territory")],
            "desc": (
                "The back room of the storefront. Old retail shelving holds "
                "duffel bags and gear. A bathroom with a cracked mirror "
                "serves as the only private changing area.\n\n"
                "Competition here is cutthroat — everyone knows the Beast "
                "Works and WWF are close. Wrestlers sabotage each other's "
                "gear, steal each other's spots, and politic constantly. "
                "Welcome to the Northeast."
            ),
        },
        {
            "key": "gsg_road",
            "name": "Route 55 North — Heading Out",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("gsg", "territory")],
            "extras": {"destinations": ["fhwa", "gccw", "bba", "psc", "lsu", "beast_works", "wwf"]},
            "desc": (
                "Route 55 heads north toward the Turnpike and eventually "
                "New York City — Madison Square Garden, the WWF, the "
                "biggest stage in wrestling.\n\n"
                "The Beast Works in Westville is just 20 minutes away. "
                "If Larry Sharpton sees something in you, that's your "
                "ticket to the Northeast wrestling pipeline.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("parking", "gsg_parking", "gsg_venue"),
        ("storefront", "gsg_parking", "gsg_venue"),
        ("locker", "gsg_venue", "gsg_locker"),
        ("back", "gsg_venue", "gsg_locker"),
        ("ring", "gsg_locker", "gsg_venue"),
        ("out", "gsg_venue", "gsg_parking"),
        ("road", "gsg_parking", "gsg_road"),
        ("back", "gsg_road", "gsg_parking"),
    ],
}

# ============================================================
# LSU — Lone Star Underground (Fort Worth, TX)
# ============================================================

BACKYARD_TERRITORIES["lsu"] = {
    "name": "Lone Star Underground",
    "abbrev": "LSU",
    "tier": 1,
    "location": "Fort Worth, TX",
    "rooms": [
        {
            "key": "lsu_parking",
            "name": "LSU Parking Lot",
            "typeclass": "typeclasses.rooms.BackyardFedRoom",
            "tags": [("lsu", "territory"), ("start_lsu", "chargen")],
            "desc": (
                "A dusty lot behind the Stockyards, Fort Worth. Pickup "
                "trucks with longhorn hood ornaments and Lone Star bumper "
                "stickers crowd the unpaved lot. Texas heat radiates from "
                "the dirt even at night.\n\n"
                "A plywood sign reads: 'LSU — LONE STAR UNDERGROUND — "
                "NO RULES, NO SCRIPT'. The Lone Star Underground has no "
                "training school pipeline — you either get spotted by "
                "World Class territory or you sink. Sink or swim, Texas "
                "style."
            ),
        },
        {
            "key": "lsu_venue",
            "name": "Stockyard Arena — LSU Ring",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("lsu", "territory")],
            "extras": {"capacity": 80},
            "desc": (
                "A converted livestock auction barn. The ring sits where "
                "cattle used to be sold. Metal bleachers on three sides, "
                "a wooden fence on the fourth where the cowboys lean.\n\n"
                "The crowd is loud, drunk, and expects action. Texas "
                "wrestling fans are emotionally invested — they'll throw "
                "beer at heels and chant for faces. World Class territory "
                "in Dallas is just 30 miles east, and the Von Adler family "
                "has eyes everywhere."
            ),
        },
        {
            "key": "lsu_locker",
            "name": "Tack Room — Locker Area",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("lsu", "territory")],
            "desc": (
                "The tack room — where they used to store saddles and "
                "bridles — now holds duffel bags and wrestling boots. "
                "It smells like leather and horse. A bare bulb hangs from "
                "the ceiling.\n\n"
                "No training school feeds into LSU. If you're here, you "
                "learned on your own or from someone's backyard. The good "
                "news: World Class territory scouts regularly. The bad "
                "news: they only want the best."
            ),
        },
        {
            "key": "lsu_road",
            "name": "I-30 East — Heading Out",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("lsu", "territory")],
            "extras": {"destinations": ["fhwa", "gccw", "bba", "psc", "gsg", "wccw"]},
            "desc": (
                "Interstate 30 heads east to Dallas and World Class "
                "territory — the Sportatorium, the Von Adlers, Friday "
                "Night Star Wars on TV.\n\n"
                "No training school in between — you go straight from "
                "the Stockyards to the big time or you don't go at all. "
                "That's the Texas way.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("parking", "lsu_parking", "lsu_venue"),
        ("arena", "lsu_parking", "lsu_venue"),
        ("locker", "lsu_venue", "lsu_locker"),
        ("tack", "lsu_venue", "lsu_locker"),
        ("ring", "lsu_locker", "lsu_venue"),
        ("out", "lsu_venue", "lsu_parking"),
        ("road", "lsu_parking", "lsu_road"),
        ("back", "lsu_road", "lsu_parking"),
    ],
}
