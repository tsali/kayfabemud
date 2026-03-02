"""
Kayfabe: Protect the Business — Tier 3.5 Developmental territories.
OVW, FCW, DSW, HWA.
"""

DEVELOPMENTAL_TERRITORIES = {}

# ============================================================
# OVW — Ohio Valley Wrestling (Louisville, KY)
# ============================================================

DEVELOPMENTAL_TERRITORIES["ovw"] = {
    "name": "Ohio Valley Wrestling",
    "abbrev": "OVW",
    "tier": 3.5,
    "location": "Louisville, KY",
    "rooms": [
        {
            "key": "ovw_arena",
            "name": "Davis Arena",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("ovw", "territory"), ("start_ovw", "chargen")],
            "extras": {"capacity": 400},
            "desc": (
                "Davis Arena — OVW's home base in Louisville. A converted "
                "warehouse with bleachers on three sides and a hard camera "
                "on the fourth. The arena seats 400 on a good night.\n\n"
                "This is developmental — the last stop before the national "
                "promotions. Every match is taped, every promo is reviewed, "
                "and Jim Corwin is watching from the back with his arms "
                "crossed and his tennis racket within reach."
            ),
        },
        {
            "key": "ovw_backstage",
            "name": "Davis Arena Backstage",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("ovw", "territory")],
            "desc": (
                "A tight backstage area. The OVW roster is hungry — "
                "everyone here knows they're one good match, one great "
                "promo away from The Call. The tension is palpable.\n\n"
                "Danny Dusk and Al Frost manage the day-to-day. Corwin "
                "manages the creative. The three of them don't always "
                "agree, which keeps things interesting."
            ),
        },
        {
            "key": "ovw_gym",
            "name": "OVW Training Facility",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("ovw", "territory")],
            "extras": {"stat_bonus": "cha", "bonus_amount": 2},
            "desc": (
                "The OVW training facility — a proper gym attached to "
                "Davis Arena. Ring, weights, and most importantly: a "
                "promo room with a camera and monitor.\n\n"
                "OVW's focus is making you TV-ready. Can you cut a promo "
                "that connects through a lens? Can you work a match that "
                "tells a story on a 19-inch screen? That's what matters.\n\n"
                "|yTraining here gives a Charisma bonus.|n"
            ),
        },
        {
            "key": "ovw_corwin",
            "name": "Cornette's Office",
            "typeclass": "typeclasses.rooms.UniqueRoom",
            "tags": [("ovw", "territory")],
            "desc": (
                "Jim Corwin's office at Davis Arena. VHS tapes stacked "
                "floor to ceiling — every OVW show ever taped. A tennis "
                "racket leans against the desk. A whiteboard covered in "
                "booking notes and crossed-out names.\n\n"
                "Corwin is the best mind in the business. His critiques "
                "are brutal, his knowledge is encyclopedic, and if he "
                "says you're ready for the main roster, you're ready. "
                "If he says you're not, God help you."
            ),
        },
        {
            "key": "ovw_frost",
            "name": "Al Frost's Office",
            "typeclass": "typeclasses.rooms.TerritoryRoom",
            "tags": [("ovw", "territory")],
            "desc": (
                "Al Frost's office. A mannequin head sits on the desk — "
                "nobody asks about it. Frost is a veteran who still wrestles "
                "on OVW cards, serving as a gatekeeper. If you can't beat "
                "Frost, you're not ready.\n\n"
                "He's also the co-promoter and the voice of reason when "
                "Corwin goes on one of his legendary rants."
            ),
        },
        {
            "key": "ovw_bar",
            "name": "Louisville Dive Bar",
            "typeclass": "typeclasses.rooms.BarRoom",
            "tags": [("ovw", "territory")],
            "desc": (
                "A no-name bar near the arena where the OVW roster drinks "
                "cheap bourbon and swaps stories. The bartender is a mark "
                "who doesn't realize half his regulars will be on national "
                "TV within a year.\n\n"
                "Developmental is a pressure cooker. This bar is the "
                "release valve."
            ),
        },
        {
            "key": "ovw_travel",
            "name": "Shepherdsville Road",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("ovw", "territory")],
            "extras": {"destinations": ["fhwa", "memphis", "midsouth", "midatlantic", "wwf", "wcw"]},
            "desc": (
                "Shepherdsville Road heads south to I-65. Louisville is "
                "a crossroads — close to every major territory and "
                "within driving distance of both WWF and WCW headquarters.\n\n"
                "When The Call comes, this is the road you'll take.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
        {
            "key": "ovw_hotel",
            "name": "Louisville Budget Hotel",
            "typeclass": "typeclasses.rooms.InnRoom",
            "tags": [("ovw", "territory")],
            "extras": {"inn_tier": 3, "rest_cost": 75, "rest_bonus": {"all": 2}},
            "desc": (
                "A budget hotel near Davis Arena. Developmental pay doesn't "
                "cover luxury, but this place has clean sheets and hot water. "
                "The front desk knows the OVW roster by name.\n\n"
                "Corwin's curfew is 11 PM. The hotel staff doesn't enforce "
                "it, but they do report late arrivals."
            ),
        },
    ],
    "exits": [
        ("north;n", "ovw_arena", "ovw_travel"),
        ("south;s", "ovw_travel", "ovw_arena"),
        ("west;w", "ovw_arena", "ovw_gym"),
        ("east;e", "ovw_gym", "ovw_arena"),
        ("east;e", "ovw_arena", "ovw_bar"),
        ("west;w", "ovw_bar", "ovw_arena"),
        ("south;s", "ovw_arena", "ovw_backstage"),
        ("north;n", "ovw_backstage", "ovw_arena"),
        ("west;w", "ovw_backstage", "ovw_corwin"),
        ("east;e", "ovw_corwin", "ovw_backstage"),
        ("east;e", "ovw_backstage", "ovw_frost"),
        ("west;w", "ovw_frost", "ovw_backstage"),
        ("south;s", "ovw_bar", "ovw_hotel"),
        ("north;n", "ovw_hotel", "ovw_bar"),
    ],
}

# ============================================================
# FCW — Florida Championship Wrestling (Tampa, FL)
# ============================================================

DEVELOPMENTAL_TERRITORIES["fcw"] = {
    "name": "Florida Championship Wrestling",
    "abbrev": "FCW",
    "tier": 3.5,
    "location": "Tampa, FL",
    "rooms": [
        {
            "key": "fcw_arena",
            "name": "FCW Arena",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("fcw", "territory"), ("start_fcw", "chargen")],
            "extras": {"capacity": 300},
            "desc": (
                "The FCW Arena — a converted strip mall space in Tampa. "
                "Fluorescent lights, metal bleachers, and a ring that's "
                "seen better days. The unglamorous reality of developmental "
                "wrestling.\n\n"
                "But every Tuesday night, the cameras roll. FCW TV tapings "
                "are where careers are made. The production truck parked "
                "outside captures everything."
            ),
        },
        {
            "key": "fcw_backstage",
            "name": "FCW Backstage",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("fcw", "territory")],
            "desc": (
                "A cramped backstage area in the strip mall. Folding "
                "chairs and a curtain separate the wrestlers from the "
                "audience. A monitor shows the live camera feed.\n\n"
                "Iron Steve Keirn runs a tight ship. He's an old Florida "
                "territory vet who knows what it takes to survive on TV."
            ),
        },
        {
            "key": "fcw_gym",
            "name": "FCW Training Gym",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("fcw", "territory")],
            "extras": {"stat_bonus": "psy", "bonus_amount": 2},
            "desc": (
                "The FCW gym focuses on camera awareness. A ring with "
                "cameras set up at TV angles. Students practice hitting "
                "marks, looking into the hard camera, and timing their "
                "moves for TV.\n\n"
                "Psychology is everything here — working for a camera "
                "is different from working for a crowd.\n\n"
                "|yTraining here gives a Psychology bonus.|n"
            ),
        },
        {
            "key": "fcw_truck",
            "name": "Production Truck",
            "typeclass": "typeclasses.rooms.UniqueRoom",
            "tags": [("fcw", "territory")],
            "desc": (
                "A production truck parked behind the strip mall. Inside: "
                "monitors showing every camera angle, a switching board, "
                "and a director who calls the shots.\n\n"
                "Students review their matches here — watching themselves "
                "on screen is humbling. The camera sees everything you "
                "thought you were hiding."
            ),
        },
        {
            "key": "fcw_travel",
            "name": "Dale Mabry Highway — FCW Exit",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("fcw", "territory")],
            "extras": {"destinations": ["florida", "dungeon_holds", "pensacola", "wwf", "wcw"]},
            "desc": (
                "Dale Mabry Highway leads to the rest of Tampa and "
                "beyond. FCW is the gateway to the national stage.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
        {
            "key": "fcw_hotel",
            "name": "Tampa Extended Stay",
            "typeclass": "typeclasses.rooms.InnRoom",
            "tags": [("fcw", "territory")],
            "extras": {"inn_tier": 3, "rest_cost": 75, "rest_bonus": {"all": 2}},
            "desc": (
                "An extended-stay hotel near the FCW strip mall. Kitchenettes "
                "with microwaves and mini-fridges. The developmental roster "
                "lives here for months at a time, cooking ramen and dreaming "
                "of the main roster.\n\n"
                "The pool is the one luxury — sore muscles appreciate it."
            ),
        },
    ],
    "exits": [
        ("north;n", "fcw_arena", "fcw_travel"),
        ("south;s", "fcw_travel", "fcw_arena"),
        ("west;w", "fcw_arena", "fcw_gym"),
        ("east;e", "fcw_gym", "fcw_arena"),
        ("east;e", "fcw_arena", "fcw_truck"),
        ("west;w", "fcw_truck", "fcw_arena"),
        ("south;s", "fcw_arena", "fcw_backstage"),
        ("north;n", "fcw_backstage", "fcw_arena"),
        ("east;e", "fcw_backstage", "fcw_hotel"),
        ("west;w", "fcw_hotel", "fcw_backstage"),
    ],
}

# ============================================================
# DSW — Deep South Wrestling (McDonough, GA)
# ============================================================

DEVELOPMENTAL_TERRITORIES["dsw"] = {
    "name": "Deep South Wrestling",
    "abbrev": "DSW",
    "tier": 3.5,
    "location": "McDonough, GA",
    "rooms": [
        {
            "key": "dsw_arena",
            "name": "DSW Warehouse",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("dsw", "territory"), ("start_dsw", "chargen")],
            "extras": {"capacity": 250},
            "desc": (
                "The DSW Warehouse — literally a warehouse in McDonough, "
                "Georgia. Concrete floors, folding chairs, no AC. The "
                "Georgia heat is punishing and Sergeant DeMott considers "
                "that a feature, not a bug.\n\n"
                "DSW separates those who want it from those who don't. "
                "If you can't handle the Warehouse, you can't handle "
                "the pressure of a national promotion."
            ),
        },
        {
            "key": "dsw_backstage",
            "name": "DSW Backstage",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("dsw", "territory")],
            "desc": (
                "A section of the warehouse partitioned with tarps. "
                "No lockers — just hooks on a two-by-four. A cooler of "
                "water (no sports drinks — earn them). A folding table "
                "serves as the trainer's station.\n\n"
                "DeMott's rules are posted on the wall. Rule one: don't "
                "complain. There is no rule two."
            ),
        },
        {
            "key": "dsw_gym",
            "name": "Bill DeMott's Boot Camp",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("dsw", "territory")],
            "extras": {"stat_bonus": "tou", "bonus_amount": 2},
            "desc": (
                "An outdoor training area behind the warehouse. Tires "
                "for flipping, ropes for climbing, a sand pit for bear "
                "crawls. DeMott runs conditioning drills that would make "
                "a Marine cry.\n\n"
                "DSW's focus is physical toughness and ring presence. "
                "You won't learn finesse here — you'll learn to survive.\n\n"
                "|yTraining here gives a Toughness bonus.|n"
            ),
        },
        {
            "key": "dsw_office",
            "name": "DSW Promoter's Office",
            "typeclass": "typeclasses.rooms.PromoterOffice",
            "tags": [("dsw", "territory")],
            "extras": {"promoter_name": "Sergeant Bill DeMott"},
            "desc": (
                "DeMott's office — a corner of the warehouse with a desk "
                "and a single chair. He doesn't invite you to sit. "
                "Meetings are short, direct, and often involve being told "
                "to do 500 squats.\n\n"
                "A whiteboard shows the week's conditioning scores. "
                "Your name had better not be at the bottom."
            ),
        },
        {
            "key": "dsw_travel",
            "name": "I-75 South — McDonough Exit",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("dsw", "territory")],
            "extras": {"destinations": ["georgia", "florida", "psc", "wcw", "wwf"]},
            "desc": (
                "Interstate 75 heads north to Atlanta and south to "
                "Florida. McDonough is close to the Georgia territory "
                "and the WCW headquarters at CNN Center.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
        {
            "key": "dsw_hotel",
            "name": "McDonough Motor Inn",
            "typeclass": "typeclasses.rooms.InnRoom",
            "tags": [("dsw", "territory")],
            "extras": {"inn_tier": 3, "rest_cost": 75, "rest_bonus": {"all": 2}},
            "desc": (
                "A motor inn off I-75. Basic rooms with Georgia heat barely "
                "held at bay by window units. DeMott doesn't care where you "
                "sleep as long as you show up at 6 AM ready to work.\n\n"
                "The vending machine outside has protein bars. Someone "
                "thoughtful restocked it."
            ),
        },
    ],
    "exits": [
        ("north;n", "dsw_arena", "dsw_travel"),
        ("south;s", "dsw_travel", "dsw_arena"),
        ("west;w", "dsw_arena", "dsw_gym"),
        ("east;e", "dsw_gym", "dsw_arena"),
        ("south;s", "dsw_arena", "dsw_backstage"),
        ("north;n", "dsw_backstage", "dsw_arena"),
        ("west;w", "dsw_backstage", "dsw_office"),
        ("east;e", "dsw_office", "dsw_backstage"),
        ("east;e", "dsw_backstage", "dsw_hotel"),
        ("west;w", "dsw_hotel", "dsw_backstage"),
    ],
}

# ============================================================
# HWA — Heartland Wrestling Association (Cincinnati, OH)
# ============================================================

DEVELOPMENTAL_TERRITORIES["hwa"] = {
    "name": "Heartland Wrestling Association",
    "abbrev": "HWA",
    "tier": 3.5,
    "location": "Cincinnati, OH",
    "rooms": [
        {
            "key": "hwa_arena",
            "name": "HWA Sportsplex",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("hwa", "territory"), ("start_hwa", "chargen")],
            "extras": {"capacity": 350},
            "desc": (
                "The HWA Sportsplex — a multi-purpose athletic facility "
                "in Cincinnati that hosts wrestling every Thursday night. "
                "Decent lighting, proper seating, and a ring that Les "
                "Thatcher keeps in immaculate condition.\n\n"
                "HWA is the thinking person's developmental. Less about "
                "physicality, more about psychology, promos, and the "
                "cerebral side of the business."
            ),
        },
        {
            "key": "hwa_backstage",
            "name": "HWA Backstage",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("hwa", "territory")],
            "desc": (
                "A clean, organized backstage area. Thatcher runs HWA "
                "like a school — discipline, respect, and preparation. "
                "Students are expected to arrive early, dressed properly, "
                "and with their promos memorized."
            ),
        },
        {
            "key": "hwa_gym",
            "name": "Les Thatcher's Classroom",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("hwa", "territory")],
            "extras": {"stat_bonus": "cha", "bonus_amount": 2},
            "desc": (
                "A literal classroom with a chalkboard, TV monitor, "
                "lectern, and rows of folding chairs. Thatcher teaches "
                "match psychology like a professor — with lectures, "
                "tape study, and assigned homework.\n\n"
                "A practice ring sits adjacent, but most of the learning "
                "happens in this room. The best CHA and PSY training in "
                "the game.\n\n"
                "|yTraining here gives a Charisma bonus.|n"
            ),
        },
        {
            "key": "hwa_interview",
            "name": "Interview Set",
            "typeclass": "typeclasses.rooms.UniqueRoom",
            "tags": [("hwa", "territory")],
            "desc": (
                "A camera and backdrop set up for promo practice. "
                "Students stand at the mark, look into the lens, and "
                "deliver. Thatcher sits behind the camera with a buzzer "
                "— if your promo loses focus, he buzzes you.\n\n"
                "Surviving three minutes without getting buzzered is "
                "the first milestone. Some students take weeks to get "
                "there."
            ),
        },
        {
            "key": "hwa_bar",
            "name": "Cincinnati Bar",
            "typeclass": "typeclasses.rooms.BarRoom",
            "tags": [("hwa", "territory")],
            "desc": (
                "A neighborhood bar near the Sportsplex. Midwestern "
                "honest — cheap beer, bar food, and a jukebox with too "
                "much classic rock. The HWA roster gathers here after "
                "shows.\n\n"
                "Thatcher occasionally joins for a beer. When he does, "
                "it turns into an impromptu seminar on match psychology "
                "that's worth more than any training session."
            ),
        },
        {
            "key": "hwa_travel",
            "name": "I-71 / I-75 Interchange",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("hwa", "territory")],
            "extras": {"destinations": ["ovw", "fhwa", "midatlantic", "awa", "wwf", "wcw"]},
            "desc": (
                "Cincinnati's interchange connects to Louisville (OVW), "
                "Columbus, Cleveland, and the Northeast corridor. "
                "The Midwest developmental pipeline runs through here.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
        {
            "key": "hwa_hotel",
            "name": "Cincinnati Comfort Inn",
            "typeclass": "typeclasses.rooms.InnRoom",
            "tags": [("hwa", "territory")],
            "extras": {"inn_tier": 3, "rest_cost": 75, "rest_bonus": {"all": 2}},
            "desc": (
                "A comfort inn near the Sportsplex. Midwestern reliable — "
                "clean rooms, firm beds, and a continental breakfast that "
                "includes actual eggs. Thatcher approves.\n\n"
                "The lobby has a TV permanently tuned to wrestling reruns. "
                "The night manager is a mark who asks for autographs."
            ),
        },
    ],
    "exits": [
        ("north;n", "hwa_arena", "hwa_travel"),
        ("south;s", "hwa_travel", "hwa_arena"),
        ("west;w", "hwa_arena", "hwa_gym"),
        ("east;e", "hwa_gym", "hwa_arena"),
        ("east;e", "hwa_arena", "hwa_bar"),
        ("west;w", "hwa_bar", "hwa_arena"),
        ("south;s", "hwa_arena", "hwa_backstage"),
        ("north;n", "hwa_backstage", "hwa_arena"),
        ("east;e", "hwa_backstage", "hwa_interview"),
        ("west;w", "hwa_interview", "hwa_backstage"),
        ("south;s", "hwa_bar", "hwa_hotel"),
        ("north;n", "hwa_hotel", "hwa_bar"),
    ],
}
