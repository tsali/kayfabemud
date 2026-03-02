"""
Kayfabe: Protect the Business — Tier 2 Training School territories.
Pensacola is in the main territories.py. These are the 5 additional schools.
"""

SCHOOL_TERRITORIES = {}

# ============================================================
# SLAUGHTERHOUSE — Viktor Kovalenko's (North Andover, MA)
# Based on Killer Kowalski's Institute
# ============================================================

SCHOOL_TERRITORIES["slaughterhouse"] = {
    "name": "Viktor Kovalenko's Slaughterhouse",
    "abbrev": "Slaughterhouse",
    "tier": 2,
    "location": "North Andover, MA",
    "rooms": [
        {
            "key": "slaught_entrance",
            "name": "Slaughterhouse — Entrance",
            "typeclass": "typeclasses.rooms.TrainingSchoolRoom",
            "tags": [("slaughterhouse", "territory"), ("start_slaughterhouse", "chargen")],
            "desc": (
                "A converted warehouse in an industrial park off Route 114. "
                "The sign above the loading dock reads: 'KOVALENKO WRESTLING "
                "ACADEMY' in faded red paint. Below it, someone has scrawled "
                "'THE SLAUGHTERHOUSE' in black marker.\n\n"
                "New England cold seeps through the cinderblock walls. "
                "Viktor Kovalenko built champions here — if you survive "
                "his training, you can survive anything."
            ),
        },
        {
            "key": "slaught_floor",
            "name": "Slaughterhouse — Training Floor",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("slaughterhouse", "territory")],
            "extras": {"stat_bonus": "str", "bonus_amount": 2},
            "desc": (
                "The main training floor is a cavernous warehouse space. "
                "Two rings sit side by side — one with tight ropes for "
                "beginners, one with standard tension for advanced students. "
                "Heavy bags and free weights line the walls.\n\n"
                "Kovalenko's method is old-school brutality. Strength and "
                "toughness above all. If you can't lift your opponent, you "
                "can't wrestle your opponent.\n\n"
                "|yTraining here gives a Strength bonus.|n"
            ),
        },
        {
            "key": "slaught_ring",
            "name": "Slaughterhouse — The Ring",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("slaughterhouse", "territory")],
            "extras": {"capacity": 30},
            "desc": (
                "The main ring where students spar under Kovalenko's "
                "merciless eye. The canvas is stained with years of sweat "
                "and the occasional drop of blood. The ropes are regulation "
                "taut.\n\n"
                "A folding chair sits in the corner — Kovalenko's throne. "
                "When he stands up, everyone stops. When he nods, you know "
                "you did something right. It doesn't happen often."
            ),
        },
        {
            "key": "slaught_office",
            "name": "Kovalenko's Office",
            "typeclass": "typeclasses.rooms.TerritoryRoom",
            "tags": [("slaughterhouse", "territory")],
            "desc": (
                "A cramped office at the back of the warehouse. Photos of "
                "Kovalenko's greatest students cover every wall — world "
                "champions, main eventers, legends. A heavy wooden desk "
                "holds stacks of VHS tapes labeled with student names.\n\n"
                "The man himself is intimidating even seated. Six-foot-seven "
                "and still built like a freight train. He doesn't waste words."
            ),
        },
        {
            "key": "slaught_road",
            "name": "Route 114 — Heading Out",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("slaughterhouse", "territory")],
            "extras": {"destinations": ["gsg", "fhwa", "beast_works", "wwf", "midatlantic"]},
            "desc": (
                "Route 114 connects to I-93 and the highways that lead to "
                "New York, Philly, and the Northeast wrestling circuit. "
                "The WWF's home turf is just a few hours south.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
        {
            "key": "slaught_motel",
            "name": "Route 114 Motor Inn",
            "typeclass": "typeclasses.rooms.InnRoom",
            "tags": [("slaughterhouse", "territory")],
            "extras": {"inn_tier": 2, "rest_cost": 25, "rest_bonus": {"all": 1}},
            "desc": (
                "A budget motel on Route 114. New England winter seeps "
                "through the single-pane windows. The heater clanks like a "
                "body hitting canvas. At least the water's hot.\n\n"
                "Kovalenko's students crash here between training sessions. "
                "The beds are hard — almost as hard as the training."
            ),
        },
    ],
    "exits": [
        ("north;n", "slaught_entrance", "slaught_road"),
        ("south;s", "slaught_road", "slaught_entrance"),
        ("south;s", "slaught_entrance", "slaught_floor"),
        ("north;n", "slaught_floor", "slaught_entrance"),
        ("east;e", "slaught_floor", "slaught_ring"),
        ("west;w", "slaught_ring", "slaught_floor"),
        ("west;w", "slaught_floor", "slaught_office"),
        ("east;e", "slaught_office", "slaught_floor"),
        ("east;e", "slaught_entrance", "slaught_motel"),
        ("west;w", "slaught_motel", "slaught_entrance"),
    ],
}

# ============================================================
# BEAST WORKS — Larry Sharpton's (Westville, NJ)
# Based on Monster Factory
# ============================================================

SCHOOL_TERRITORIES["beast_works"] = {
    "name": "The Beast Works",
    "abbrev": "Beast Works",
    "tier": 2,
    "location": "Westville, NJ",
    "rooms": [
        {
            "key": "beast_entrance",
            "name": "Beast Works — Entrance",
            "typeclass": "typeclasses.rooms.TrainingSchoolRoom",
            "tags": [("beast_works", "territory"), ("start_beast_works", "chargen")],
            "desc": (
                "A squat concrete building in Westville, New Jersey. The "
                "sign reads: 'THE BEAST WORKS — PROFESSIONAL WRESTLING "
                "TRAINING'. A parking lot full of beaters and one black "
                "Cadillac (Larry Sharpton's).\n\n"
                "The Beast Works is the pipeline to WWF and Mid-Atlantic. "
                "Sharpton builds big men — power wrestlers who fill arenas. "
                "If you're under six feet, you'd better be twice as tough."
            ),
        },
        {
            "key": "beast_floor",
            "name": "Beast Works — Training Floor",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("beast_works", "territory")],
            "extras": {"stat_bonus": "tou", "bonus_amount": 2},
            "desc": (
                "The training floor is dominated by a regulation ring and "
                "an Olympic weight set that would make a powerlifter weep. "
                "Sharpton's philosophy: size matters. The walls are lined "
                "with mirrors so students can watch their form.\n\n"
                "A heavy bag hangs in the corner, beaten into submission "
                "by generations of students. The floor is rubber matting "
                "over concrete — falls here teach you to land right.\n\n"
                "|yTraining here gives a Toughness bonus.|n"
            ),
        },
        {
            "key": "beast_ring",
            "name": "Beast Works — The Ring",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("beast_works", "territory")],
            "extras": {"capacity": 25},
            "desc": (
                "The Beast Works ring — where students prove they belong. "
                "Sharpton runs a weekly in-house show for friends and "
                "family, giving students match experience before sending "
                "them to the independents.\n\n"
                "The ring itself is standard — but Sharpton's standards "
                "are not. He expects power moves executed perfectly. "
                "Sloppy work gets you sent home."
            ),
        },
        {
            "key": "beast_road",
            "name": "Route 130 — Heading Out",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("beast_works", "territory")],
            "extras": {"destinations": ["gsg", "fhwa", "slaughterhouse", "wwf", "midatlantic", "ecw"]},
            "desc": (
                "Route 130 heads north toward Philadelphia and the "
                "ECW territory, or south toward the independents. "
                "The Turnpike connects to New York and the WWF.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
        {
            "key": "beast_motel",
            "name": "Westville Budget Inn",
            "typeclass": "typeclasses.rooms.InnRoom",
            "tags": [("beast_works", "territory")],
            "extras": {"inn_tier": 2, "rest_cost": 25, "rest_bonus": {"all": 1}},
            "desc": (
                "A budget inn in Westville, just down the road from the Beast "
                "Works. The rooms are cramped but functional. Sharpton's students "
                "share doubles to save money.\n\n"
                "The front desk has a bowl of aspirin by the register. They know "
                "their clientele."
            ),
        },
    ],
    "exits": [
        ("north;n", "beast_entrance", "beast_road"),
        ("south;s", "beast_road", "beast_entrance"),
        ("south;s", "beast_entrance", "beast_floor"),
        ("north;n", "beast_floor", "beast_entrance"),
        ("east;e", "beast_floor", "beast_ring"),
        ("west;w", "beast_ring", "beast_floor"),
        ("east;e", "beast_entrance", "beast_motel"),
        ("west;w", "beast_motel", "beast_entrance"),
    ],
}

# ============================================================
# CONSERVATORY — Dory Funk Sr.'s (Ocala, FL)
# Based on Funkin' Conservatory
# ============================================================

SCHOOL_TERRITORIES["conservatory"] = {
    "name": "The Conservatory",
    "abbrev": "Conservatory",
    "tier": 2,
    "location": "Ocala, FL",
    "rooms": [
        {
            "key": "cons_entrance",
            "name": "Conservatory — Entrance",
            "typeclass": "typeclasses.rooms.TrainingSchoolRoom",
            "tags": [("conservatory", "territory"), ("start_conservatory", "chargen")],
            "desc": (
                "A converted horse ranch outside Ocala, Florida. White "
                "fences and live oaks frame a metal building with a sign: "
                "'THE CONSERVATORY — DORY FUNK SR. — PROFESSIONAL WRESTLING "
                "TRAINING'. Horses graze in the adjacent pasture.\n\n"
                "The Conservatory teaches the art of chain wrestling — "
                "holds, counters, reversals. Technical mastery above all."
            ),
        },
        {
            "key": "cons_floor",
            "name": "Conservatory — Training Floor",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("conservatory", "territory")],
            "extras": {"stat_bonus": "tec", "bonus_amount": 2},
            "desc": (
                "The training floor is immaculate — Dory keeps it clean "
                "as a surgical theater. One ring, regulation size, with "
                "ropes set to competition tension. A wrestling mat covers "
                "the floor for ground work.\n\n"
                "Dory teaches chain wrestling: lockup to wristlock to "
                "hammerlock to takedown to ride. Every link in the chain "
                "must be perfect. Speed comes from repetition, not from "
                "shortcuts.\n\n"
                "|yTraining here gives a Technical bonus.|n"
            ),
        },
        {
            "key": "cons_ring",
            "name": "Conservatory — The Ring",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("conservatory", "territory")],
            "extras": {"capacity": 20},
            "desc": (
                "The Conservatory ring — where theory becomes practice. "
                "Students work 15-minute matches focused entirely on "
                "technical wrestling. No brawling, no shortcuts.\n\n"
                "Dory sits on a stool by the apron, calling out holds "
                "for students to execute in sequence. 'Wristlock! Counter! "
                "Go-behind! Takedown!' The rhythm becomes second nature."
            ),
        },
        {
            "key": "cons_road",
            "name": "I-75 — Heading Out",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("conservatory", "territory")],
            "extras": {"destinations": ["psc", "gccw", "pensacola", "florida", "georgia", "wccw"]},
            "desc": (
                "Interstate 75 connects Ocala to Tampa (Florida territory), "
                "Atlanta (Georgia territory), and beyond. The Conservatory's "
                "graduates are sought by technical-heavy territories.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
        {
            "key": "cons_motel",
            "name": "Ocala Country Inn",
            "typeclass": "typeclasses.rooms.InnRoom",
            "tags": [("conservatory", "territory")],
            "extras": {"inn_tier": 2, "rest_cost": 25, "rest_bonus": {"all": 1}},
            "desc": (
                "A country inn on the road outside Ocala. Horses graze in the "
                "pasture across the street. The rooms smell like hay and "
                "wildflowers. It's almost peaceful.\n\n"
                "Dory Funk's students stay here when they can afford it. The "
                "alternative is sleeping on the ranch, which isn't bad either."
            ),
        },
    ],
    "exits": [
        ("north;n", "cons_entrance", "cons_road"),
        ("south;s", "cons_road", "cons_entrance"),
        ("south;s", "cons_entrance", "cons_floor"),
        ("north;n", "cons_floor", "cons_entrance"),
        ("east;e", "cons_floor", "cons_ring"),
        ("west;w", "cons_ring", "cons_floor"),
        ("east;e", "cons_entrance", "cons_motel"),
        ("west;w", "cons_motel", "cons_entrance"),
    ],
}

# ============================================================
# DUNGEON OF HOLDS — Boris Malenko's (Tampa, FL)
# Based on Malenko School
# ============================================================

SCHOOL_TERRITORIES["dungeon_holds"] = {
    "name": "The Dungeon of Holds",
    "abbrev": "Dungeon",
    "tier": 2,
    "location": "Tampa, FL",
    "rooms": [
        {
            "key": "dung_entrance",
            "name": "Dungeon of Holds — Entrance",
            "typeclass": "typeclasses.rooms.TrainingSchoolRoom",
            "tags": [("dungeon_holds", "territory"), ("start_dungeon_holds", "chargen")],
            "desc": (
                "A basement entrance beneath a strip mall in Tampa. Concrete "
                "steps lead down to a heavy metal door with a hand-painted "
                "sign: 'MALENKO SCHOOL OF WRESTLING — THE DUNGEON OF HOLDS'. "
                "The air gets cooler and damper as you descend.\n\n"
                "Boris Malenko teaches catch wrestling — the real thing, "
                "not the worked version. Submissions, joint locks, and the "
                "science of making someone tap."
            ),
        },
        {
            "key": "dung_floor",
            "name": "The Dungeon — Training Floor",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("dungeon_holds", "territory")],
            "extras": {"stat_bonus": "tec", "bonus_amount": 2},
            "desc": (
                "The Dungeon lives up to its name. A low-ceilinged basement "
                "with a ring crammed into the space, mats covering every "
                "inch of floor, and anatomy charts on the walls showing "
                "every joint and pressure point.\n\n"
                "Malenko's method is scientific. He teaches the names of "
                "bones as he demonstrates holds that leverage them. You'll "
                "learn 200 submissions before you learn your first slam.\n\n"
                "|yTraining here gives a Technical bonus.|n"
            ),
        },
        {
            "key": "dung_ring",
            "name": "The Dungeon — Submission Ring",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("dungeon_holds", "territory")],
            "extras": {"capacity": 15},
            "desc": (
                "A ring set up specifically for submission practice. The "
                "ropes are loose — Malenko doesn't want students relying "
                "on rope breaks. You escape a hold with technique or you "
                "tap. No shortcuts.\n\n"
                "The walls display photos of Malenko's students: Dean "
                "Malone, the Guerrera family, dozens of Florida territory "
                "grapplers who learned their craft in this basement."
            ),
        },
        {
            "key": "dung_road",
            "name": "Dale Mabry Highway — Heading Out",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("dungeon_holds", "territory")],
            "extras": {"destinations": ["gccw", "pensacola", "conservatory", "florida", "fcw"]},
            "desc": (
                "Dale Mabry Highway runs through Tampa, connecting to "
                "the Florida territory and the FCW developmental. "
                "Malenko's students are prized in any territory that "
                "values ring work.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
        {
            "key": "dung_motel",
            "name": "Tampa Budget Suites",
            "typeclass": "typeclasses.rooms.InnRoom",
            "tags": [("dungeon_holds", "territory")],
            "extras": {"inn_tier": 2, "rest_cost": 25, "rest_bonus": {"all": 1}},
            "desc": (
                "A budget extended-stay near Dale Mabry Highway. The rooms "
                "have kitchenettes with microwaves older than most of the "
                "trainees. The pool hasn't been cleaned in weeks.\n\n"
                "Malenko's students recover here between sessions, soaking "
                "their wrenched joints in epsom salt baths."
            ),
        },
    ],
    "exits": [
        ("north;n", "dung_entrance", "dung_road"),
        ("south;s", "dung_road", "dung_entrance"),
        ("south;s", "dung_entrance", "dung_floor"),
        ("north;n", "dung_floor", "dung_entrance"),
        ("east;e", "dung_floor", "dung_ring"),
        ("west;w", "dung_ring", "dung_floor"),
        ("east;e", "dung_entrance", "dung_motel"),
        ("west;w", "dung_motel", "dung_entrance"),
    ],
}

# ============================================================
# PROVING GROUNDS — Harley Reece's (Eldon, MO)
# Based on Harley Race Academy
# ============================================================

SCHOOL_TERRITORIES["proving_grounds"] = {
    "name": "The Proving Grounds",
    "abbrev": "Proving Grounds",
    "tier": 2,
    "location": "Eldon, MO",
    "rooms": [
        {
            "key": "prov_entrance",
            "name": "Proving Grounds — Entrance",
            "typeclass": "typeclasses.rooms.TrainingSchoolRoom",
            "tags": [("proving_grounds", "territory"), ("start_proving_grounds", "chargen")],
            "desc": (
                "A sprawling facility on the outskirts of Eldon, Missouri. "
                "The sign reads: 'HARLEY REECE WRESTLING ACADEMY — THE "
                "PROVING GROUNDS'. An NWA World Championship banner hangs "
                "above the entrance.\n\n"
                "Reece is a seven-time world champion. He teaches the "
                "NWA style: all-around wrestling where you need strength, "
                "technique, and psychology. No specialists here — you "
                "learn everything or you learn nothing."
            ),
        },
        {
            "key": "prov_floor",
            "name": "Proving Grounds — Training Floor",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("proving_grounds", "territory")],
            "extras": {"stat_bonus": "psy", "bonus_amount": 2},
            "desc": (
                "A professional-grade training facility. Two rings, a full "
                "weight room, and a classroom area with a TV and VCR for "
                "studying tape. Reece's approach is cerebral — he teaches "
                "psychology as much as physicality.\n\n"
                "'A match is a story,' he says. 'If you can't tell a story "
                "in that ring, all the muscles in the world won't save you.'\n\n"
                "|yTraining here gives a Psychology bonus.|n"
            ),
        },
        {
            "key": "prov_ring",
            "name": "Proving Grounds — The Ring",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("proving_grounds", "territory")],
            "extras": {"capacity": 40},
            "desc": (
                "The main ring at the Proving Grounds. Reece holds monthly "
                "shows that draw from Kansas City, St. Louis, and the "
                "entire Midwest. AWA and Mid-South scouts are regulars.\n\n"
                "The ring is surrounded by chairs and a simple announce "
                "table. No frills. The work speaks for itself."
            ),
        },
        {
            "key": "prov_road",
            "name": "Highway 54 — Heading Out",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("proving_grounds", "territory")],
            "extras": {"destinations": ["bba", "fhwa", "awa", "midsouth", "memphis"]},
            "desc": (
                "Highway 54 winds through the Missouri Ozarks, connecting "
                "to I-70 and the heartland territories. AWA in Minneapolis, "
                "Mid-South in Shreveport, Memphis — all within driving "
                "distance.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
        {
            "key": "prov_motel",
            "name": "Eldon Motor Lodge",
            "typeclass": "typeclasses.rooms.InnRoom",
            "tags": [("proving_grounds", "territory")],
            "extras": {"inn_tier": 2, "rest_cost": 25, "rest_bonus": {"all": 1}},
            "desc": (
                "A small motor lodge in Eldon, Missouri. The Ozark hills "
                "roll outside the window. A Bible and a Harley Reece "
                "autographed photo sit on the nightstand.\n\n"
                "Reece's students stay here when the academy dorms are full. "
                "The owner gives a wrestler's discount — he's been a fan "
                "since the NWA days."
            ),
        },
    ],
    "exits": [
        ("north;n", "prov_entrance", "prov_road"),
        ("south;s", "prov_road", "prov_entrance"),
        ("south;s", "prov_entrance", "prov_floor"),
        ("north;n", "prov_floor", "prov_entrance"),
        ("east;e", "prov_floor", "prov_ring"),
        ("west;w", "prov_ring", "prov_floor"),
        ("east;e", "prov_entrance", "prov_motel"),
        ("west;w", "prov_motel", "prov_entrance"),
    ],
}
