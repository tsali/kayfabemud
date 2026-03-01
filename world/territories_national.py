"""
Kayfabe: Protect the Business — Tier 4 National/International territories.
WWF, WCW, ECW, UK, Japan.
"""

NATIONAL_TERRITORIES = {}

# ============================================================
# WWF (New York, NY) — McMahon
# ============================================================

NATIONAL_TERRITORIES["wwf"] = {
    "name": "World Wrestling Federation",
    "abbrev": "WWF",
    "tier": 4,
    "location": "New York, NY",
    "rooms": [
        {
            "key": "wwf_arena",
            "name": "Madison Square Garden",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("wwf", "territory"), ("start_wwf", "chargen")],
            "extras": {"capacity": 20000},
            "desc": (
                "Madison Square Garden — the Mecca of professional "
                "wrestling. Twenty thousand seats, national television, "
                "and the biggest stage in the business. The lights are "
                "blinding, the crowd is deafening, and every match here "
                "is history.\n\n"
                "This is where careers are made or broken in a single "
                "night. The WWF is the biggest promotion in the world "
                "and MSG is its throne room."
            ),
        },
        {
            "key": "wwf_backstage",
            "name": "MSG Backstage — Gorilla Position",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("wwf", "territory")],
            "desc": (
                "The backstage area at Madison Square Garden. Gorilla "
                "Position — the curtain where you enter the arena — is "
                "the most famous threshold in wrestling. Veterans gather "
                "here to watch the monitor and evaluate the talent.\n\n"
                "The production is massive. Makeup artists, cameramen, "
                "writers, agents — the WWF machine runs on hundreds of "
                "people. Your job is to perform."
            ),
        },
        {
            "key": "wwf_gym",
            "name": "WWF Performance Center",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("wwf", "territory")],
            "extras": {"stat_bonus": "cha", "bonus_amount": 2},
            "desc": (
                "The WWF Performance Center — a state-of-the-art facility "
                "for the main roster. Multiple rings, a professional gym, "
                "promo coaching, and camera training. Everything is geared "
                "toward making you a TV star.\n\n"
                "In the WWF, charisma is king. You can be an average "
                "worker and main event if you have 'it'. You can be the "
                "best wrestler alive and job forever if you don't.\n\n"
                "|yTraining here gives a Charisma bonus.|n"
            ),
        },
        {
            "key": "wwf_studio",
            "name": "WWF TV Studio — Titan Towers",
            "typeclass": "typeclasses.rooms.TerritoryRoom",
            "tags": [("wwf", "territory")],
            "extras": {"room_type": "studio"},
            "desc": (
                "Titan Towers — the corporate headquarters of the World "
                "Wrestling Federation. A sleek office building in Stamford, "
                "Connecticut that houses the TV production, marketing, "
                "and booking operations.\n\n"
                "Interview segments are taped here. The set is professional "
                "— polished backdrops, proper lighting, and a staff of "
                "writers who script your promos (whether you like it or not)."
            ),
        },
        {
            "key": "wwf_bar",
            "name": "The World — Midtown Bar",
            "typeclass": "typeclasses.rooms.BarRoom",
            "tags": [("wwf", "territory")],
            "desc": (
                "A midtown Manhattan bar where the WWF roster gathers "
                "after MSG shows. Expensive drinks, dim lighting, and "
                "the kind of crowd that recognizes celebrities.\n\n"
                "Deals are made here. Agents whisper about pushes and "
                "title runs. Rivals share drinks and plan feuds. The "
                "business never stops."
            ),
        },
        {
            "key": "wwf_office",
            "name": "Vince McMahon's Office",
            "typeclass": "typeclasses.rooms.PromoterOffice",
            "tags": [("wwf", "territory")],
            "extras": {"promoter_name": "Vince McMahon"},
            "desc": (
                "The boss's office at Titan Towers. A massive desk, "
                "championship belts on display, and a wall of monitors "
                "showing every WWF program simultaneously.\n\n"
                "McMahon is not just a promoter — he's the creator of "
                "the modern wrestling entertainment machine. He sees "
                "wrestlers as characters in his vision. Fit the vision "
                "or be replaced."
            ),
        },
        {
            "key": "wwf_travel",
            "name": "JFK Airport — International Terminal",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("wwf", "territory")],
            "extras": {"destinations": ["wcw", "ecw", "uk", "japan", "midatlantic", "awa", "ovw", "fcw", "hwa", "slaughterhouse", "beast_works"]},
            "desc": (
                "JFK International Airport. First class tickets for main "
                "eventers, coach for everyone else. The WWF tours "
                "nationally and internationally — you could be in New "
                "York tonight and Tokyo next week.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("backstage", "wwf_arena", "wwf_backstage"),
        ("gorilla", "wwf_arena", "wwf_backstage"),
        ("arena", "wwf_backstage", "wwf_arena"),
        ("msg", "wwf_backstage", "wwf_arena"),
        ("gym", "wwf_arena", "wwf_gym"),
        ("arena", "wwf_gym", "wwf_arena"),
        ("studio", "wwf_arena", "wwf_studio"),
        ("titan", "wwf_arena", "wwf_studio"),
        ("arena", "wwf_studio", "wwf_arena"),
        ("bar", "wwf_arena", "wwf_bar"),
        ("arena", "wwf_bar", "wwf_arena"),
        ("office", "wwf_backstage", "wwf_office"),
        ("backstage", "wwf_office", "wwf_backstage"),
        ("travel", "wwf_arena", "wwf_travel"),
        ("airport", "wwf_arena", "wwf_travel"),
        ("back", "wwf_travel", "wwf_arena"),
    ],
}

# ============================================================
# WCW (Atlanta, GA) — Turner / Bischoff
# ============================================================

NATIONAL_TERRITORIES["wcw"] = {
    "name": "World Championship Wrestling",
    "abbrev": "WCW",
    "tier": 4,
    "location": "Atlanta, GA",
    "rooms": [
        {
            "key": "wcw_arena",
            "name": "CNN Center Arena",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("wcw", "territory"), ("start_wcw", "chargen")],
            "extras": {"capacity": 15000},
            "desc": (
                "The CNN Center Arena in Atlanta — WCW's home base and "
                "ground zero for the Monday Night Wars. Turner money "
                "built this machine and it shows. Production values that "
                "rival Hollywood, pyrotechnics, and a roster stacked "
                "with talent from every territory.\n\n"
                "Monday Nitro goes head-to-head with WWF every week. "
                "The ratings war is real and it's personal."
            ),
        },
        {
            "key": "wcw_backstage",
            "name": "CNN Center Backstage",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("wcw", "territory")],
            "desc": (
                "A sprawling backstage area with separate locker rooms "
                "for main eventers, midcarders, and the cruiserweight "
                "division. The politics are legendary — cliques, power "
                "plays, and creative control clauses.\n\n"
                "Turner's checkbook is bottomless. Anyone can be bought. "
                "The question is whether you'll survive the backstage "
                "politics long enough to matter."
            ),
        },
        {
            "key": "wcw_gym",
            "name": "WCW Power Plant",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("wcw", "territory")],
            "extras": {"stat_bonus": "agi", "bonus_amount": 2},
            "desc": (
                "The WCW Power Plant — the company's official training "
                "facility. Multiple rings, a state-of-the-art weight room, "
                "and coaches from every style. WCW's cruiserweight division "
                "has brought high-flying, international styles into the "
                "mainstream.\n\n"
                "Agility and innovation are valued here. If you can do "
                "something nobody's seen before, WCW will put you on TV.\n\n"
                "|yTraining here gives an Agility bonus.|n"
            ),
        },
        {
            "key": "wcw_studio",
            "name": "WCW Saturday Night Studio",
            "typeclass": "typeclasses.rooms.TerritoryRoom",
            "tags": [("wcw", "territory")],
            "extras": {"room_type": "studio"},
            "desc": (
                "The studio where WCW Saturday Night and Thunder are "
                "taped. Professional production — three cameras, proper "
                "lighting, and a set designed for national television.\n\n"
                "WCW's B-shows are where midcarders and cruiserweights "
                "get their TV time. A strong showing here can lead to "
                "a Nitro spot."
            ),
        },
        {
            "key": "wcw_bar",
            "name": "The Turner Club",
            "typeclass": "typeclasses.rooms.BarRoom",
            "tags": [("wcw", "territory")],
            "desc": (
                "An upscale bar near CNN Center. WCW's main eventers "
                "have guaranteed contracts and the spending habits to "
                "match. The bar tab at the Turner Club is legendary.\n\n"
                "Political alliances form and dissolve over martinis. "
                "Whose clique are you in? That matters more than your "
                "workrate."
            ),
        },
        {
            "key": "wcw_office",
            "name": "Eric Bischoff's Office",
            "typeclass": "typeclasses.rooms.PromoterOffice",
            "tags": [("wcw", "territory")],
            "extras": {"promoter_name": "Eric Bischoff"},
            "desc": (
                "Eric Bischoff's corner office at CNN Center. Floor-to-ceiling "
                "windows overlooking Atlanta. A TV tuned to Raw on one "
                "screen, Nitro ratings on another. Bischoff plays to win.\n\n"
                "He's willing to spend any amount to beat McMahon. If you "
                "can help him win the ratings war, name your price."
            ),
        },
        {
            "key": "wcw_travel",
            "name": "Hartsfield Airport",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("wcw", "territory")],
            "extras": {"destinations": ["wwf", "ecw", "japan", "uk", "georgia", "florida", "midatlantic", "ovw", "dsw"]},
            "desc": (
                "Hartsfield-Jackson Atlanta International Airport — the "
                "busiest airport in the world. WCW tours nationally and "
                "has talent exchange agreements with Japan.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("backstage", "wcw_arena", "wcw_backstage"),
        ("arena", "wcw_backstage", "wcw_arena"),
        ("gym", "wcw_arena", "wcw_gym"),
        ("plant", "wcw_arena", "wcw_gym"),
        ("arena", "wcw_gym", "wcw_arena"),
        ("studio", "wcw_arena", "wcw_studio"),
        ("arena", "wcw_studio", "wcw_arena"),
        ("bar", "wcw_arena", "wcw_bar"),
        ("arena", "wcw_bar", "wcw_arena"),
        ("office", "wcw_backstage", "wcw_office"),
        ("backstage", "wcw_office", "wcw_backstage"),
        ("travel", "wcw_arena", "wcw_travel"),
        ("airport", "wcw_arena", "wcw_travel"),
        ("back", "wcw_travel", "wcw_arena"),
    ],
}

# ============================================================
# ECW (Philadelphia, PA) — Phil Eastman (Heyman)
# ============================================================

NATIONAL_TERRITORIES["ecw"] = {
    "name": "Extreme Championship Wrestling",
    "abbrev": "ECW",
    "tier": 4,
    "location": "Philadelphia, PA",
    "rooms": [
        {
            "key": "ecw_arena",
            "name": "The Bingo Hall",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("ecw", "territory"), ("start_ecw", "chargen")],
            "extras": {"capacity": 1200},
            "desc": (
                "The ECW Arena — a converted bingo hall in South "
                "Philadelphia that became the most dangerous venue in "
                "wrestling. Low ceiling, no guardrails, and a crowd that "
                "throws chairs.\n\n"
                "ECW rewrote the rules. Tables, ladders, chairs, barbed "
                "wire — everything is a weapon. The crowd chants 'EC-DUB' "
                "like a war cry. This isn't sports entertainment. This is "
                "a revolution."
            ),
        },
        {
            "key": "ecw_backstage",
            "name": "Bingo Hall Backstage",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("ecw", "territory")],
            "desc": (
                "A cramped, grimy backstage area. No lockers — hooks on "
                "the wall. No trainer's table — patch yourself up. The "
                "ECW roster lives on the edge, and the backstage reflects "
                "it.\n\n"
                "Phil Eastman paces back and forth, cutting promos to "
                "himself, planning the show in his head. He's a genius "
                "and he's broke. The checks might bounce but the shows "
                "never disappoint."
            ),
        },
        {
            "key": "ecw_gym",
            "name": "South Philly Gym",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("ecw", "territory")],
            "extras": {"stat_bonus": "tou", "bonus_amount": 2},
            "desc": (
                "A boxing gym in South Philadelphia that the ECW roster "
                "has colonized. Heavy bags, speed bags, a ring with "
                "bloodstains that won't wash out. No fancy equipment — "
                "just iron and will.\n\n"
                "ECW doesn't care about your look. They care about your "
                "toughness and your willingness to go to the extreme.\n\n"
                "|yTraining here gives a Toughness bonus.|n"
            ),
        },
        {
            "key": "ecw_bar",
            "name": "Pat's Steaks Parking Lot",
            "typeclass": "typeclasses.rooms.BarRoom",
            "tags": [("ecw", "territory")],
            "desc": (
                "Not a bar — the parking lot outside Pat's King of Steaks "
                "on Passyunk Avenue. The ECW roster can't afford bars. "
                "They eat cheesesteaks at 2 AM and plan spots on napkins.\n\n"
                "The camaraderie is real. ECW wrestlers bleed for each "
                "other — literally. The bonds formed in this parking lot "
                "last forever."
            ),
        },
        {
            "key": "ecw_office",
            "name": "Eastman's Office",
            "typeclass": "typeclasses.rooms.PromoterOffice",
            "tags": [("ecw", "territory")],
            "extras": {"promoter_name": "Phil Eastman"},
            "desc": (
                "Phil Eastman's 'office' — a closet in the back of the "
                "Bingo Hall with a phone, a VCR, and stacks of unpaid "
                "bills. A whiteboard has the most brilliant booking in "
                "wrestling written in dry-erase marker.\n\n"
                "Eastman is the mad genius of the industry. He can't pay "
                "you on time but he'll make you a star. His promos are "
                "legendary. His checks are... less so."
            ),
        },
        {
            "key": "ecw_travel",
            "name": "I-95 — South Philly On-Ramp",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("ecw", "territory")],
            "extras": {"destinations": ["wwf", "wcw", "midatlantic", "beast_works", "gsg", "japan"]},
            "desc": (
                "Interstate 95 heads north to New York and south to "
                "Baltimore, DC, and beyond. ECW tours the Northeast "
                "corridor in rented vans and borrowed cars.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("backstage", "ecw_arena", "ecw_backstage"),
        ("arena", "ecw_backstage", "ecw_arena"),
        ("gym", "ecw_arena", "ecw_gym"),
        ("arena", "ecw_gym", "ecw_arena"),
        ("bar", "ecw_arena", "ecw_bar"),
        ("pats", "ecw_arena", "ecw_bar"),
        ("arena", "ecw_bar", "ecw_arena"),
        ("office", "ecw_backstage", "ecw_office"),
        ("backstage", "ecw_office", "ecw_backstage"),
        ("travel", "ecw_arena", "ecw_travel"),
        ("back", "ecw_travel", "ecw_arena"),
    ],
}

# ============================================================
# UK (London, UK) — World of Sport
# ============================================================

NATIONAL_TERRITORIES["uk"] = {
    "name": "World of Sport Wrestling",
    "abbrev": "UK",
    "tier": 4,
    "location": "London, UK",
    "rooms": [
        {
            "key": "uk_arena",
            "name": "Royal Albert Hall",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("uk", "territory"), ("start_uk", "chargen")],
            "extras": {"capacity": 5000},
            "desc": (
                "The Royal Albert Hall — British wrestling at its most "
                "prestigious. World of Sport brings a distinctly British "
                "style: rounds-based matches, technical chain wrestling, "
                "and a stiff upper lip.\n\n"
                "The crowd is passionate but polite — no chair-throwing "
                "here. They appreciate the craft: clean breaks, technical "
                "exchanges, and the noble art of grappling."
            ),
        },
        {
            "key": "uk_backstage",
            "name": "Albert Hall Backstage",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("uk", "territory")],
            "desc": (
                "An ornate backstage area that reflects the venue's "
                "Victorian heritage. Proper changing rooms, tea service "
                "(naturally), and a level of decorum unusual in wrestling.\n\n"
                "British wrestling is its own world — different rules, "
                "different style, different expectations. Respect is "
                "earned on the mat, not on the microphone."
            ),
        },
        {
            "key": "uk_gym",
            "name": "The Snake Pit — Wigan",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("uk", "territory")],
            "extras": {"stat_bonus": "tec", "bonus_amount": 2},
            "desc": (
                "The Snake Pit in Wigan — the birthplace of catch "
                "wrestling and the most technically demanding training "
                "facility in the world. Billy Robinson's legacy lives "
                "here.\n\n"
                "Catch-as-catch-can wrestling. No ropes, no ring — just "
                "mats and holds. If you can survive the Snake Pit, you "
                "can out-wrestle anyone on the planet.\n\n"
                "|yTraining here gives a Technical bonus.|n"
            ),
        },
        {
            "key": "uk_pub",
            "name": "The Grappler's Arms",
            "typeclass": "typeclasses.rooms.BarRoom",
            "tags": [("uk", "territory")],
            "desc": (
                "A proper British pub near the Albert Hall. Dark wood, "
                "brass taps, and pints of bitter. Wrestling photos cover "
                "the walls — Big Daddy, Giant Haystacks, the legends of "
                "British wrestling.\n\n"
                "The landlord is a retired wrestler who still has the "
                "grip strength to crush a pint glass. Stories are traded "
                "over ale until closing time."
            ),
        },
        {
            "key": "uk_travel",
            "name": "Heathrow Airport",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("uk", "territory")],
            "extras": {"destinations": ["wwf", "wcw", "japan", "stampede", "midatlantic"]},
            "desc": (
                "Heathrow Airport — gateway to the world. British "
                "wrestlers travel to Japan, the US, and Europe. The "
                "international wrestling circuit runs through London.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("backstage", "uk_arena", "uk_backstage"),
        ("arena", "uk_backstage", "uk_arena"),
        ("gym", "uk_arena", "uk_gym"),
        ("wigan", "uk_arena", "uk_gym"),
        ("arena", "uk_gym", "uk_arena"),
        ("pub", "uk_arena", "uk_pub"),
        ("bar", "uk_arena", "uk_pub"),
        ("arena", "uk_pub", "uk_arena"),
        ("travel", "uk_arena", "uk_travel"),
        ("airport", "uk_arena", "uk_travel"),
        ("back", "uk_travel", "uk_arena"),
    ],
}

# ============================================================
# JAPAN (Tokyo, Japan) — AJPW/NJPW
# ============================================================

NATIONAL_TERRITORIES["japan"] = {
    "name": "All Japan / New Japan Pro Wrestling",
    "abbrev": "Japan",
    "tier": 4,
    "location": "Tokyo, Japan",
    "rooms": [
        {
            "key": "jp_arena",
            "name": "Nippon Budokan",
            "typeclass": "typeclasses.rooms.ArenaRoom",
            "tags": [("japan", "territory"), ("start_japan", "chargen")],
            "extras": {"capacity": 14000},
            "desc": (
                "The Nippon Budokan — Japan's most sacred wrestling venue. "
                "Originally built for judo at the 1964 Olympics, it now "
                "hosts the biggest shows in Japanese wrestling.\n\n"
                "Japanese wrestling is workrate above all. Matches are "
                "longer, stiffer, and more athletic than anywhere else. "
                "The crowd is respectful — silent during rest holds, "
                "explosive for big moves. Earning their respect is the "
                "ultimate achievement in the business."
            ),
        },
        {
            "key": "jp_backstage",
            "name": "Budokan Backstage",
            "typeclass": "typeclasses.rooms.LockerRoom",
            "tags": [("japan", "territory")],
            "desc": (
                "A meticulously organized backstage area. Hierarchy is "
                "absolute — young boys carry bags, clean boots, and cook "
                "meals for the veterans. Respect is earned through years "
                "of service.\n\n"
                "Foreign wrestlers (gaijin) are treated as special "
                "attractions but must earn the locker room's respect "
                "by working stiff and showing fighting spirit."
            ),
        },
        {
            "key": "jp_gym",
            "name": "The Dojo",
            "typeclass": "typeclasses.rooms.GymRoom",
            "tags": [("japan", "territory")],
            "extras": {"stat_bonus": "tec", "bonus_amount": 2},
            "desc": (
                "A traditional Japanese wrestling dojo. Tatami mats, a "
                "practice ring, and a shrine in the corner. Training "
                "starts at 5 AM. Breakfast is chanko nabe (sumo stew). "
                "The regimen is grueling.\n\n"
                "Japanese training emphasizes technical perfection, "
                "conditioning, and fighting spirit (never give up, "
                "never show weakness). A 3-year excursion here will "
                "make you world-class.\n\n"
                "|yTraining here gives a Technical bonus.|n"
            ),
        },
        {
            "key": "jp_bar",
            "name": "Shinjuku Izakaya",
            "typeclass": "typeclasses.rooms.BarRoom",
            "tags": [("japan", "territory")],
            "desc": (
                "A smoky izakaya (Japanese bar) in Shinjuku where the "
                "wrestlers drink after shows. Sake, beer, yakitori, and "
                "stories told in three languages. The foreign wrestlers "
                "cluster at one end, the Japanese roster at the other, "
                "but by the third round everyone's mixed together.\n\n"
                "Japanese drinking culture is mandatory — refusing the "
                "senior wrestlers is a career-limiting move."
            ),
        },
        {
            "key": "jp_office",
            "name": "NJPW / AJPW Office",
            "typeclass": "typeclasses.rooms.PromoterOffice",
            "tags": [("japan", "territory")],
            "extras": {"promoter_name": "Giant Bamba"},
            "desc": (
                "The corporate office of All Japan Pro Wrestling. Formal, "
                "corporate, and steeped in tradition. Giant Bamba's legacy "
                "looms over everything — his vision of wrestling as a "
                "legitimate athletic competition defines the Japanese style.\n\n"
                "Booking meetings are conducted with military precision. "
                "Match results are planned months in advance."
            ),
        },
        {
            "key": "jp_travel",
            "name": "Narita International Airport",
            "typeclass": "typeclasses.rooms.TravelHub",
            "tags": [("japan", "territory")],
            "extras": {"destinations": ["wwf", "wcw", "ecw", "uk", "stampede", "wccw", "midatlantic"]},
            "desc": (
                "Narita International Airport — the gateway between "
                "Japanese wrestling and the world. Talent exchanges "
                "flow constantly: gaijin come to Japan for excursions, "
                "Japanese wrestlers tour the US and Europe.\n\n"
                "|wType 'travel' to see available destinations.|n"
            ),
        },
    ],
    "exits": [
        ("backstage", "jp_arena", "jp_backstage"),
        ("arena", "jp_backstage", "jp_arena"),
        ("gym", "jp_arena", "jp_gym"),
        ("dojo", "jp_arena", "jp_gym"),
        ("arena", "jp_gym", "jp_arena"),
        ("bar", "jp_arena", "jp_bar"),
        ("izakaya", "jp_arena", "jp_bar"),
        ("arena", "jp_bar", "jp_arena"),
        ("office", "jp_backstage", "jp_office"),
        ("backstage", "jp_office", "jp_backstage"),
        ("travel", "jp_arena", "jp_travel"),
        ("airport", "jp_arena", "jp_travel"),
        ("back", "jp_travel", "jp_arena"),
    ],
}
