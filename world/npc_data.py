"""
Kayfabe: Protect the Business — NPC wrestler and manager data definitions.

Each NPC is a dict with:
    npc_id, name, based_on, territory, role, alignment,
    finisher_name, finisher_type, level, stats (str,agi,tec,cha,tou,psy)

Stats are raw integers. Level determines tier placement.
"""

# ============================================================
# ALL NPC WRESTLERS (~380)
# ============================================================

NPC_WRESTLERS = [

    # ----------------------------------------------------------
    # TERRITORY ERA (#1-50)
    # ----------------------------------------------------------
    {"npc_id": 1, "name": "Rick Fontaine", "based_on": "Ric Flair", "territory": "midatlantic", "role": "wrestler", "alignment": "Heel", "finisher_name": "Figure-Four Leglock", "finisher_type": "technical", "level": 40, "stats": (12, 11, 16, 20, 13, 19)},
    {"npc_id": 2, "name": "Rusty Roads", "based_on": "Dusty Rhodes", "territory": "florida", "role": "wrestler", "alignment": "Face", "finisher_name": "Bionic Elbow", "finisher_type": "power", "level": 38, "stats": (14, 7, 11, 20, 16, 18)},
    {"npc_id": 3, "name": "Ricky Riverdale", "based_on": "Ricky Steamboat", "territory": "midatlantic", "role": "wrestler", "alignment": "Face", "finisher_name": "Deep Body Press", "finisher_type": "aerial", "level": 38, "stats": (12, 16, 17, 16, 13, 18)},
    {"npc_id": 4, "name": "Art Alderson", "based_on": "Arn Anderson", "territory": "midatlantic", "role": "wrestler", "alignment": "Heel", "finisher_name": "Spinebuster", "finisher_type": "power", "level": 35, "stats": (15, 8, 16, 13, 16, 18)},
    {"npc_id": 5, "name": "Tyler Blanford", "based_on": "Tully Blanchard", "territory": "midatlantic", "role": "wrestler", "alignment": "Heel", "finisher_name": "Slingshot Suplex", "finisher_type": "technical", "level": 33, "stats": (12, 11, 15, 14, 12, 16)},
    {"npc_id": 6, "name": "Magnus T.A.", "based_on": "Magnum T.A.", "territory": "midatlantic", "role": "wrestler", "alignment": "Face", "finisher_name": "Belly-to-Belly Suplex", "finisher_type": "power", "level": 33, "stats": (15, 10, 13, 16, 14, 15)},
    {"npc_id": 7, "name": "Chief Thunderhawk", "based_on": "Wahoo McDaniel", "territory": "midatlantic", "role": "wrestler", "alignment": "Face", "finisher_name": "Tomahawk Chop", "finisher_type": "power", "level": 32, "stats": (16, 8, 11, 13, 17, 14)},
    {"npc_id": 8, "name": "Hawk Hogan", "based_on": "Hulk Hogan", "territory": "wwf", "role": "wrestler", "alignment": "Face", "finisher_name": "Atomic Leg Drop", "finisher_type": "charisma", "level": 45, "stats": (16, 7, 8, 20, 17, 14)},
    {"npc_id": 9, "name": "Bruno Sammarco", "based_on": "Bruno Sammartino", "territory": "wwf", "role": "wrestler", "alignment": "Face", "finisher_name": "Bear Hug", "finisher_type": "power", "level": 42, "stats": (19, 6, 13, 16, 19, 16)},
    {"npc_id": 10, "name": "Antoine the Giant", "based_on": "Andre the Giant", "territory": "wwf", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Sitdown Splash", "finisher_type": "power", "level": 42, "stats": (20, 3, 8, 17, 20, 13)},
    {"npc_id": 11, "name": '"Wild Man" Randy Salvatore', "based_on": "Randy Savage", "territory": "wwf", "role": "wrestler", "alignment": "Heel", "finisher_name": "Flying Elbow Drop", "finisher_type": "aerial", "level": 40, "stats": (13, 14, 13, 18, 14, 17)},
    {"npc_id": 12, "name": "Roddy Viper", "based_on": "Roddy Piper", "territory": "pnw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Sleeper Hold", "finisher_type": "technical", "level": 38, "stats": (13, 10, 12, 19, 15, 18)},
    {"npc_id": 13, "name": 'Jake "The Serpent" Rollins', "based_on": "Jake Roberts", "territory": "wwf", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "DDT", "finisher_type": "technical", "level": 36, "stats": (12, 9, 14, 17, 13, 20)},
    {"npc_id": 14, "name": "The Gravedigger", "based_on": "Undertaker", "territory": "wwf", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Tombstone Piledriver", "finisher_type": "power", "level": 44, "stats": (16, 10, 13, 18, 18, 17)},
    {"npc_id": 15, "name": "Brett Harmon", "based_on": "Bret Hart", "territory": "stampede", "role": "wrestler", "alignment": "Face", "finisher_name": "Sharpshooter", "finisher_type": "technical", "level": 42, "stats": (13, 13, 19, 15, 15, 19)},
    {"npc_id": 16, "name": "Oliver Harmon", "based_on": "Owen Hart", "territory": "stampede", "role": "wrestler", "alignment": "Heel", "finisher_name": "Enziguiri", "finisher_type": "aerial", "level": 35, "stats": (11, 16, 17, 14, 12, 16)},
    {"npc_id": 17, "name": "The Supreme Savage", "based_on": "Ultimate Warrior", "territory": "wwf", "role": "wrestler", "alignment": "Face", "finisher_name": "Gorilla Press Splash", "finisher_type": "power", "level": 38, "stats": (18, 10, 5, 17, 16, 6)},
    {"npc_id": 18, "name": '"Billion Dollar Man" Ted DiMarco', "based_on": "Ted DiBiase", "territory": "midsouth", "role": "wrestler", "alignment": "Heel", "finisher_name": "Million Dollar Dream", "finisher_type": "technical", "level": 37, "stats": (14, 10, 15, 17, 14, 17)},
    {"npc_id": 19, "name": "Kerry Von Adler", "based_on": "Kerry Von Erich", "territory": "wccw", "role": "wrestler", "alignment": "Face", "finisher_name": "Iron Claw", "finisher_type": "power", "level": 36, "stats": (16, 12, 11, 17, 15, 13)},
    {"npc_id": 20, "name": "Kevin Von Adler", "based_on": "Kevin Von Erich", "territory": "wccw", "role": "wrestler", "alignment": "Face", "finisher_name": "Tornado Punch", "finisher_type": "power", "level": 35, "stats": (14, 15, 12, 16, 14, 13)},
    {"npc_id": 21, "name": "David Von Adler", "based_on": "David Von Erich", "territory": "wccw", "role": "wrestler", "alignment": "Face", "finisher_name": "Iron Claw", "finisher_type": "power", "level": 30, "stats": (15, 11, 11, 15, 13, 12)},
    {"npc_id": 22, "name": 'Mitchell "PS" Hale', "based_on": "Michael Hayes", "territory": "wccw", "role": "wrestler", "alignment": "Heel", "finisher_name": "DDT", "finisher_type": "technical", "level": 33, "stats": (11, 9, 11, 18, 12, 15)},
    {"npc_id": 23, "name": 'Terry "Boom Boom" Gordon', "based_on": "Terry Gordy", "territory": "wccw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Powerbomb", "finisher_type": "power", "level": 35, "stats": (17, 8, 12, 11, 17, 14)},
    {"npc_id": 24, "name": "Buddy Robards", "based_on": "Buddy Roberts", "territory": "wccw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Eye Rake", "finisher_type": "charisma", "level": 28, "stats": (10, 10, 10, 14, 11, 13)},
    {"npc_id": 25, "name": "Jerry Crowley", "based_on": "Jerry Lawler", "territory": "memphis", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Piledriver", "finisher_type": "power", "level": 35, "stats": (13, 9, 12, 19, 14, 18)},
    {"npc_id": 26, "name": "Andy Coughlin", "based_on": "Andy Kaufman", "territory": "memphis", "role": "wrestler", "alignment": "Heel", "finisher_name": "Slap", "finisher_type": "charisma", "level": 10, "stats": (3, 5, 2, 20, 3, 8)},
    {"npc_id": 27, "name": "Bill Brisbane", "based_on": "Bill Dundee", "territory": "memphis", "role": "wrestler", "alignment": "Heel", "finisher_name": "Diving Headbutt", "finisher_type": "aerial", "level": 28, "stats": (11, 12, 13, 15, 13, 16)},
    {"npc_id": 28, "name": "Jimmy Gallant", "based_on": "Jimmy Valiant", "territory": "memphis", "role": "wrestler", "alignment": "Face", "finisher_name": "Elbow Drop", "finisher_type": "power", "level": 25, "stats": (14, 8, 9, 16, 15, 12)},
    {"npc_id": 29, "name": "Vernon Gavin", "based_on": "Verne Gagne", "territory": "awa", "role": "wrestler", "alignment": "Face", "finisher_name": "Sleeper Hold", "finisher_type": "technical", "level": 38, "stats": (14, 10, 18, 15, 15, 18)},
    {"npc_id": 30, "name": "Nick Buckminster", "based_on": "Nick Bockwinkel", "territory": "awa", "role": "wrestler", "alignment": "Heel", "finisher_name": "Piledriver", "finisher_type": "power", "level": 36, "stats": (13, 10, 17, 16, 14, 18)},
    {"npc_id": 31, "name": "The Grinder", "based_on": "The Crusher", "territory": "awa", "role": "wrestler", "alignment": "Face", "finisher_name": "Bolo Punch", "finisher_type": "power", "level": 30, "stats": (16, 7, 8, 14, 17, 11)},
    {"npc_id": 32, "name": "Rabid Dog Vachon", "based_on": "Mad Dog Vachon", "territory": "awa", "role": "wrestler", "alignment": "Heel", "finisher_name": "Biting", "finisher_type": "power", "level": 30, "stats": (15, 8, 7, 13, 16, 10)},
    {"npc_id": 33, "name": "Kurt Hennison", "based_on": "Curt Hennig", "territory": "awa", "role": "wrestler", "alignment": "Heel", "finisher_name": "Perfectplex", "finisher_type": "technical", "level": 36, "stats": (13, 14, 16, 16, 12, 17)},
    {"npc_id": 34, "name": "Larry Zablonski", "based_on": "Larry Zbyszko", "territory": "awa", "role": "wrestler", "alignment": "Heel", "finisher_name": "Swinging Neckbreaker", "finisher_type": "technical", "level": 30, "stats": (12, 9, 15, 13, 13, 15)},
    {"npc_id": 35, "name": '"Dr. Damage" Stan Williamson', "based_on": "Dr. Death Steve Williams", "territory": "midsouth", "role": "wrestler", "alignment": "Face", "finisher_name": "Oklahoma Stampede", "finisher_type": "power", "level": 35, "stats": (18, 8, 14, 11, 18, 13)},
    {"npc_id": 36, "name": "Salvage Yard Hound", "based_on": "Junkyard Dog", "territory": "midsouth", "role": "wrestler", "alignment": "Face", "finisher_name": "Thump", "finisher_type": "power", "level": 33, "stats": (16, 7, 8, 18, 16, 12)},
    {"npc_id": 37, "name": "Buzzsaw Jim Dugan", "based_on": "Hacksaw Jim Duggan", "territory": "midsouth", "role": "wrestler", "alignment": "Face", "finisher_name": "Three-Point Clothesline", "finisher_type": "power", "level": 30, "stats": (16, 6, 7, 15, 16, 10)},
    {"npc_id": 38, "name": "Keith Solomon", "based_on": "Kevin Sullivan", "territory": "florida", "role": "wrestler", "alignment": "Heel", "finisher_name": "Double Stomp", "finisher_type": "power", "level": 30, "stats": (13, 8, 11, 15, 14, 16)},
    {"npc_id": 39, "name": "Barry Wyndham", "based_on": "Barry Windham", "territory": "florida", "role": "wrestler", "alignment": "Face", "finisher_name": "Superplex", "finisher_type": "power", "level": 34, "stats": (15, 11, 15, 13, 14, 16)},
    {"npc_id": 40, "name": '"Megastar" Billy Grayham', "based_on": "Superstar Billy Graham", "territory": "florida", "role": "wrestler", "alignment": "Heel", "finisher_name": "Bear Hug", "finisher_type": "power", "level": 33, "stats": (18, 6, 8, 18, 15, 11)},
    {"npc_id": 41, "name": "Tommy Richmond", "based_on": "Tommy Rich", "territory": "georgia", "role": "wrestler", "alignment": "Face", "finisher_name": "Thesz Press", "finisher_type": "technical", "level": 28, "stats": (12, 10, 13, 15, 12, 14)},
    {"npc_id": 42, "name": "Beastly & Havok", "based_on": "Road Warriors", "territory": "midatlantic", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Doomsday Device", "finisher_type": "power", "level": 38, "stats": (19, 8, 8, 16, 19, 12)},
    {"npc_id": 43, "name": "Davey Bull Smythe", "based_on": "British Bulldog", "territory": "stampede", "role": "wrestler", "alignment": "Face", "finisher_name": "Running Powerslam", "finisher_type": "power", "level": 34, "stats": (17, 12, 12, 13, 15, 13)},
    {"npc_id": 44, "name": "Dynamo Keith", "based_on": "Dynamite Kid", "territory": "stampede", "role": "wrestler", "alignment": "Heel", "finisher_name": "Diving Headbutt", "finisher_type": "aerial", "level": 33, "stats": (12, 17, 16, 10, 13, 15)},
    {"npc_id": 45, "name": "Stuart Harmon", "based_on": "Stu Hart", "territory": "stampede", "role": "trainer", "alignment": "Face", "finisher_name": "Stretching", "finisher_type": "technical", "level": 40, "stats": (14, 6, 20, 12, 17, 20)},
    {"npc_id": 46, "name": "Terry Bronco", "based_on": "Terry Funk", "territory": "wccw", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Spinning Toe Hold", "finisher_type": "technical", "level": 38, "stats": (14, 9, 15, 16, 17, 18)},
    {"npc_id": 47, "name": "Stan Hanssen", "based_on": "Stan Hansen", "territory": "japan", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Western Lariat", "finisher_type": "power", "level": 38, "stats": (18, 8, 13, 12, 18, 15)},
    {"npc_id": 48, "name": "Johnny Sinclair", "based_on": "Johnny Saint", "territory": "uk", "role": "wrestler", "alignment": "Face", "finisher_name": "Chain Wrestling", "finisher_type": "technical", "level": 30, "stats": (8, 14, 19, 12, 10, 17)},
    {"npc_id": 49, "name": "Chris Adkins", "based_on": "Chris Adams", "territory": "wccw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Superkick", "finisher_type": "aerial", "level": 30, "stats": (12, 14, 13, 13, 12, 14)},
    {"npc_id": 50, "name": "Ladykiller Buddy Bloom", "based_on": "Buddy Rose", "territory": "pnw", "role": "wrestler", "alignment": "Heel", "finisher_name": "DDT", "finisher_type": "technical", "level": 28, "stats": (13, 9, 13, 15, 13, 14)},

    # ----------------------------------------------------------
    # PENSACOLA TRAINING CENTER (#51-70)
    # ----------------------------------------------------------
    {"npc_id": 51, "name": "Chief Afa Savea", "based_on": "Afa Anoa'i", "territory": "pensacola", "role": "trainer", "alignment": "Face", "finisher_name": "Samoan Drop", "finisher_type": "power", "level": 40, "stats": (16, 8, 14, 15, 18, 19)},
    {"npc_id": 52, "name": "Chief Sika Savea", "based_on": "Sika Anoa'i", "territory": "pensacola", "role": "trainer", "alignment": "Face", "finisher_name": "Samoan Drop", "finisher_type": "power", "level": 40, "stats": (17, 7, 13, 14, 19, 18)},
    {"npc_id": 53, "name": "Master Matsuda", "based_on": "Hiro Matsuda", "territory": "pensacola", "role": "trainer", "alignment": "Heel", "finisher_name": "Leg Break", "finisher_type": "technical", "level": 40, "stats": (14, 10, 20, 12, 16, 20)},
    {"npc_id": 54, "name": '"The Mountain" Tua Savea', "based_on": "Yokozuna", "territory": "pensacola", "role": "wrestler", "alignment": "Heel", "finisher_name": "Banzai Drop", "finisher_type": "power", "level": 20, "stats": (18, 4, 8, 12, 17, 10)},
    {"npc_id": 55, "name": '"Big Sola" Fatu', "based_on": "Rikishi", "territory": "pensacola", "role": "wrestler", "alignment": "Face", "finisher_name": "Stinkface", "finisher_type": "charisma", "level": 18, "stats": (15, 7, 9, 14, 16, 11)},
    {"npc_id": 56, "name": '"The Savage" Eddo Fatu', "based_on": "Umaga", "territory": "pensacola", "role": "wrestler", "alignment": "Heel", "finisher_name": "Samoan Spike", "finisher_type": "power", "level": 22, "stats": (17, 8, 7, 10, 17, 9)},
    {"npc_id": 57, "name": "Roman Savea", "based_on": "Roman Reigns", "territory": "pensacola", "role": "wrestler", "alignment": "Face", "finisher_name": "Spear", "finisher_type": "power", "level": 15, "stats": (14, 10, 11, 15, 14, 13)},
    {"npc_id": 58, "name": "Jay & Jimmy Fatu", "based_on": "The Usos", "territory": "pensacola", "role": "wrestler", "alignment": "Face", "finisher_name": "Superkick", "finisher_type": "aerial", "level": 15, "stats": (12, 14, 11, 14, 12, 12)},
    {"npc_id": 59, "name": "Solo Savea", "based_on": "Solo Sikoa", "territory": "pensacola", "role": "wrestler", "alignment": "Heel", "finisher_name": "Samoan Spike", "finisher_type": "power", "level": 12, "stats": (15, 9, 8, 11, 14, 9)},
    {"npc_id": 60, "name": "Nia Fane", "based_on": "Nia Jax", "territory": "pensacola", "role": "wrestler", "alignment": "Heel", "finisher_name": "Leg Drop", "finisher_type": "power", "level": 14, "stats": (16, 6, 6, 10, 15, 7)},
    {"npc_id": 61, "name": '"Coconut" Jimmy Snooks Jr.', "based_on": "Jimmy Snuka Jr.", "territory": "pensacola", "role": "wrestler", "alignment": "Face", "finisher_name": "Superfly Splash", "finisher_type": "aerial", "level": 12, "stats": (10, 14, 9, 11, 10, 9)},
    {"npc_id": 62, "name": '"Samoan Storm" Manu Savea', "based_on": "Manu", "territory": "pensacola", "role": "wrestler", "alignment": "Face", "finisher_name": "Samoan Drop", "finisher_type": "power", "level": 10, "stats": (14, 8, 7, 9, 13, 8)},
    {"npc_id": 63, "name": "Samu Savea", "based_on": "Samu", "territory": "pensacola", "role": "wrestler", "alignment": "Heel", "finisher_name": "Diving Headbutt", "finisher_type": "aerial", "level": 18, "stats": (15, 9, 10, 10, 15, 11)},
    {"npc_id": 64, "name": "Luna Vasquez", "based_on": "Luna Vachon", "territory": "pensacola", "role": "wrestler", "alignment": "Heel", "finisher_name": "Moonsault", "finisher_type": "aerial", "level": 20, "stats": (12, 13, 11, 14, 13, 12)},
    {"npc_id": 65, "name": '"Superfly" Jimmy Snooks', "based_on": "Jimmy Snuka", "territory": "pensacola", "role": "wrestler", "alignment": "Face", "finisher_name": "Superfly Splash", "finisher_type": "aerial", "level": 30, "stats": (13, 16, 10, 16, 13, 12)},
    {"npc_id": 66, "name": 'Brutus "The Blade" Beefsteak', "based_on": "Brutus Beefcake", "territory": "pensacola", "role": "wrestler", "alignment": "Face", "finisher_name": "Sleeper", "finisher_type": "technical", "level": 22, "stats": (12, 9, 9, 14, 12, 10)},
    {"npc_id": 67, "name": '"The Kid" Billy Kidwell', "based_on": "Billy Kidman", "territory": "pensacola", "role": "wrestler", "alignment": "Face", "finisher_name": "Shooting Star Press", "finisher_type": "aerial", "level": 15, "stats": (8, 16, 12, 12, 9, 12)},
    {"npc_id": 68, "name": "Malia Hoskins", "based_on": "Tamina Snuka", "territory": "pensacola", "role": "wrestler", "alignment": "Heel", "finisher_name": "Superfly Splash", "finisher_type": "aerial", "level": 14, "stats": (14, 9, 8, 9, 13, 8)},
    {"npc_id": 69, "name": "High Chief Pita Maivia", "based_on": "Peter Maivia", "territory": "pensacola", "role": "trainer", "alignment": "Face", "finisher_name": "Headbutt", "finisher_type": "power", "level": 35, "stats": (15, 8, 12, 14, 16, 16)},
    {"npc_id": 70, "name": 'Gene "The Machine" Snitzky', "based_on": "Gene Snitsky", "territory": "pensacola", "role": "wrestler", "alignment": "Heel", "finisher_name": "Pumphandle Slam", "finisher_type": "power", "level": 16, "stats": (16, 5, 5, 8, 15, 6)},

    # ----------------------------------------------------------
    # OVW DEVELOPMENTAL (#71-91)
    # ----------------------------------------------------------
    {"npc_id": 71, "name": "The Prototype", "based_on": "John Cena", "territory": "ovw", "role": "wrestler", "alignment": "Face", "finisher_name": "FU", "finisher_type": "power", "level": 20, "stats": (15, 9, 10, 16, 14, 12)},
    {"npc_id": 72, "name": "Leviathan", "based_on": "Batista", "territory": "ovw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Bautiste Bomb", "finisher_type": "power", "level": 18, "stats": (17, 7, 7, 13, 16, 9)},
    {"npc_id": 73, "name": "Brock Lester", "based_on": "Brock Lesnar", "territory": "ovw", "role": "wrestler", "alignment": "Heel", "finisher_name": "F-5", "finisher_type": "power", "level": 22, "stats": (19, 12, 13, 11, 17, 11)},
    {"npc_id": 74, "name": "Randy Viper", "based_on": "Randy Orton", "territory": "ovw", "role": "wrestler", "alignment": "Heel", "finisher_name": "RKO", "finisher_type": "technical", "level": 18, "stats": (12, 13, 13, 15, 12, 14)},
    {"npc_id": 75, "name": "Sheldon Banks", "based_on": "Shelton Benjamin", "territory": "ovw", "role": "wrestler", "alignment": "Face", "finisher_name": "T-Bone Suplex", "finisher_type": "power", "level": 18, "stats": (14, 16, 15, 10, 13, 12)},
    {"npc_id": 76, "name": "C.M. Phillips", "based_on": "CM Punk", "territory": "ovw", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "GTS", "finisher_type": "technical", "level": 20, "stats": (11, 12, 15, 17, 12, 16)},
    {"npc_id": 77, "name": "Bobby Lash", "based_on": "Bobby Lashley", "territory": "ovw", "role": "wrestler", "alignment": "Face", "finisher_name": "Dominator", "finisher_type": "power", "level": 18, "stats": (18, 10, 10, 10, 16, 9)},
    {"npc_id": 78, "name": "Mike Kennedy", "based_on": "Mr. Kennedy", "territory": "ovw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Green Bay Plunge", "finisher_type": "aerial", "level": 16, "stats": (12, 11, 11, 15, 12, 12)},
    {"npc_id": 79, "name": "Cody Rhoades", "based_on": "Cody Rhodes", "territory": "ovw", "role": "wrestler", "alignment": "Face", "finisher_name": "Cross Rhodes", "finisher_type": "technical", "level": 16, "stats": (12, 12, 14, 15, 11, 14)},
    {"npc_id": 80, "name": "Ted DiBrasi Jr.", "based_on": "Ted DiBiase Jr", "territory": "ovw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Dream Street", "finisher_type": "technical", "level": 14, "stats": (13, 10, 12, 12, 12, 11)},
    {"npc_id": 81, "name": "Kofi Kingsley", "based_on": "Kofi Kingston", "territory": "ovw", "role": "wrestler", "alignment": "Face", "finisher_name": "Trouble in Paradise", "finisher_type": "aerial", "level": 16, "stats": (10, 16, 12, 14, 11, 12)},
    {"npc_id": 82, "name": "Nick Nemeth", "based_on": "Dolph Ziggler", "territory": "ovw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Zig Zag", "finisher_type": "technical", "level": 16, "stats": (11, 14, 14, 14, 12, 14)},
    {"npc_id": 83, "name": "Mike Mizanin", "based_on": "The Miz", "territory": "ovw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Skull Crushing Finale", "finisher_type": "technical", "level": 16, "stats": (11, 10, 11, 17, 11, 13)},
    {"npc_id": 84, "name": "Beth Fenix", "based_on": "Beth Phoenix", "territory": "ovw", "role": "wrestler", "alignment": "Face", "finisher_name": "Glam Slam", "finisher_type": "power", "level": 18, "stats": (15, 10, 12, 13, 14, 12)},
    {"npc_id": 85, "name": "Mickie Jameson", "based_on": "Mickie James", "territory": "ovw", "role": "wrestler", "alignment": "Face", "finisher_name": "Mickie-DT", "finisher_type": "technical", "level": 16, "stats": (10, 13, 13, 14, 11, 13)},
    {"npc_id": 86, "name": "Nick Dunsmore", "based_on": "Eugene", "territory": "ovw", "role": "wrestler", "alignment": "Face", "finisher_name": "Stunner", "finisher_type": "technical", "level": 14, "stats": (12, 10, 13, 12, 12, 10)},
    {"npc_id": 87, "name": "Simon Deen", "based_on": "Nova", "territory": "ovw", "role": "trainer", "alignment": "Face", "finisher_name": "Kryptonite Krunch", "finisher_type": "power", "level": 22, "stats": (13, 11, 14, 12, 13, 14)},
    {"npc_id": 88, "name": "Rico Constantine", "based_on": "Rico", "territory": "ovw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Spin Kick", "finisher_type": "aerial", "level": 14, "stats": (11, 12, 11, 14, 10, 11)},
    {"npc_id": 89, "name": '"Nightmare" Danny Dusk', "based_on": "Danny Davis", "territory": "ovw", "role": "authority", "alignment": "Face", "finisher_name": "n/a", "finisher_type": "power", "level": 30, "stats": (10, 7, 10, 15, 10, 16)},
    {"npc_id": 90, "name": "Jim Corwin", "based_on": "Jim Cornette", "territory": "ovw", "role": "authority", "alignment": "Heel", "finisher_name": "Tennis Racket", "finisher_type": "charisma", "level": 1, "stats": (4, 4, 6, 19, 4, 20)},
    {"npc_id": 91, "name": "Al Frost", "based_on": "Al Snow", "territory": "ovw", "role": "wrestler", "alignment": "Face", "finisher_name": "Snow Plow", "finisher_type": "power", "level": 28, "stats": (14, 11, 14, 13, 14, 15)},

    # ----------------------------------------------------------
    # FCW / DSW / HWA DEVELOPMENTAL (#92-103)
    # ----------------------------------------------------------
    {"npc_id": 92, "name": '"Iron Steve" Keirn', "based_on": "Steve Keirn", "territory": "fcw", "role": "trainer", "alignment": "Face", "finisher_name": "n/a", "finisher_type": "technical", "level": 30, "stats": (12, 10, 14, 14, 12, 16)},
    {"npc_id": 93, "name": '"Sergeant" Bill DeMott', "based_on": "Bill DeMott", "territory": "dsw", "role": "trainer", "alignment": "Heel", "finisher_name": "No Laughing Matter", "finisher_type": "power", "level": 28, "stats": (15, 7, 10, 12, 15, 13)},
    {"npc_id": 94, "name": "Les Thatcher", "based_on": "Les Thatcher", "territory": "hwa", "role": "trainer", "alignment": "Face", "finisher_name": "n/a", "finisher_type": "technical", "level": 30, "stats": (10, 8, 16, 16, 10, 20)},
    {"npc_id": 95, "name": "Seth Blackburn", "based_on": "Seth Rollins", "territory": "fcw", "role": "wrestler", "alignment": "Face", "finisher_name": "Blackout", "finisher_type": "aerial", "level": 18, "stats": (13, 16, 15, 14, 12, 14)},
    {"npc_id": 96, "name": "Dean Amberson", "based_on": "Dean Ambrose", "territory": "fcw", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Dirty Deeds", "finisher_type": "technical", "level": 18, "stats": (13, 11, 12, 15, 14, 14)},
    {"npc_id": 97, "name": "Naomi Fatu", "based_on": "Naomi", "territory": "fcw", "role": "wrestler", "alignment": "Face", "finisher_name": "Rear View", "finisher_type": "aerial", "level": 14, "stats": (10, 15, 10, 13, 10, 10)},
    {"npc_id": 98, "name": "Bray Rotunda", "based_on": "Bray Wyatt", "territory": "fcw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Sister Abigail", "finisher_type": "charisma", "level": 18, "stats": (14, 8, 11, 17, 14, 15)},
    {"npc_id": 99, "name": '"Big Red" Knox', "based_on": "Kane", "territory": "dsw", "role": "trainer", "alignment": "Anti-Hero", "finisher_name": "Chokeslam", "finisher_type": "power", "level": 35, "stats": (17, 9, 11, 14, 17, 13)},
    {"npc_id": 100, "name": "Cody Rhoades Jr.", "based_on": "Cody Rhodes (DSW)", "territory": "dsw", "role": "wrestler", "alignment": "Face", "finisher_name": "Cross Rhodes", "finisher_type": "technical", "level": 14, "stats": (11, 11, 13, 14, 10, 12)},
    {"npc_id": 101, "name": "Bobby Lash Jr.", "based_on": "Bobby Lashley (DSW)", "territory": "dsw", "role": "wrestler", "alignment": "Face", "finisher_name": "Dominator", "finisher_type": "power", "level": 16, "stats": (17, 9, 9, 9, 15, 8)},
    {"npc_id": 102, "name": 'Brian "The Dragon" Danielson', "based_on": "Bryan Danielson", "territory": "hwa", "role": "wrestler", "alignment": "Face", "finisher_name": "Cattle Mutilation", "finisher_type": "technical", "level": 18, "stats": (11, 14, 18, 13, 13, 16)},
    {"npc_id": 103, "name": "Nick Nemeth Jr.", "based_on": "Dolph Ziggler (HWA)", "territory": "hwa", "role": "wrestler", "alignment": "Heel", "finisher_name": "Zig Zag", "finisher_type": "technical", "level": 14, "stats": (10, 13, 13, 13, 11, 12)},

    # ----------------------------------------------------------
    # ADDITIONAL TERRITORY ERA + ANNOUNCERS (#104-118)
    # ----------------------------------------------------------
    {"npc_id": 104, "name": '"Ice Cold" Steve Austen', "based_on": "Steve Austin", "territory": "wwf", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Stone Cold Stunner", "finisher_type": "technical", "level": 44, "stats": (15, 10, 14, 19, 16, 17)},
    {"npc_id": 105, "name": "Gordon Stoley", "based_on": "Gordon Solie", "territory": "georgia", "role": "announcer", "alignment": "Face", "finisher_name": "", "finisher_type": "", "level": 1, "stats": (3, 3, 5, 18, 5, 20)},
    {"npc_id": 106, "name": "Jim Roth", "based_on": "Jim Ross", "territory": "midsouth", "role": "announcer", "alignment": "Face", "finisher_name": "", "finisher_type": "", "level": 1, "stats": (3, 3, 5, 18, 5, 20)},
    {"npc_id": 107, "name": "Lance Rosemont", "based_on": "Lance Russell", "territory": "memphis", "role": "announcer", "alignment": "Face", "finisher_name": "", "finisher_type": "", "level": 1, "stats": (3, 3, 5, 18, 5, 20)},
    {"npc_id": 108, "name": "Giant Bamba", "based_on": "Giant Baba", "territory": "japan", "role": "wrestler", "alignment": "Face", "finisher_name": "Running Neckbreaker", "finisher_type": "power", "level": 38, "stats": (17, 6, 13, 14, 16, 16)},
    {"npc_id": 109, "name": "Antonio Inagi", "based_on": "Antonio Inoki", "territory": "japan", "role": "wrestler", "alignment": "Face", "finisher_name": "Enziguiri", "finisher_type": "technical", "level": 40, "stats": (14, 12, 18, 16, 15, 18)},
    {"npc_id": 110, "name": "Jumbo Tsukuda", "based_on": "Jumbo Tsuruta", "territory": "japan", "role": "wrestler", "alignment": "Face", "finisher_name": "Knee Lift", "finisher_type": "power", "level": 38, "stats": (16, 11, 16, 13, 16, 17)},
    {"npc_id": 111, "name": "Large Lad", "based_on": "Big Daddy", "territory": "uk", "role": "wrestler", "alignment": "Face", "finisher_name": "Belly Splash", "finisher_type": "power", "level": 30, "stats": (17, 4, 6, 16, 18, 10)},
    {"npc_id": 112, "name": "Colossal Haymaker", "based_on": "Giant Haystacks", "territory": "uk", "role": "wrestler", "alignment": "Heel", "finisher_name": "Splash", "finisher_type": "power", "level": 30, "stats": (18, 3, 5, 13, 19, 9)},
    {"npc_id": 113, "name": "Pat Finney", "based_on": "Fit Finlay", "territory": "uk", "role": "wrestler", "alignment": "Heel", "finisher_name": "Celtic Cross", "finisher_type": "power", "level": 32, "stats": (14, 10, 16, 11, 16, 16)},
    {"npc_id": 114, "name": '"Iron" Mike Rotunda', "based_on": "Mike Rotundo", "territory": "midsouth", "role": "wrestler", "alignment": "Heel", "finisher_name": "Airplane Spin", "finisher_type": "technical", "level": 30, "stats": (14, 9, 15, 11, 14, 14)},
    {"npc_id": 115, "name": "Lex Lugar", "based_on": "Lex Luger", "territory": "midatlantic", "role": "wrestler", "alignment": "Face", "finisher_name": "Torture Rack", "finisher_type": "power", "level": 34, "stats": (17, 9, 10, 14, 15, 11)},
    {"npc_id": 116, "name": '"Ravishing" Rick Rood', "based_on": "Rick Rude", "territory": "awa", "role": "wrestler", "alignment": "Heel", "finisher_name": "Rude Awakening", "finisher_type": "technical", "level": 34, "stats": (15, 11, 13, 16, 14, 14)},
    {"npc_id": 117, "name": '"Mr. Magnificent" Paul Orndoff', "based_on": "Paul Orndorff", "territory": "midsouth", "role": "wrestler", "alignment": "Heel", "finisher_name": "Piledriver", "finisher_type": "power", "level": 32, "stats": (15, 10, 12, 14, 14, 13)},
    {"npc_id": 118, "name": "Harley Reece", "based_on": "Harley Race", "territory": "midsouth", "role": "wrestler", "alignment": "Heel", "finisher_name": "Diving Headbutt", "finisher_type": "aerial", "level": 38, "stats": (16, 8, 15, 14, 18, 18)},

    # ----------------------------------------------------------
    # ECW (#119-133)
    # ----------------------------------------------------------
    {"npc_id": 119, "name": '"The Sandstorm" Sandy White', "based_on": "Sandman", "territory": "ecw", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "White Russian Legsweep", "finisher_type": "power", "level": 28, "stats": (13, 7, 6, 16, 16, 10)},
    {"npc_id": 120, "name": "Tommy Dreaming", "based_on": "Tommy Dreamer", "territory": "ecw", "role": "wrestler", "alignment": "Face", "finisher_name": "Dreamer DDT", "finisher_type": "technical", "level": 28, "stats": (13, 9, 11, 15, 16, 13)},
    {"npc_id": 121, "name": "Raven Darkholme", "based_on": "Raven", "territory": "ecw", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Evenflow DDT", "finisher_type": "technical", "level": 30, "stats": (12, 10, 13, 17, 13, 17)},
    {"npc_id": 122, "name": "Sabu al-Rashid", "based_on": "Sabu", "territory": "ecw", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Triple Jump Moonsault", "finisher_type": "aerial", "level": 30, "stats": (11, 18, 10, 14, 14, 10)},
    {"npc_id": 123, "name": "Rob Van Dyke", "based_on": "Rob Van Dam", "territory": "ecw", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Five Star Frog Splash", "finisher_type": "aerial", "level": 34, "stats": (12, 18, 14, 16, 13, 13)},
    {"npc_id": 124, "name": "Shane Dalton", "based_on": "Shane Douglas", "territory": "ecw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Belly-to-Belly Suplex", "finisher_type": "power", "level": 28, "stats": (13, 9, 13, 16, 13, 14)},
    {"npc_id": 125, "name": '"The Crippler" Chris Benning', "based_on": "Chris Benoit", "territory": "ecw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Crossface", "finisher_type": "technical", "level": 36, "stats": (14, 13, 19, 10, 15, 17)},
    {"npc_id": 126, "name": "Eddie Guerrera", "based_on": "Eddie Guerrero", "territory": "ecw", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Frog Splash", "finisher_type": "aerial", "level": 38, "stats": (12, 16, 18, 18, 13, 18)},
    {"npc_id": 127, "name": "Taz Simmons", "based_on": "Taz", "territory": "ecw", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Taz-mission", "finisher_type": "technical", "level": 28, "stats": (15, 9, 16, 13, 15, 13)},
    {"npc_id": 128, "name": "Mike Awesome Powers", "based_on": "Mike Awesome", "territory": "ecw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Awesome Bomb", "finisher_type": "power", "level": 28, "stats": (17, 11, 10, 10, 15, 10)},
    {"npc_id": 129, "name": "Jerry Lydon", "based_on": "Jerry Lynn", "territory": "ecw", "role": "wrestler", "alignment": "Face", "finisher_name": "Cradle Piledriver", "finisher_type": "technical", "level": 28, "stats": (11, 14, 16, 12, 12, 15)},
    {"npc_id": 130, "name": "Lance Tempest", "based_on": "Lance Storm", "territory": "ecw", "role": "wrestler", "alignment": "Face", "finisher_name": "Canadian Maple Leaf", "finisher_type": "technical", "level": 28, "stats": (12, 12, 17, 10, 13, 15)},
    {"npc_id": 131, "name": "New Jack Carter", "based_on": "New Jack", "territory": "ecw", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "187", "finisher_type": "power", "level": 25, "stats": (13, 8, 4, 16, 15, 7)},
    {"npc_id": 132, "name": "The Dudleys", "based_on": "Dudley Boyz", "territory": "ecw", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "3D", "finisher_type": "power", "level": 30, "stats": (15, 9, 10, 16, 15, 13)},
    {"npc_id": 133, "name": 'Mick "Cactus" Manley', "based_on": "Mick Foley", "territory": "ecw", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Mandible Claw", "finisher_type": "charisma", "level": 36, "stats": (14, 8, 11, 18, 18, 17)},

    # ----------------------------------------------------------
    # WCW (#134-148)
    # ----------------------------------------------------------
    {"npc_id": 134, "name": '"The Scorpion" Steve Borden', "based_on": "Sting", "territory": "wcw", "role": "wrestler", "alignment": "Face", "finisher_name": "Scorpion Deathlock", "finisher_type": "technical", "level": 40, "stats": (15, 12, 14, 18, 15, 16)},
    {"npc_id": 135, "name": "Diamond Dallas Pierce", "based_on": "DDP", "territory": "wcw", "role": "wrestler", "alignment": "Face", "finisher_name": "Diamond Cutter", "finisher_type": "technical", "level": 35, "stats": (13, 10, 12, 17, 14, 15)},
    {"npc_id": 136, "name": "Goldburg", "based_on": "Goldberg", "territory": "wcw", "role": "wrestler", "alignment": "Face", "finisher_name": "Spear", "finisher_type": "power", "level": 38, "stats": (18, 10, 8, 16, 17, 8)},
    {"npc_id": 137, "name": '"Big Poppa" Scotty Steinberg', "based_on": "Scott Steiner", "territory": "wcw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Steinberg Recliner", "finisher_type": "power", "level": 35, "stats": (17, 11, 14, 15, 15, 12)},
    {"npc_id": 138, "name": "Ricky Steinberg", "based_on": "Rick Steiner", "territory": "wcw", "role": "wrestler", "alignment": "Face", "finisher_name": "Steinberg Bulldog", "finisher_type": "power", "level": 30, "stats": (16, 10, 12, 12, 15, 11)},
    {"npc_id": 139, "name": "Booker Washington", "based_on": "Booker T", "territory": "wcw", "role": "wrestler", "alignment": "Face", "finisher_name": "Scissors Kick", "finisher_type": "aerial", "level": 34, "stats": (14, 14, 13, 16, 14, 14)},
    {"npc_id": 140, "name": "Rey Mysterioso", "based_on": "Rey Mysterio", "territory": "wcw", "role": "wrestler", "alignment": "Face", "finisher_name": "619", "finisher_type": "aerial", "level": 34, "stats": (7, 20, 16, 16, 10, 16)},
    {"npc_id": 141, "name": "K-Dogg Konner", "based_on": "Konnan", "territory": "wcw", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Tequila Sunrise", "finisher_type": "technical", "level": 28, "stats": (13, 10, 13, 14, 13, 12)},
    {"npc_id": 142, "name": '"The Lionheart" Chris Jerichord', "based_on": "Chris Jericho", "territory": "wcw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Walls of Jerichord", "finisher_type": "technical", "level": 38, "stats": (13, 14, 16, 18, 13, 17)},
    {"npc_id": 143, "name": '"The Iceman" Dean Malone', "based_on": "Dean Malenko", "territory": "wcw", "role": "wrestler", "alignment": "Face", "finisher_name": "Texas Cloverleaf", "finisher_type": "technical", "level": 30, "stats": (12, 12, 19, 8, 13, 16)},
    {"npc_id": 144, "name": "Perry Sattler", "based_on": "Perry Saturn", "territory": "wcw", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Rings of Sattler", "finisher_type": "technical", "level": 28, "stats": (14, 11, 15, 10, 14, 13)},
    {"npc_id": 145, "name": "Buff Bagman", "based_on": "Buff Bagwell", "territory": "wcw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Blockbuster", "finisher_type": "aerial", "level": 25, "stats": (13, 12, 9, 15, 12, 10)},
    {"npc_id": 146, "name": '"The Colossus" Paul Whitmore', "based_on": "Big Show", "territory": "wcw", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Chokeslam", "finisher_type": "power", "level": 35, "stats": (19, 5, 9, 14, 18, 11)},
    {"npc_id": 147, "name": '"The Cat" Ernest Mills', "based_on": "Ernest Miller", "territory": "wcw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Feliner", "finisher_type": "aerial", "level": 22, "stats": (11, 14, 10, 14, 11, 9)},
    {"npc_id": 148, "name": "Vampiro Diablo", "based_on": "Vampiro", "territory": "wcw", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Nail in the Coffin", "finisher_type": "power", "level": 25, "stats": (13, 11, 10, 14, 13, 11)},

    # ----------------------------------------------------------
    # WWF ATTITUDE ERA (#149-166)
    # ----------------------------------------------------------
    {"npc_id": 149, "name": "Hunter Hearst Hampton", "based_on": "Triple H", "territory": "wwf", "role": "wrestler", "alignment": "Heel", "finisher_name": "Pedigree", "finisher_type": "power", "level": 42, "stats": (16, 11, 14, 17, 16, 17)},
    {"npc_id": 150, "name": '"The Showstopper" Shane Mitchell', "based_on": "Shawn Michaels", "territory": "wwf", "role": "wrestler", "alignment": "Face", "finisher_name": "Sweet Chin Music", "finisher_type": "aerial", "level": 42, "stats": (12, 17, 16, 18, 12, 19)},
    {"npc_id": 151, "name": '"The Inferno" Kane Blackwell', "based_on": "Kane", "territory": "wwf", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Chokeslam", "finisher_type": "power", "level": 38, "stats": (17, 9, 11, 14, 17, 13)},
    {"npc_id": 152, "name": '"Lightning" Sean Walton', "based_on": "X-Pac", "territory": "wwf", "role": "wrestler", "alignment": "Heel", "finisher_name": "X-Factor", "finisher_type": "aerial", "level": 25, "stats": (10, 15, 13, 13, 11, 13)},
    {"npc_id": 153, "name": '"Bad Ass" Billy Gunther', "based_on": "Billy Gunn", "territory": "wwf", "role": "wrestler", "alignment": "Face", "finisher_name": "Fameasser", "finisher_type": "aerial", "level": 25, "stats": (14, 12, 10, 13, 13, 10)},
    {"npc_id": 154, "name": "Road Dog Jesse Jamison", "based_on": "Road Dogg", "territory": "wwf", "role": "wrestler", "alignment": "Face", "finisher_name": "Shake Rattle & Roll", "finisher_type": "charisma", "level": 25, "stats": (12, 10, 9, 16, 12, 12)},
    {"npc_id": 155, "name": "Jeff Rainbow", "based_on": "Jeff Hardy", "territory": "wwf", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Swanton Bomb", "finisher_type": "aerial", "level": 30, "stats": (10, 18, 12, 16, 12, 13)},
    {"npc_id": 156, "name": "Matt Rainbow", "based_on": "Matt Hardy", "territory": "wwf", "role": "wrestler", "alignment": "Face", "finisher_name": "Twist of Fate", "finisher_type": "technical", "level": 28, "stats": (12, 13, 13, 14, 13, 14)},
    {"npc_id": 157, "name": 'Adam "Razor" Copperton', "based_on": "Edge", "territory": "wwf", "role": "wrestler", "alignment": "Heel", "finisher_name": "Spear", "finisher_type": "power", "level": 35, "stats": (14, 14, 14, 16, 13, 16)},
    {"npc_id": 158, "name": "Christian Cabot", "based_on": "Christian", "territory": "wwf", "role": "wrestler", "alignment": "Heel", "finisher_name": "Killswitch", "finisher_type": "technical", "level": 30, "stats": (12, 13, 14, 15, 12, 15)},
    {"npc_id": 159, "name": "Kirk Engleton", "based_on": "Kurt Angle", "territory": "wwf", "role": "wrestler", "alignment": "Heel", "finisher_name": "Ankle Lock", "finisher_type": "technical", "level": 40, "stats": (15, 13, 19, 15, 15, 17)},
    {"npc_id": 160, "name": "Kenny Starling", "based_on": "Ken Shamrock", "territory": "wwf", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Ankle Lock", "finisher_type": "technical", "level": 28, "stats": (15, 12, 16, 10, 15, 11)},
    {"npc_id": 161, "name": "Vince Valentine", "based_on": "Val Venis", "territory": "wwf", "role": "wrestler", "alignment": "Face", "finisher_name": "Money Shot", "finisher_type": "aerial", "level": 22, "stats": (13, 11, 11, 14, 12, 11)},
    {"npc_id": 162, "name": "Marcus Henderson", "based_on": "Mark Henry", "territory": "wwf", "role": "wrestler", "alignment": "Face", "finisher_name": "World's Strongest Slam", "finisher_type": "power", "level": 30, "stats": (20, 5, 8, 12, 18, 9)},
    {"npc_id": 163, "name": "Farooq Simms", "based_on": "Ron Simmons", "territory": "wwf", "role": "wrestler", "alignment": "Face", "finisher_name": "Dominator", "finisher_type": "power", "level": 30, "stats": (16, 9, 11, 13, 16, 12)},
    {"npc_id": 164, "name": "Dante Lowe", "based_on": "D'Lo Brown", "territory": "wwf", "role": "wrestler", "alignment": "Face", "finisher_name": "Lo Down", "finisher_type": "aerial", "level": 22, "stats": (13, 13, 11, 13, 12, 11)},
    {"npc_id": 165, "name": "Titan Andrews", "based_on": "Test", "territory": "wwf", "role": "wrestler", "alignment": "Face", "finisher_name": "Big Boot", "finisher_type": "power", "level": 22, "stats": (15, 10, 9, 11, 14, 9)},
    {"npc_id": 166, "name": '"The Foundation" Dwayne Maivia', "based_on": "The Rock", "territory": "wwf", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Rock Bottom", "finisher_type": "power", "level": 44, "stats": (15, 11, 12, 20, 15, 17)},

    # ----------------------------------------------------------
    # WOMEN'S DIVISION I (#167-181)
    # ----------------------------------------------------------
    {"npc_id": 167, "name": "Trish Stratos", "based_on": "Trish Stratus", "territory": "wwf", "role": "wrestler", "gender": "Female", "alignment": "Face", "finisher_name": "Stratusfaction", "finisher_type": "technical", "level": 30, "stats": (10, 13, 13, 17, 11, 14)},
    {"npc_id": 168, "name": '"The Rebel" Amy Dumas', "based_on": "Lita", "territory": "wwf", "role": "wrestler", "gender": "Female", "alignment": "Anti-Hero", "finisher_name": "Litasault", "finisher_type": "aerial", "level": 28, "stats": (10, 16, 12, 15, 11, 13)},
    {"npc_id": 169, "name": '"The Ninth Wonder" Joan Laurer', "based_on": "Chyna", "territory": "wwf", "role": "wrestler", "gender": "Female", "alignment": "Anti-Hero", "finisher_name": "Pedigree", "finisher_type": "power", "level": 30, "stats": (16, 9, 10, 14, 15, 11)},
    {"npc_id": 170, "name": "The Fabulous Moolah Franklin", "based_on": "Fabulous Moolah", "territory": "wwf", "role": "wrestler", "gender": "Female", "alignment": "Heel", "finisher_name": "Backbreaker", "finisher_type": "power", "level": 30, "stats": (12, 8, 13, 14, 13, 16)},
    {"npc_id": 171, "name": "Wendy Richmond", "based_on": "Wendi Richter", "territory": "wwf", "role": "wrestler", "gender": "Female", "alignment": "Face", "finisher_name": "Suplex", "finisher_type": "power", "level": 25, "stats": (12, 10, 11, 14, 12, 12)},
    {"npc_id": 172, "name": "Alundra Blaze", "based_on": "Madusa", "territory": "wwf", "role": "wrestler", "gender": "Female", "alignment": "Face", "finisher_name": "German Suplex", "finisher_type": "technical", "level": 28, "stats": (11, 12, 14, 13, 12, 14)},
    {"npc_id": 173, "name": "Sable Monroe", "based_on": "Sable", "territory": "wwf", "role": "wrestler", "gender": "Female", "alignment": "Heel", "finisher_name": "Sable Bomb", "finisher_type": "power", "level": 18, "stats": (10, 8, 7, 17, 9, 8)},
    {"npc_id": 174, "name": "Jacqueline Morrow", "based_on": "Jacqueline", "territory": "memphis", "role": "wrestler", "gender": "Female", "alignment": "Face", "finisher_name": "DDT", "finisher_type": "technical", "level": 25, "stats": (12, 11, 12, 13, 13, 13)},
    {"npc_id": 175, "name": "Molly Holloway", "based_on": "Molly Holly", "territory": "wwf", "role": "wrestler", "gender": "Female", "alignment": "Face", "finisher_name": "Molly-Go-Round", "finisher_type": "aerial", "level": 22, "stats": (10, 13, 13, 12, 11, 13)},
    {"npc_id": 176, "name": "Victoria Varon", "based_on": "Victoria", "territory": "wwf", "role": "wrestler", "gender": "Female", "alignment": "Heel", "finisher_name": "Widow's Peak", "finisher_type": "technical", "level": 25, "stats": (13, 11, 12, 13, 13, 12)},
    {"npc_id": 177, "name": "Jazz Carlisle", "based_on": "Jazz", "territory": "ecw", "role": "wrestler", "gender": "Female", "alignment": "Heel", "finisher_name": "STF", "finisher_type": "technical", "level": 25, "stats": (13, 10, 14, 11, 14, 13)},
    {"npc_id": 178, "name": "Bull Nakamura", "based_on": "Bull Nakano", "territory": "japan", "role": "wrestler", "gender": "Female", "alignment": "Heel", "finisher_name": "Guillotine Leg Drop", "finisher_type": "power", "level": 30, "stats": (16, 9, 12, 12, 16, 13)},
    {"npc_id": 179, "name": "Manami Toyoda", "based_on": "Manami Toyota", "territory": "japan", "role": "wrestler", "gender": "Female", "alignment": "Face", "finisher_name": "Japanese Ocean Cyclone Suplex", "finisher_type": "technical", "level": 32, "stats": (10, 16, 18, 14, 12, 17)},
    {"npc_id": 180, "name": "Aja Kongo", "based_on": "Aja Kong", "territory": "japan", "role": "wrestler", "gender": "Female", "alignment": "Heel", "finisher_name": "Uraken", "finisher_type": "power", "level": 30, "stats": (17, 8, 12, 13, 16, 13)},
    {"npc_id": 181, "name": "Sensuous Sherry Valentine", "based_on": "Sherri Martel", "territory": "wwf", "role": "wrestler", "gender": "Female", "alignment": "Heel", "finisher_name": "Loaded Purse Shot", "finisher_type": "charisma", "level": 25, "stats": (10, 10, 10, 16, 11, 14)},

    # ----------------------------------------------------------
    # TAG TEAMS I (#182-193)
    # ----------------------------------------------------------
    {"npc_id": 182, "name": "Bobby Eaton Jr.", "based_on": "Bobby Eaton", "territory": "midsouth", "role": "wrestler", "alignment": "Heel", "finisher_name": "Rocket Launcher", "finisher_type": "aerial", "level": 30, "stats": (12, 14, 14, 12, 13, 15)},
    {"npc_id": 183, "name": "Stan Lake", "based_on": "Stan Lane", "territory": "midsouth", "role": "wrestler", "alignment": "Heel", "finisher_name": "Rocket Launcher", "finisher_type": "aerial", "level": 28, "stats": (11, 14, 13, 13, 12, 14)},
    {"npc_id": 184, "name": "Ricky Gibson", "based_on": "Ricky Morton", "territory": "midsouth", "role": "wrestler", "alignment": "Face", "finisher_name": "Double Dropkick", "finisher_type": "aerial", "level": 28, "stats": (10, 15, 13, 16, 11, 15)},
    {"npc_id": 185, "name": "Robert Fulton", "based_on": "Robert Gibson", "territory": "midsouth", "role": "wrestler", "alignment": "Face", "finisher_name": "Double Dropkick", "finisher_type": "aerial", "level": 26, "stats": (11, 14, 12, 13, 12, 13)},
    {"npc_id": 186, "name": "Brian Knox", "based_on": "Brian Knobbs", "territory": "wwf", "role": "wrestler", "alignment": "Heel", "finisher_name": "Pit Stop", "finisher_type": "power", "level": 22, "stats": (14, 7, 7, 12, 14, 8)},
    {"npc_id": 187, "name": "Jerry Saggs", "based_on": "Jerry Sags", "territory": "wwf", "role": "wrestler", "alignment": "Heel", "finisher_name": "Pit Stop", "finisher_type": "power", "level": 22, "stats": (14, 8, 7, 11, 14, 8)},
    {"npc_id": 188, "name": 'Jim "The Anvil" Niedhardt', "based_on": "Jim Neidhart", "territory": "stampede", "role": "wrestler", "alignment": "Heel", "finisher_name": "Hart Attack", "finisher_type": "power", "level": 28, "stats": (16, 7, 9, 11, 16, 10)},
    {"npc_id": 189, "name": "Demolition Axe", "based_on": "Demolition Ax", "territory": "wwf", "role": "wrestler", "alignment": "Heel", "finisher_name": "Decapitation", "finisher_type": "power", "level": 26, "stats": (16, 6, 8, 12, 16, 9)},
    {"npc_id": 190, "name": "Art Alderson (Tag)", "based_on": "Arn Anderson (Enforcers)", "territory": "midatlantic", "role": "wrestler", "alignment": "Heel", "finisher_name": "Spike Piledriver", "finisher_type": "power", "level": 35, "stats": (15, 8, 16, 13, 16, 18)},
    {"npc_id": 191, "name": "Larry Zablonski (Tag)", "based_on": "Larry Zbyszko (Enforcers)", "territory": "midatlantic", "role": "wrestler", "alignment": "Heel", "finisher_name": "Spike Piledriver", "finisher_type": "power", "level": 30, "stats": (12, 9, 15, 13, 13, 15)},
    {"npc_id": 192, "name": "Crush", "based_on": "Demolition Crush", "territory": "wwf", "role": "wrestler", "alignment": "Heel", "finisher_name": "Decapitation Elbow", "finisher_type": "power", "level": 24, "stats": (16, 8, 7, 11, 15, 8)},
    {"npc_id": 193, "name": "Demolition Smash", "based_on": "Demolition Smash", "territory": "wwf", "role": "wrestler", "alignment": "Heel", "finisher_name": "Decapitation Elbow", "finisher_type": "power", "level": 24, "stats": (16, 6, 8, 12, 15, 9)},

    # ----------------------------------------------------------
    # INTERNATIONAL I (#194-207)
    # ----------------------------------------------------------
    {"npc_id": 194, "name": "Mitsuhiro Misawa", "based_on": "Mitsuharu Misawa", "territory": "japan", "role": "wrestler", "alignment": "Face", "finisher_name": "Emerald Flowsion", "finisher_type": "power", "level": 40, "stats": (14, 14, 18, 14, 16, 19)},
    {"npc_id": 195, "name": "Kenta Kobashi-do", "based_on": "Kenta Kobashi", "territory": "japan", "role": "wrestler", "alignment": "Face", "finisher_name": "Burning Lariat", "finisher_type": "power", "level": 40, "stats": (17, 11, 16, 14, 18, 18)},
    {"npc_id": 196, "name": "Akira Taue", "based_on": "Akira Taue", "territory": "japan", "role": "wrestler", "alignment": "Heel", "finisher_name": "Dynamic Bomb", "finisher_type": "power", "level": 35, "stats": (16, 8, 14, 11, 16, 15)},
    {"npc_id": 197, "name": "Toshiaki Kawada", "based_on": "Toshiaki Kawada", "territory": "japan", "role": "wrestler", "alignment": "Heel", "finisher_name": "Ganso Bomb", "finisher_type": "power", "level": 38, "stats": (16, 10, 17, 12, 17, 18)},
    {"npc_id": 198, "name": "Hayabusa Takeda", "based_on": "Hayabusa", "territory": "japan", "role": "wrestler", "alignment": "Face", "finisher_name": "Phoenix Splash", "finisher_type": "aerial", "level": 30, "stats": (10, 19, 14, 14, 11, 14)},
    {"npc_id": 199, "name": "El Santo Dorado", "based_on": "El Santo", "territory": "japan", "role": "wrestler", "alignment": "Face", "finisher_name": "La de a Caballo", "finisher_type": "technical", "level": 35, "stats": (13, 14, 16, 18, 14, 16)},
    {"npc_id": 200, "name": "El Hijo del Diablo", "based_on": "Mil Mascaras", "territory": "japan", "role": "wrestler", "alignment": "Face", "finisher_name": "Plancha", "finisher_type": "aerial", "level": 32, "stats": (13, 16, 14, 15, 13, 14)},
    {"npc_id": 201, "name": "Psicosis Loco", "based_on": "Psicosis", "territory": "wcw", "role": "wrestler", "alignment": "Heel", "finisher_name": "Guillotine Leg Drop", "finisher_type": "aerial", "level": 25, "stats": (9, 17, 12, 11, 10, 12)},
    {"npc_id": 202, "name": "Juventud Guerrera Jr.", "based_on": "Juventud Guerrera", "territory": "wcw", "role": "wrestler", "alignment": "Face", "finisher_name": "Juvi Driver", "finisher_type": "aerial", "level": 25, "stats": (9, 18, 13, 13, 9, 13)},
    {"npc_id": 203, "name": "La Parka Esqueleto", "based_on": "La Parka", "territory": "wcw", "role": "wrestler", "alignment": "Anti-Hero", "finisher_name": "Corkscrew Plancha", "finisher_type": "aerial", "level": 25, "stats": (11, 15, 11, 16, 12, 11)},
    {"npc_id": 204, "name": "Lord William Regalton", "based_on": "William Regal", "territory": "uk", "role": "wrestler", "alignment": "Heel", "finisher_name": "Power of the Punch", "finisher_type": "technical", "level": 32, "stats": (14, 9, 17, 15, 14, 16)},
    {"npc_id": 205, "name": "Nigel McGuinn", "based_on": "Nigel McGuinness", "territory": "uk", "role": "wrestler", "alignment": "Face", "finisher_name": "Tower of London", "finisher_type": "power", "level": 28, "stats": (13, 12, 16, 13, 13, 15)},
    {"npc_id": 206, "name": "Davey Richardson", "based_on": "Davey Boy Smith Jr.", "territory": "stampede", "role": "wrestler", "alignment": "Face", "finisher_name": "Running Powerslam", "finisher_type": "power", "level": 22, "stats": (15, 11, 11, 11, 14, 11)},
    {"npc_id": 207, "name": "Tiger Mask Hayashi", "based_on": "Tiger Mask", "territory": "japan", "role": "wrestler", "alignment": "Face", "finisher_name": "Tiger Suplex", "finisher_type": "technical", "level": 32, "stats": (11, 17, 17, 14, 11, 16)},

    # ----------------------------------------------------------
    # TRAINING SCHOOL HEAD TRAINERS (#208-211)
    # ----------------------------------------------------------
    {"npc_id": 208, "name": "Viktor Kovalenko", "based_on": "Killer Kowalski", "territory": "slaughterhouse", "role": "trainer", "alignment": "Heel", "finisher_name": "Kowalski Claw", "finisher_type": "power", "level": 40, "stats": (17, 7, 15, 13, 18, 18)},
    {"npc_id": 209, "name": "Larry Sharpton", "based_on": "Larry Sharpe", "territory": "beastworks", "role": "trainer", "alignment": "Face", "finisher_name": "Boston Crab", "finisher_type": "technical", "level": 35, "stats": (15, 8, 14, 12, 15, 16)},
    {"npc_id": 210, "name": "Dory Funk Sr.", "based_on": "Dory Funk Jr.", "territory": "conservatory", "role": "trainer", "alignment": "Face", "finisher_name": "Spinning Toe Hold", "finisher_type": "technical", "level": 38, "stats": (13, 9, 19, 14, 15, 19)},
    {"npc_id": 211, "name": "Boris Malenko", "based_on": "Boris Malenko", "territory": "dungeon", "role": "trainer", "alignment": "Heel", "finisher_name": "Armbar", "finisher_type": "technical", "level": 36, "stats": (12, 8, 20, 10, 14, 18)},
]

# Import extended roster (#212-380)
from world.npc_data_extended import NPC_WRESTLERS_EXTENDED
NPC_WRESTLERS.extend(NPC_WRESTLERS_EXTENDED)


# ============================================================
# NPC MANAGERS (~16)
# ============================================================

NPC_MANAGERS = [
    {"npc_id": 1001, "name": "Bobby Haynes", "based_on": "Bobby Heenan", "territory": "awa", "alignment": "Heel", "style": "cowardly genius", "specialty": "CHA boost + interference", "cha": 18, "psy": 17, "retainer_cost": 150, "cut_percent": 25},
    {"npc_id": 1002, "name": "Jimmy Montague", "based_on": "Jimmy Hart", "territory": "memphis", "alignment": "Heel", "style": "fast-talking megaphone", "specialty": "Heat generation", "cha": 16, "psy": 14, "retainer_cost": 100, "cut_percent": 20},
    {"npc_id": 1003, "name": '"Captain" Lou Albanese', "based_on": "Captain Lou Albano", "territory": "wwf", "alignment": "Heel", "style": "wild and unpredictable", "specialty": "Interference", "cha": 15, "psy": 13, "retainer_cost": 120, "cut_percent": 20},
    {"npc_id": 1004, "name": "Paul Barrington", "based_on": "Paul Bearer", "territory": "wwf", "alignment": "Heel", "style": "supernatural", "specialty": "PSY boost + mind games", "cha": 14, "psy": 16, "retainer_cost": 130, "cut_percent": 20},
    {"npc_id": 1005, "name": "Miss Elizabeth Salvatore", "based_on": "Miss Elizabeth", "territory": "wwf", "gender": "Female", "alignment": "Face", "style": "elegant distraction", "specialty": "Distraction specialist", "cha": 17, "psy": 12, "retainer_cost": 120, "cut_percent": 15},
    {"npc_id": 1006, "name": "Freddy Blaze", "based_on": "Freddie Blassie", "territory": "wwf", "alignment": "Heel", "style": "cane-wielding old school", "specialty": "Weapon interference", "cha": 16, "psy": 14, "retainer_cost": 110, "cut_percent": 20},
    {"npc_id": 1007, "name": "Jim Corwin", "based_on": "Jim Cornette", "territory": "ovw", "alignment": "Heel", "style": "tennis racket screamer", "specialty": "CHA+PSY boost, booking influence", "cha": 19, "psy": 20, "retainer_cost": 200, "cut_percent": 25},
    {"npc_id": 1008, "name": "Percival Ellison", "based_on": "Paul Ellering", "territory": "midatlantic", "alignment": "Face", "style": "intellectual strategist", "specialty": "PSY boost + match planning", "cha": 13, "psy": 18, "retainer_cost": 140, "cut_percent": 20},
    {"npc_id": 1009, "name": "Sonny King", "based_on": "Skandor Akbar", "territory": "midsouth", "alignment": "Heel", "style": "mastermind", "specialty": "Heat generation + stable building", "cha": 15, "psy": 16, "retainer_cost": 130, "cut_percent": 20},
    {"npc_id": 1010, "name": "Mr. Fuji Tanaka", "based_on": "Mr. Fuji", "territory": "wwf", "alignment": "Heel", "style": "devious", "specialty": "Salt to eyes interference", "cha": 13, "psy": 15, "retainer_cost": 100, "cut_percent": 20},
    {"npc_id": 1011, "name": 'Phil "The Advocate" Eastman', "based_on": "Paul Heyman", "territory": "ecw", "alignment": "Anti-Hero", "style": "master strategist", "specialty": "Best CHA in game, works any alignment", "cha": 20, "psy": 19, "retainer_cost": 300, "cut_percent": 25},
    {"npc_id": 1012, "name": "Sensuous Sherry Valentine (Mgr)", "based_on": "Sherri Martel", "territory": "wwf", "gender": "Female", "alignment": "Heel", "style": "physical interference", "specialty": "Also wrestles, CHA boost", "cha": 16, "psy": 13, "retainer_cost": 110, "cut_percent": 20},
    {"npc_id": 1013, "name": "Gary Sharp", "based_on": "Gary Hart", "territory": "wccw", "alignment": "Heel", "style": "mastermind booker", "specialty": "Booking influence + PSY boost", "cha": 15, "psy": 17, "retainer_cost": 140, "cut_percent": 20},
    {"npc_id": 1014, "name": "James Dixon", "based_on": "J.J. Dillon", "territory": "midatlantic", "alignment": "Heel", "style": "corporate fixer", "specialty": "Negotiation + booking influence", "cha": 14, "psy": 16, "retainer_cost": 130, "cut_percent": 20},
    {"npc_id": 1015, "name": "Sunshine Summers", "based_on": "Sunny", "territory": "wwf", "gender": "Female", "alignment": "Face", "style": "distraction specialist", "specialty": "CHA boost + merch bonus", "cha": 18, "psy": 11, "retainer_cost": 120, "cut_percent": 15},
    {"npc_id": 1016, "name": "Terri Goldwyn", "based_on": "Terri Runnels", "territory": "wwf", "gender": "Female", "alignment": "Heel", "style": "plays both sides", "specialty": "Distraction + double-cross potential", "cha": 15, "psy": 13, "retainer_cost": 100, "cut_percent": 20},
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_npc_by_id(npc_id):
    """Look up an NPC wrestler by ID."""
    for npc in NPC_WRESTLERS:
        if npc["npc_id"] == npc_id:
            return npc
    return None


def get_npcs_for_territory(territory_key):
    """Get all NPCs assigned to a territory."""
    return [n for n in NPC_WRESTLERS if n["territory"] == territory_key]


def get_manager_by_id(npc_id):
    """Look up a manager by ID."""
    for mgr in NPC_MANAGERS:
        if mgr["npc_id"] == npc_id:
            return mgr
    return None


def get_managers_for_territory(territory_key):
    """Get all managers assigned to a territory."""
    return [m for m in NPC_MANAGERS if m["territory"] == territory_key]
