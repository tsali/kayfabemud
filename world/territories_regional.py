"""
Kayfabe: Protect the Business — Tier 3 Regional territories.
Memphis is in the main territories.py. These are the 8 remaining regionals.
"""

REGIONAL_TERRITORIES = {}

# ============================================================
# MID-SOUTH (Shreveport, LA) — Bill Watts / UWF
# ============================================================

REGIONAL_TERRITORIES["midsouth"] = {
    "name": "Mid-South Wrestling",
    "abbrev": "Mid-South",
    "tier": 3,
    "location": "Shreveport, LA",
    "rooms": [
        {
            "key": "ms_arena",
            "name": "The Hirsch Memorial Coliseum",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("midsouth", "territory"), ("start_midsouth", "chargen")],
            "extras": {"capacity": 3000},
            "desc": (
                "The Hirsch Memorial Coliseum — Mid-South Wrestling's "
                "cathedral. Bill Watts runs this territory with an iron "
                "fist. No top-rope moves. No outside interference. Just "
                "hard-hitting, stiff, Southern wrestling.\n\n"
                "The crowd is blue-collar and loud. Oil field workers, "
                "soldiers from Barksdale AFB, and families pack the stands "
                "every Saturday night. They want blood and they get it."
            ),
        },
        {
            "key": "ms_backstage",
            "name": "Coliseum Backstage",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("midsouth", "territory")],
            "desc": (
                "The Hirsch backstage is cramped and hot. Concrete block "
                "walls, metal lockers, one shower that barely works. "
                "The hierarchy is strict — main eventers get space, "
                "everyone else makes do.\n\n"
                "A corkboard displays tonight's card and a reminder: "
                "'NO TOP ROPE MOVES — WATTS' RULES'. Break them and "
                "you're fired on the spot."
            ),
        },
        {
            "key": "ms_gym",
            "name": "Mid-South Wrestling Gym",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("midsouth", "territory")],
            "extras": {"stat_bonus": "str", "bonus_amount": 1},
            "desc": (
                "A no-frills gym in a warehouse district. Heavy iron, "
                "concrete floor, a ring in the corner for sparring. "
                "No air conditioning. The temperature matches the "
                "Louisiana humidity outside.\n\n"
                "Mid-South is a power territory. You need to look like "
                "a fighter and hit like one. The gym reflects that.\n\n"
                "|yTraining here gives a Strength bonus.|n"
            ),
        },
        {
            "key": "ms_bar",
            "name": "Bourbon Street Bar",
            "typeclass": "typeclasses.rooms.BarRoom",
            "tags": [("midsouth", "territory")],
            "desc": (
                "A neon-lit dive bar on a Shreveport back street that "
                "the boys call 'Bourbon Street' even though it's 300 "
                "miles from New Orleans. Cheap whiskey, a jukebox stuck "
                "on country, and a pool table with a ripped felt.\n\n"
                "This is where deals get made. Bookers drink here, "
                "veterans swap road stories, and newcomers try to make "
                "connections without looking too eager."
            ),
        },
        {
            "key": "ms_office",
            "name": "Watts' Office",
            "typeclass": "typeclasses.rooms.PromoterOffice",
            "tags": [("midsouth", "territory")],
            "extras": {"promoter_name": "Bill Watts"},
            "desc": (
                "A sparse office dominated by a massive wooden desk. "
                "Bill Watts sits behind it like a general behind a war "
                "table. Charts of territory revenue hang on the wall. "
                "A football from his playing days sits on a shelf.\n\n"
                "Watts doesn't small talk. You're either making him "
                "money or you're not. If you're not, this conversation "
                "is going to be very short."
            ),
        },
        {
            "key": "ms_travel",
            "name": "I-20 Interchange",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("midsouth", "territory")],
            "extras": {"destinations": ["memphis", "florida", "georgia", "wccw", "awa", "midatlantic", "bba", "proving_grounds"]},
            "desc": (
                "The I-20 interchange outside Shreveport connects to "
                "every major territory in the South and Midwest. East "
                "to Memphis and Georgia. West to Dallas and World Class. "
                "North to the AWA.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("north;n", "ms_arena", "ms_travel"),
        ("south;s", "ms_travel", "ms_arena"),
        ("west;w", "ms_arena", "ms_gym"),
        ("east;e", "ms_gym", "ms_arena"),
        ("east;e", "ms_arena", "ms_bar"),
        ("west;w", "ms_bar", "ms_arena"),
        ("south;s", "ms_arena", "ms_backstage"),
        ("north;n", "ms_backstage", "ms_arena"),
        ("west;w", "ms_backstage", "ms_office"),
        ("east;e", "ms_office", "ms_backstage"),
    ],
}

# ============================================================
# MID-ATLANTIC (Charlotte, NC) — JCP / NWA
# ============================================================

REGIONAL_TERRITORIES["midatlantic"] = {
    "name": "Mid-Atlantic Championship Wrestling",
    "abbrev": "Mid-Atlantic",
    "tier": 3,
    "location": "Charlotte, NC",
    "rooms": [
        {
            "key": "ma_arena",
            "name": "Greensboro Coliseum",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("midatlantic", "territory"), ("start_midatlantic", "chargen")],
            "extras": {"capacity": 5000},
            "desc": (
                "The Greensboro Coliseum — the crown jewel of Mid-Atlantic "
                "wrestling. NWA world title matches happen here. The arena "
                "seats thousands and fills for every big card. This is "
                "where workrate matters.\n\n"
                "The crowd is knowledgeable — Carolina wrestling fans "
                "know the difference between a good match and a great one. "
                "They'll sit on their hands for lazy work and blow the "
                "roof off for a five-star classic."
            ),
        },
        {
            "key": "ma_backstage",
            "name": "Coliseum Backstage",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("midatlantic", "territory")],
            "desc": (
                "The backstage area of the Greensboro Coliseum. Professional "
                "and organized — this is a big-time operation. Metal lockers, "
                "a trainer's table, and a TV monitor showing the live feed.\n\n"
                "The Horsemen hold court in the corner. Rick Fontaine's "
                "custom suit hangs on a rack. The tag teams warm up in "
                "pairs. This is a territory built on in-ring excellence."
            ),
        },
        {
            "key": "ma_gym",
            "name": "Charlotte Wrestling Gym",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("midatlantic", "territory")],
            "extras": {"stat_bonus": "tec", "bonus_amount": 1},
            "desc": (
                "A professional gym near the Coliseum. Two rings, a "
                "weight room, and a wall of mirrors for practicing holds. "
                "Mid-Atlantic values balanced, technical wrestling — the "
                "NWA style.\n\n"
                "Workrate is king here. You need to be able to go 30 "
                "minutes without gassing. The gym reflects that ethos.\n\n"
                "|yTraining here gives a Technical bonus.|n"
            ),
        },
        {
            "key": "ma_bar",
            "name": "The Watering Hole",
            "typeclass": "typeclasses.rooms.BarRoom",
            "tags": [("midatlantic", "territory")],
            "desc": (
                "A roadhouse bar outside Charlotte where the wrestlers "
                "gather after shows. Wooden booths, a long bar, and a "
                "dance floor that nobody uses because everyone's too "
                "banged up.\n\n"
                "Rick Fontaine's tab is legendary. The boys swap road "
                "stories and argue about match psychology until closing."
            ),
        },
        {
            "key": "ma_office",
            "name": "JCP Promoter's Office",
            "typeclass": "typeclasses.rooms.PromoterOffice",
            "tags": [("midatlantic", "territory")],
            "extras": {"promoter_name": "Jim Crockett Jr."},
            "desc": (
                "The Jim Crockett Promotions office in Charlotte. "
                "Wood-paneled walls, leather chairs, and the NWA "
                "championship belt displayed in a glass case. This "
                "territory is the backbone of the National Wrestling "
                "Alliance.\n\n"
                "Getting booked here means you've arrived. Staying "
                "booked means you can work."
            ),
        },
        {
            "key": "ma_studio",
            "name": "WPCQ TV Studio",
            "typeclass": "typeclasses.rooms.TerritoryRoom",
            "tags": [("midatlantic", "territory")],
            "extras": {"room_type": "studio"},
            "desc": (
                "The TV studio where Mid-Atlantic Championship Wrestling "
                "tapes its weekly syndicated show. Three cameras, professional "
                "lighting, and a set that looks like it cost actual money.\n\n"
                "Getting TV time here means national syndication — your "
                "face on screens from the Carolinas to Virginia."
            ),
        },
        {
            "key": "ma_travel",
            "name": "I-85 / I-77 Interchange",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("midatlantic", "territory")],
            "extras": {"destinations": ["memphis", "midsouth", "florida", "georgia", "awa", "stampede", "pnw", "wwf", "slaughterhouse", "beast_works"]},
            "desc": (
                "The Charlotte interchange where I-85 meets I-77. "
                "North to Virginia and the Northeast. South to Georgia "
                "and Florida. The Mid-Atlantic territory stretches from "
                "the Carolinas to Virginia.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("north;n", "ma_arena", "ma_travel"),
        ("south;s", "ma_travel", "ma_arena"),
        ("west;w", "ma_arena", "ma_gym"),
        ("east;e", "ma_gym", "ma_arena"),
        ("east;e", "ma_arena", "ma_bar"),
        ("west;w", "ma_bar", "ma_arena"),
        ("south;s", "ma_arena", "ma_backstage"),
        ("north;n", "ma_backstage", "ma_arena"),
        ("west;w", "ma_backstage", "ma_office"),
        ("east;e", "ma_office", "ma_backstage"),
        ("east;e", "ma_backstage", "ma_studio"),
        ("west;w", "ma_studio", "ma_backstage"),
    ],
}

# ============================================================
# FLORIDA (Tampa, FL) — CWF
# ============================================================

REGIONAL_TERRITORIES["florida"] = {
    "name": "Championship Wrestling from Florida",
    "abbrev": "Florida",
    "tier": 3,
    "location": "Tampa, FL",
    "rooms": [
        {
            "key": "fl_arena",
            "name": "Tampa Armory",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("florida", "territory"), ("start_florida", "chargen")],
            "extras": {"capacity": 2500},
            "desc": (
                "The Tampa National Guard Armory — Florida territory's "
                "home base. A brick building with high ceilings and no "
                "air conditioning. The Florida heat is part of the show.\n\n"
                "Florida is a blood-and-guts territory. Blade jobs, "
                "hardcore brawls, and old-school storytelling. The crowd "
                "wants to see someone bleed and they're not shy about "
                "saying so."
            ),
        },
        {
            "key": "fl_backstage",
            "name": "Armory Backstage",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("florida", "territory")],
            "desc": (
                "The backstage area is a drill hall converted for "
                "wrestling. Military surplus lockers, concrete floors, "
                "and a single overhead fan that does nothing against "
                "the Tampa heat.\n\n"
                "The Florida territory is a melting pot — Southern "
                "brawlers, Japanese imports, Caribbean luchadors, and "
                "old NWA hands all work here."
            ),
        },
        {
            "key": "fl_gym",
            "name": "The Swamp Gym",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("florida", "territory")],
            "extras": {"stat_bonus": "tou", "bonus_amount": 1},
            "desc": (
                "A converted storage unit behind the Armory, nicknamed "
                "'The Swamp' because the humidity inside is tropical. "
                "Rusty weights, a speed bag, and a practice ring with "
                "ropes that smell like mildew.\n\n"
                "Training in the Swamp builds toughness by sheer "
                "endurance. If you can work out here for an hour, "
                "you can wrestle anywhere.\n\n"
                "|yTraining here gives a Toughness bonus.|n"
            ),
        },
        {
            "key": "fl_bar",
            "name": "Ybor City Cantina",
            "typeclass": "typeclasses.rooms.BarRoom",
            "tags": [("florida", "territory")],
            "desc": (
                "A Cuban bar in Tampa's Ybor City district. Ceiling fans, "
                "tile floors, and a bartender who pours stiff mojitos. "
                "The jukebox plays salsa and Southern rock in equal measure.\n\n"
                "Wrestlers from every background mingle here. It's one of "
                "the few places where a Japanese technical wrestler and "
                "a Florida cracker brawler share a drink and plan a match."
            ),
        },
        {
            "key": "fl_office",
            "name": "Florida Promoter's Office",
            "typeclass": "typeclasses.rooms.PromoterOffice",
            "tags": [("florida", "territory")],
            "extras": {"promoter_name": "Eddie Graham"},
            "desc": (
                "Eddie Graham's office at the Armory. Sparse and functional "
                "— a desk, a phone, and booking sheets covered in pencil "
                "marks and eraser dust. Graham is a booker's booker — he "
                "sees angles nobody else does.\n\n"
                "A Florida championship belt hangs on the wall. To hold "
                "it, you need to bleed for it."
            ),
        },
        {
            "key": "fl_travel",
            "name": "I-4 / I-75 Interchange",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("florida", "territory")],
            "extras": {"destinations": ["memphis", "midsouth", "midatlantic", "georgia", "pensacola", "conservatory", "dungeon_holds", "fcw"]},
            "desc": (
                "The Tampa interchange. North on I-75 to Georgia and "
                "the Carolinas. East on I-4 to Orlando. The Florida "
                "territory stretches from Tampa to Jacksonville.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("north;n", "fl_arena", "fl_travel"),
        ("south;s", "fl_travel", "fl_arena"),
        ("west;w", "fl_arena", "fl_gym"),
        ("east;e", "fl_gym", "fl_arena"),
        ("east;e", "fl_arena", "fl_bar"),
        ("west;w", "fl_bar", "fl_arena"),
        ("south;s", "fl_arena", "fl_backstage"),
        ("north;n", "fl_backstage", "fl_arena"),
        ("west;w", "fl_backstage", "fl_office"),
        ("east;e", "fl_office", "fl_backstage"),
    ],
}

# ============================================================
# GEORGIA (Atlanta, GA) — GCW / TBS
# ============================================================

REGIONAL_TERRITORIES["georgia"] = {
    "name": "Georgia Championship Wrestling",
    "abbrev": "Georgia",
    "tier": 3,
    "location": "Atlanta, GA",
    "rooms": [
        {
            "key": "ga_arena",
            "name": "The Omni",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("georgia", "territory"), ("start_georgia", "chargen")],
            "extras": {"capacity": 4000},
            "desc": (
                "The Omni in downtown Atlanta — Georgia Championship "
                "Wrestling's flagship venue. This territory has something "
                "no other regional has: national television on TBS.\n\n"
                "Every Saturday night at 6:05, millions watch from their "
                "living rooms. Getting TV time here means the whole "
                "country knows your name. The pressure is immense."
            ),
        },
        {
            "key": "ga_backstage",
            "name": "Omni Backstage",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("georgia", "territory")],
            "desc": (
                "Professional backstage area befitting a national TV "
                "production. Proper lockers, a green room for interview "
                "segments, and a production office where the TV director "
                "coordinates camera shots.\n\n"
                "Gordon Stoley stands by the interview area, reviewing "
                "notes. His voice is the most trusted in wrestling."
            ),
        },
        {
            "key": "ga_gym",
            "name": "Atlanta Wrestling Gym",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("georgia", "territory")],
            "extras": {"stat_bonus": "cha", "bonus_amount": 1},
            "desc": (
                "A modern gym near the CNN Center. Georgia territory "
                "values charisma above all — you need to be able to "
                "connect through a TV camera, not just to a live crowd.\n\n"
                "A full ring, a weight room, and a mock interview set "
                "with a camera for practicing promos. Looking good on "
                "camera is half the battle here.\n\n"
                "|yTraining here gives a Charisma bonus.|n"
            ),
        },
        {
            "key": "ga_studio",
            "name": "TBS Studio",
            "typeclass": "typeclasses.rooms.TerritoryRoom",
            "tags": [("georgia", "territory")],
            "extras": {"room_type": "studio"},
            "desc": (
                "The TBS studio at CNN Center — where Georgia Championship "
                "Wrestling goes national. Professional cameras, studio "
                "lighting, and a set that reaches millions every Saturday.\n\n"
                "Cutting a promo here isn't like cutting one in a VFW hall. "
                "The camera amplifies everything — a great talker becomes "
                "a superstar, and a bad one becomes a joke."
            ),
        },
        {
            "key": "ga_office",
            "name": "GCW Promoter's Office",
            "typeclass": "typeclasses.rooms.PromoterOffice",
            "tags": [("georgia", "territory")],
            "extras": {"promoter_name": "Jim Barnett"},
            "desc": (
                "Jim Barnett's office — the political nerve center of "
                "Georgia Championship Wrestling. Barnett is a master "
                "politician who plays the NWA board like a chess game.\n\n"
                "Getting in his good graces means TV time and national "
                "exposure. Getting on his bad side means jobbing to "
                "everyone until you quit."
            ),
        },
        {
            "key": "ga_travel",
            "name": "I-75 / I-85 Interchange",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("georgia", "territory")],
            "extras": {"destinations": ["memphis", "midsouth", "midatlantic", "florida", "awa", "psc", "conservatory", "dsw"]},
            "desc": (
                "Atlanta's highway interchange — the crossroads of the "
                "Southeast. Every territory is accessible from here.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("north;n", "ga_arena", "ga_travel"),
        ("south;s", "ga_travel", "ga_arena"),
        ("west;w", "ga_arena", "ga_gym"),
        ("east;e", "ga_gym", "ga_arena"),
        ("east;e", "ga_arena", "ga_studio"),
        ("west;w", "ga_studio", "ga_arena"),
        ("south;s", "ga_arena", "ga_backstage"),
        ("north;n", "ga_backstage", "ga_arena"),
        ("west;w", "ga_backstage", "ga_office"),
        ("east;e", "ga_office", "ga_backstage"),
    ],
}

# ============================================================
# WORLD CLASS (Dallas, TX) — WCCW / Von Erichs
# ============================================================

REGIONAL_TERRITORIES["wccw"] = {
    "name": "World Class Championship Wrestling",
    "abbrev": "WCCW",
    "tier": 3,
    "location": "Dallas, TX",
    "rooms": [
        {
            "key": "wc_arena",
            "name": "The Sportatorium",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("wccw", "territory"), ("start_wccw", "chargen")],
            "extras": {"capacity": 4500},
            "desc": (
                "The Sportatorium — World Class Championship Wrestling's "
                "legendary home in Dallas. The building is old, the seats "
                "are hard, and the air conditioning barely works. None of "
                "that matters when the crowd is on fire.\n\n"
                "Friday Night Star Wars airs from here. The Von Adler "
                "family is wrestling royalty in Texas. The fans worship "
                "them like gods. The emotion in this building on a good "
                "night is unlike anything else in the business."
            ),
        },
        {
            "key": "wc_backstage",
            "name": "Sportatorium Backstage",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("wccw", "territory")],
            "desc": (
                "A cramped backstage area in a building that was never "
                "designed for wrestling. Wrestlers share the space with "
                "electrical panels and storage. But nobody complains — "
                "this is World Class.\n\n"
                "The Von Adler boys are here — golden-haired, athletic, "
                "the pride of Texas. Everyone else orbits around them."
            ),
        },
        {
            "key": "wc_gym",
            "name": "Dallas Wrestling Gym",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("wccw", "territory")],
            "extras": {"stat_bonus": "agi", "bonus_amount": 1},
            "desc": (
                "A gym near the Sportatorium where the World Class roster "
                "trains. The Von Adlers brought an athletic, high-energy "
                "style to Texas wrestling — agility matters here.\n\n"
                "A ring, free weights, and a trampoline for practicing "
                "aerial moves. The Texas heat pours through the windows.\n\n"
                "|yTraining here gives an Agility bonus.|n"
            ),
        },
        {
            "key": "wc_ranch",
            "name": "Von Adler Ranch",
            "typeclass": "typeclasses.rooms.UniqueRoom",
            "tags": [("wccw", "territory")],
            "desc": (
                "The Von Adler family ranch outside Dallas. Sprawling "
                "Texas land, a private ring under a tin roof, and the "
                "family compound where wrestling legends are born.\n\n"
                "Getting invited to the ranch means you're family — or "
                "close enough. The Von Adlers train here, plan here, "
                "and mourn here. The ranch holds joy and tragedy in "
                "equal measure."
            ),
        },
        {
            "key": "wc_office",
            "name": "WCCW Promoter's Office",
            "typeclass": "typeclasses.rooms.PromoterOffice",
            "tags": [("wccw", "territory")],
            "extras": {"promoter_name": "Fritz Von Adler"},
            "desc": (
                "Fritz Von Adler's office at the Sportatorium. The "
                "patriarch runs World Class with patriarchal authority. "
                "Family comes first — his boys headline every card.\n\n"
                "If you're not a Von Adler, your ceiling depends on "
                "how well you make them look. Fritz's booking is "
                "emotional, dramatic, and deeply personal."
            ),
        },
        {
            "key": "wc_travel",
            "name": "I-35 / I-30 Interchange",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("wccw", "territory")],
            "extras": {"destinations": ["midsouth", "memphis", "awa", "midatlantic", "lsu", "japan"]},
            "desc": (
                "The Dallas interchange. South to Houston, east to "
                "Shreveport and Mid-South, north to Oklahoma and the "
                "AWA territory. World Class also has a pipeline to Japan.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("north;n", "wc_arena", "wc_travel"),
        ("south;s", "wc_travel", "wc_arena"),
        ("west;w", "wc_arena", "wc_gym"),
        ("east;e", "wc_gym", "wc_arena"),
        ("east;e", "wc_arena", "wc_ranch"),
        ("west;w", "wc_ranch", "wc_arena"),
        ("south;s", "wc_arena", "wc_backstage"),
        ("north;n", "wc_backstage", "wc_arena"),
        ("west;w", "wc_backstage", "wc_office"),
        ("east;e", "wc_office", "wc_backstage"),
    ],
}

# ============================================================
# AWA (Minneapolis, MN) — Verne Gagne
# ============================================================

REGIONAL_TERRITORIES["awa"] = {
    "name": "American Wrestling Association",
    "abbrev": "AWA",
    "tier": 3,
    "location": "Minneapolis, MN",
    "rooms": [
        {
            "key": "awa_arena",
            "name": "Minneapolis Auditorium",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("awa", "territory"), ("start_awa", "chargen")],
            "extras": {"capacity": 3500},
            "desc": (
                "The Minneapolis Auditorium — home of the American Wrestling "
                "Association. Vernon Gavin built this territory on legitimacy "
                "— real athletes, real holds, real wrestling.\n\n"
                "The Midwest crowd respects ability. No flashy gimmicks "
                "needed — just show them you can wrestle. The AWA "
                "championship is the most prestigious in wrestling "
                "(just ask Vernon)."
            ),
        },
        {
            "key": "awa_backstage",
            "name": "Auditorium Backstage",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("awa", "territory")],
            "desc": (
                "A clean, organized backstage area. The AWA runs like a "
                "legitimate sports operation — dress codes, handshake "
                "greetings, and a respect for the craft that borders on "
                "reverence.\n\n"
                "Vernon Gavin's championship hangs in a glass case by "
                "the entrance. He polishes it personally before every show."
            ),
        },
        {
            "key": "awa_gym",
            "name": "Gagne's Training Barn",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("awa", "territory")],
            "extras": {"stat_bonus": "tec", "bonus_amount": 1},
            "desc": (
                "A barn on Vernon Gavin's farm outside Minneapolis, "
                "converted into a world-class training facility. A ring, "
                "a weight room, and wrestling mats for amateur-style "
                "drilling.\n\n"
                "Gavin's philosophy: wrestling is an athletic contest "
                "first. His training emphasizes amateur technique, "
                "conditioning, and mat wrestling.\n\n"
                "|yTraining here gives a Technical bonus.|n"
            ),
        },
        {
            "key": "awa_bar",
            "name": "The Minneapolis Club",
            "typeclass": "typeclasses.rooms.BarRoom",
            "tags": [("awa", "territory")],
            "desc": (
                "A supper club where the AWA roster gathers after shows. "
                "White tablecloths, steak dinners, and cocktails — the "
                "AWA considers itself a step above the Southern territories.\n\n"
                "Vernon holds court at the head table. He lectures about "
                "the sport, its legitimacy, and how he once beat anyone "
                "who challenged him in a real fight."
            ),
        },
        {
            "key": "awa_farm",
            "name": "Gagne's Farm",
            "typeclass": "typeclasses.rooms.UniqueRoom",
            "tags": [("awa", "territory")],
            "desc": (
                "Vernon Gavin's farm outside Minneapolis. Rolling "
                "Minnesota fields, a red barn (the training facility), "
                "and a modest farmhouse. The farm is where Gavin holds "
                "tryouts and evaluates potential.\n\n"
                "Getting invited to the farm is the AWA equivalent of "
                "a job interview. Gavin watches you move, checks your "
                "amateur credentials, and decides if you're 'legitimate' "
                "enough for his territory."
            ),
        },
        {
            "key": "awa_office",
            "name": "AWA Promoter's Office",
            "typeclass": "typeclasses.rooms.PromoterOffice",
            "tags": [("awa", "territory")],
            "extras": {"promoter_name": "Vernon Gavin"},
            "desc": (
                "Gavin's office at the Auditorium. Trophies from his "
                "amateur wrestling days line the shelves. A map of the "
                "AWA territory — Minnesota, Wisconsin, Illinois, Manitoba "
                "— hangs behind his desk.\n\n"
                "Vernon books the AWA like he wrestles: methodically, "
                "carefully, and always with himself on top."
            ),
        },
        {
            "key": "awa_travel",
            "name": "I-94 / I-35 Interchange",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("awa", "territory")],
            "extras": {"destinations": ["memphis", "midsouth", "midatlantic", "wccw", "stampede", "pnw", "proving_grounds", "wwf"]},
            "desc": (
                "The Minneapolis interchange. West to the Dakotas and "
                "Stampede territory in Calgary. East to Chicago and the "
                "Northeast. South to Kansas City and the heartland.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("north;n", "awa_arena", "awa_travel"),
        ("south;s", "awa_travel", "awa_arena"),
        ("west;w", "awa_arena", "awa_gym"),
        ("east;e", "awa_gym", "awa_arena"),
        ("east;e", "awa_arena", "awa_bar"),
        ("west;w", "awa_bar", "awa_arena"),
        ("south;s", "awa_arena", "awa_backstage"),
        ("north;n", "awa_backstage", "awa_arena"),
        ("west;w", "awa_backstage", "awa_office"),
        ("east;e", "awa_office", "awa_backstage"),
        ("east;e", "awa_backstage", "awa_farm"),
        ("west;w", "awa_farm", "awa_backstage"),
    ],
}

# ============================================================
# STAMPEDE (Calgary, AB) — Stu Hart
# ============================================================

REGIONAL_TERRITORIES["stampede"] = {
    "name": "Stampede Wrestling",
    "abbrev": "Stampede",
    "tier": 3,
    "location": "Calgary, AB",
    "rooms": [
        {
            "key": "stm_arena",
            "name": "The Pavilion",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("stampede", "territory"), ("start_stampede", "chargen")],
            "extras": {"capacity": 2000},
            "desc": (
                "The Victoria Pavilion — Stampede Wrestling's home since "
                "the territory began. Friday nights in Calgary belong to "
                "the Harmon family. The Pavilion is old, cold, and loud.\n\n"
                "Stampede is a technical territory with a mean streak. "
                "The style is stiff, the holds are real, and anyone who "
                "survives the Dungeon can survive anything."
            ),
        },
        {
            "key": "stm_backstage",
            "name": "Pavilion Backstage",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("stampede", "territory")],
            "desc": (
                "A cold backstage area — it's Calgary, and the Pavilion's "
                "heating hasn't worked properly since 1974. The Harmon "
                "family is everywhere — brothers, cousins, in-laws.\n\n"
                "Foreign wrestlers cycle through Stampede constantly — "
                "Japanese stars on excursion, British grapplers, European "
                "technicians. It's one of the most international "
                "territories in North America."
            ),
        },
        {
            "key": "stm_gym",
            "name": "The Dungeon",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("stampede", "territory")],
            "extras": {"stat_bonus": "tou", "bonus_amount": 2},
            "desc": (
                "The Dungeon — Stuart Harmon's basement training facility. "
                "The most feared room in professional wrestling. Low "
                "ceiling, bare concrete, wrestling mats, and decades of "
                "pain soaked into every surface.\n\n"
                "Stuart stretches students until they scream. His catch "
                "wrestling is real — the holds hurt, the submissions are "
                "legitimate, and tapping out is not optional until he "
                "says so.\n\n"
                "|yTraining here gives a Toughness bonus.|n"
            ),
        },
        {
            "key": "stm_office",
            "name": "Stampede Promoter's Office",
            "typeclass": "typeclasses.rooms.PromoterOffice",
            "tags": [("stampede", "territory")],
            "extras": {"promoter_name": "Stuart Harmon"},
            "desc": (
                "Stuart Harmon's office — a cluttered room in the back "
                "of the Harmon family house. Tapes from decades of "
                "Stampede shows fill the shelves. Stuart books by instinct, "
                "loyalty to family, and an eye for talent.\n\n"
                "If you're a Harmon, you're booked. If you're not, you "
                "earn your spot in the Dungeon."
            ),
        },
        {
            "key": "stm_travel",
            "name": "Trans-Canada Highway",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("stampede", "territory")],
            "extras": {"destinations": ["awa", "pnw", "midatlantic", "wwf", "uk", "japan"]},
            "desc": (
                "The Trans-Canada Highway stretches east and west from "
                "Calgary. South to Montana and the American territories. "
                "Stampede's international connections reach Japan and "
                "the UK.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("north;n", "stm_arena", "stm_travel"),
        ("south;s", "stm_travel", "stm_arena"),
        ("west;w", "stm_arena", "stm_gym"),
        ("east;e", "stm_gym", "stm_arena"),
        ("south;s", "stm_arena", "stm_backstage"),
        ("north;n", "stm_backstage", "stm_arena"),
        ("west;w", "stm_backstage", "stm_office"),
        ("east;e", "stm_office", "stm_backstage"),
    ],
}

# ============================================================
# PACIFIC NW (Portland, OR) — Portland Wrestling
# ============================================================

REGIONAL_TERRITORIES["pnw"] = {
    "name": "Pacific Northwest Wrestling",
    "abbrev": "PNW",
    "tier": 3,
    "location": "Portland, OR",
    "rooms": [
        {
            "key": "pnw_arena",
            "name": "Portland Sports Arena",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("pnw", "territory"), ("start_pnw", "chargen")],
            "extras": {"capacity": 2500},
            "desc": (
                "The Portland Sports Arena — a worker's territory through "
                "and through. No gimmicks, no flash — just solid in-ring "
                "work. Portland fans have seen it all and they demand "
                "quality.\n\n"
                "Saturday nights in Portland are an institution. The "
                "crowd is loyal, the beer is local, and the wrestling "
                "is consistently some of the best in the country."
            ),
        },
        {
            "key": "pnw_backstage",
            "name": "Arena Backstage",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("pnw", "territory")],
            "desc": (
                "A modest backstage area. Portland doesn't have the "
                "budget of the Southern territories, but the locker room "
                "culture is professional. Everyone shakes hands. Everyone "
                "works.\n\n"
                "Veterans from other territories end their careers here — "
                "the pace is sustainable and the crowds appreciate craft "
                "over spectacle."
            ),
        },
        {
            "key": "pnw_gym",
            "name": "Timber Mill Gym",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("pnw", "territory")],
            "extras": {"stat_bonus": "psy", "bonus_amount": 1},
            "desc": (
                "A gym in a converted timber mill on the outskirts of "
                "Portland. The ring sits where logs used to roll. Sawdust "
                "still clings to the rafters. The Oregon rain patters on "
                "the metal roof.\n\n"
                "Portland values psychology — telling a story in the ring. "
                "The gym has a video setup for studying matches and "
                "analyzing crowd reactions.\n\n"
                "|yTraining here gives a Psychology bonus.|n"
            ),
        },
        {
            "key": "pnw_bar",
            "name": "The Logger's Rest",
            "typeclass": "typeclasses.rooms.BarRoom",
            "tags": [("pnw", "territory")],
            "desc": (
                "A wood-paneled bar near the waterfront. Local craft beer "
                "on tap, flannel shirts on the patrons, and wrestling "
                "memorabilia covering the walls. The owner is a mark who "
                "lets the boys drink on tab.\n\n"
                "Portland wrestlers are a tight-knit community. Road "
                "stories are shared, matches are planned over pints, "
                "and the rain never stops."
            ),
        },
        {
            "key": "pnw_office",
            "name": "PNW Promoter's Office",
            "typeclass": "typeclasses.rooms.PromoterOffice",
            "tags": [("pnw", "territory")],
            "extras": {"promoter_name": "Don Owen"},
            "desc": (
                "Don Owen's office — a small room above the arena. Owen "
                "has run Portland wrestling for decades with a handshake "
                "and a fair deal. Pay isn't great but it's honest, and "
                "he never lies about your spot on the card.\n\n"
                "A poster from 1960 hangs on the wall. Portland wrestling "
                "is a tradition, not a business."
            ),
        },
        {
            "key": "pnw_travel",
            "name": "I-5 — Pacific Coast Highway",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("pnw", "territory")],
            "extras": {"destinations": ["awa", "stampede", "wccw", "midatlantic", "wwf", "japan"]},
            "desc": (
                "Interstate 5 runs north to Seattle and south to "
                "California. Portland has connections to the AWA and "
                "Stampede territories through the Pacific Northwest "
                "circuit.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("north;n", "pnw_arena", "pnw_travel"),
        ("south;s", "pnw_travel", "pnw_arena"),
        ("west;w", "pnw_arena", "pnw_gym"),
        ("east;e", "pnw_gym", "pnw_arena"),
        ("east;e", "pnw_arena", "pnw_bar"),
        ("west;w", "pnw_bar", "pnw_arena"),
        ("south;s", "pnw_arena", "pnw_backstage"),
        ("north;n", "pnw_backstage", "pnw_arena"),
        ("west;w", "pnw_backstage", "pnw_office"),
        ("east;e", "pnw_office", "pnw_backstage"),
    ],
}
