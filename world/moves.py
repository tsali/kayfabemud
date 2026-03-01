"""
Kayfabe: Protect the Business — Wrestling move database.

Each move has:
    key: unique identifier
    name: display name
    type: power / technical / aerial / charisma
    stat: primary stat used (str/agi/tec/cha/tou/psy)
    difficulty: 1-10 (higher = harder to execute, more impressive)
    damage: base damage value 1-10
    phase: which match phases this move works best in (opening/heat/hope/comeback/finish)
    desc: flavor text when executed
    fail_desc: flavor text on botch
"""

MOVES = {
    # === POWER MOVES (STR) ===
    "bodyslam": {
        "name": "Body Slam",
        "type": "power",
        "stat": "str",
        "difficulty": 2,
        "damage": 3,
        "phase": ["opening", "heat"],
        "desc": "{attacker} hoists {defender} up and slams them to the mat!",
        "fail_desc": "{attacker} tries for a body slam but can't get {defender} up!",
    },
    "suplex": {
        "name": "Vertical Suplex",
        "type": "power",
        "stat": "str",
        "difficulty": 3,
        "damage": 4,
        "phase": ["opening", "heat", "comeback"],
        "desc": "{attacker} snaps {defender} over with a textbook vertical suplex!",
        "fail_desc": "{attacker} goes for the suplex but {defender} blocks it!",
    },
    "powerbomb": {
        "name": "Powerbomb",
        "type": "power",
        "stat": "str",
        "difficulty": 6,
        "damage": 7,
        "phase": ["heat", "comeback", "finish"],
        "desc": "{attacker} lifts {defender} high and DRIVES them down with a devastating powerbomb!",
        "fail_desc": "{attacker} tries the powerbomb but {defender} reverses with a back body drop!",
    },
    "clothesline": {
        "name": "Clothesline",
        "type": "power",
        "stat": "str",
        "difficulty": 2,
        "damage": 3,
        "phase": ["opening", "heat", "comeback"],
        "desc": "{attacker} nearly takes {defender}'s head off with a running clothesline!",
        "fail_desc": "{defender} ducks the clothesline and {attacker} hits nothing but air!",
    },
    "spinebuster": {
        "name": "Spinebuster",
        "type": "power",
        "stat": "str",
        "difficulty": 5,
        "damage": 6,
        "phase": ["heat", "comeback"],
        "desc": "{attacker} catches {defender} mid-run and plants them with a spinebuster!",
        "fail_desc": "{attacker} goes for the spinebuster but {defender} slips out the back!",
    },
    "bearhug": {
        "name": "Bear Hug",
        "type": "power",
        "stat": "str",
        "difficulty": 4,
        "damage": 4,
        "phase": ["heat"],
        "desc": "{attacker} locks in a crushing bear hug! {defender} is fading!",
        "fail_desc": "{defender} elbows free of the bear hug attempt!",
    },
    "gorilla_press": {
        "name": "Gorilla Press Slam",
        "type": "power",
        "stat": "str",
        "difficulty": 7,
        "damage": 7,
        "phase": ["comeback", "finish"],
        "desc": "{attacker} presses {defender} overhead and THROWS them to the mat!",
        "fail_desc": "{defender} squirms free and lands on their feet!",
    },
    "piledriver": {
        "name": "Piledriver",
        "type": "power",
        "stat": "str",
        "difficulty": 7,
        "damage": 8,
        "phase": ["heat", "finish"],
        "desc": "{attacker} spikes {defender} on their head with a PILEDRIVER! The crowd gasps!",
        "fail_desc": "{defender} backdrops out of the piledriver attempt!",
    },

    # === TECHNICAL MOVES (TEC) ===
    "armbar": {
        "name": "Armbar",
        "type": "technical",
        "stat": "tec",
        "difficulty": 3,
        "damage": 3,
        "phase": ["opening", "heat"],
        "desc": "{attacker} wrenches the arm into a tight armbar! {defender} grimaces in pain!",
        "fail_desc": "{defender} rolls through and escapes the armbar!",
    },
    "headlock": {
        "name": "Side Headlock",
        "type": "technical",
        "stat": "tec",
        "difficulty": 1,
        "damage": 2,
        "phase": ["opening"],
        "desc": "{attacker} cinches in a side headlock, grinding {defender} down.",
        "fail_desc": "{defender} shoots {attacker} off into the ropes!",
    },
    "german_suplex": {
        "name": "German Suplex",
        "type": "technical",
        "stat": "tec",
        "difficulty": 5,
        "damage": 6,
        "phase": ["heat", "comeback"],
        "desc": "{attacker} launches {defender} with a bridging German suplex! ONE! TWO--!",
        "fail_desc": "{defender} grabs the ropes to block the German suplex!",
    },
    "figure_four": {
        "name": "Figure-Four Leglock",
        "type": "technical",
        "stat": "tec",
        "difficulty": 6,
        "damage": 5,
        "phase": ["heat", "finish"],
        "desc": "{attacker} grapevines the legs -- FIGURE FOUR! {defender} is screaming!",
        "fail_desc": "{defender} kicks {attacker} away before the Figure Four is locked in!",
    },
    "sharpshooter": {
        "name": "Sharpshooter",
        "type": "technical",
        "stat": "tec",
        "difficulty": 7,
        "damage": 6,
        "phase": ["heat", "finish"],
        "desc": "{attacker} turns {defender} over into the SHARPSHOOTER! The crowd is on their feet!",
        "fail_desc": "{defender} fights the turn and kicks free!",
    },
    "dropkick": {
        "name": "Dropkick",
        "type": "technical",
        "stat": "tec",
        "difficulty": 3,
        "damage": 3,
        "phase": ["opening", "comeback"],
        "desc": "{attacker} connects with a picture-perfect dropkick!",
        "fail_desc": "{attacker} misses the dropkick and crashes to the mat!",
    },
    "backbreaker": {
        "name": "Backbreaker",
        "type": "technical",
        "stat": "tec",
        "difficulty": 4,
        "damage": 5,
        "phase": ["heat", "comeback"],
        "desc": "{attacker} drives {defender} across their knee with a backbreaker!",
        "fail_desc": "{defender} elbows free before the backbreaker connects!",
    },
    "sleeper": {
        "name": "Sleeper Hold",
        "type": "technical",
        "stat": "tec",
        "difficulty": 5,
        "damage": 4,
        "phase": ["heat", "finish"],
        "desc": "{attacker} sinks in the sleeper hold! {defender}'s arm drops once... twice...",
        "fail_desc": "{defender} fights out of the sleeper with elbows to the gut!",
    },

    # === AERIAL MOVES (AGI) ===
    "crossbody": {
        "name": "Crossbody",
        "type": "aerial",
        "stat": "agi",
        "difficulty": 3,
        "damage": 4,
        "phase": ["opening", "comeback"],
        "desc": "{attacker} flies off the ropes with a crossbody! Both wrestlers are down!",
        "fail_desc": "{defender} sidesteps and {attacker} crashes and burns!",
    },
    "moonsault": {
        "name": "Moonsault",
        "type": "aerial",
        "stat": "agi",
        "difficulty": 7,
        "damage": 7,
        "phase": ["comeback", "finish"],
        "desc": "{attacker} goes to the top... MOONSAULT! What impact!",
        "fail_desc": "{attacker} goes up top but {defender} rolls away! Nobody home!",
    },
    "hurricanrana": {
        "name": "Hurricanrana",
        "type": "aerial",
        "stat": "agi",
        "difficulty": 5,
        "damage": 5,
        "phase": ["opening", "comeback"],
        "desc": "{attacker} snaps off a hurricanrana! {defender} is sent flying!",
        "fail_desc": "{defender} catches {attacker} mid-air and powerbombs them!",
    },
    "diving_elbow": {
        "name": "Diving Elbow Drop",
        "type": "aerial",
        "stat": "agi",
        "difficulty": 6,
        "damage": 6,
        "phase": ["heat", "finish"],
        "desc": "{attacker} climbs to the top rope... DIVING ELBOW! Right to the heart!",
        "fail_desc": "{defender} moves! {attacker}'s elbow hits nothing but canvas!",
    },
    "plancha": {
        "name": "Suicide Dive",
        "type": "aerial",
        "stat": "agi",
        "difficulty": 6,
        "damage": 5,
        "phase": ["comeback"],
        "desc": "{attacker} launches through the ropes with a suicide dive to the outside! Both wrestlers are down!",
        "fail_desc": "{attacker} dives but {defender} catches them with a forearm!",
    },
    "frog_splash": {
        "name": "Frog Splash",
        "type": "aerial",
        "stat": "agi",
        "difficulty": 7,
        "damage": 7,
        "phase": ["comeback", "finish"],
        "desc": "{attacker} leaps from the top -- FROG SPLASH! Cover! ONE! TWO--!",
        "fail_desc": "{defender} gets the knees up on the frog splash!",
    },
    "springboard": {
        "name": "Springboard Clothesline",
        "type": "aerial",
        "stat": "agi",
        "difficulty": 5,
        "damage": 5,
        "phase": ["opening", "comeback"],
        "desc": "{attacker} springboards off the middle rope with a flying clothesline!",
        "fail_desc": "{attacker} slips on the springboard and crashes awkwardly!",
    },

    # === CHARISMA MOVES (CHA) ===
    "taunt": {
        "name": "Taunt",
        "type": "charisma",
        "stat": "cha",
        "difficulty": 1,
        "damage": 0,
        "phase": ["opening", "heat", "comeback"],
        "desc": "{attacker} taunts {defender}, playing to the crowd! The fans are eating it up!",
        "fail_desc": "{attacker} taunts but {defender} attacks from behind! Bad timing!",
    },
    "signature_pose": {
        "name": "Signature Pose",
        "type": "charisma",
        "stat": "cha",
        "difficulty": 2,
        "damage": 0,
        "phase": ["opening", "comeback"],
        "desc": "{attacker} hits their signature pose! The crowd ERUPTS!",
        "fail_desc": "{attacker} poses but the crowd sits on their hands. Crickets.",
    },
    "low_blow": {
        "name": "Low Blow",
        "type": "charisma",
        "stat": "cha",
        "difficulty": 3,
        "damage": 4,
        "phase": ["heat", "finish"],
        "desc": "{attacker} with a low blow behind the referee's back! Dirty tactics!",
        "fail_desc": "The referee catches {attacker} going for the low blow! Warning issued!",
        "heel_only": True,
    },
    "foreign_object": {
        "name": "Foreign Object",
        "type": "charisma",
        "stat": "cha",
        "difficulty": 4,
        "damage": 5,
        "phase": ["heat", "finish"],
        "desc": "{attacker} pulls something out of their trunks -- WHAM! The ref didn't see it!",
        "fail_desc": "The referee spots the foreign object and confiscates it!",
        "heel_only": True,
    },
    "eye_rake": {
        "name": "Eye Rake",
        "type": "charisma",
        "stat": "cha",
        "difficulty": 2,
        "damage": 2,
        "phase": ["opening", "heat"],
        "desc": "{attacker} rakes the eyes! Classic heel tactics!",
        "fail_desc": "{defender} blocks the eye rake and fires back with rights!",
        "heel_only": True,
    },
    "rally_crowd": {
        "name": "Rally the Crowd",
        "type": "charisma",
        "stat": "cha",
        "difficulty": 3,
        "damage": 0,
        "phase": ["comeback"],
        "desc": "{attacker} is feeding off the crowd! They're hulking up! The fans are going wild!",
        "fail_desc": "{attacker} tries to rally the crowd but they're not buying it tonight.",
        "face_only": True,
    },
    "strut": {
        "name": "Heel Strut",
        "type": "charisma",
        "stat": "cha",
        "difficulty": 2,
        "damage": 0,
        "phase": ["heat"],
        "desc": "{attacker} struts around the ring, mocking {defender} and drawing massive heat!",
        "fail_desc": "{defender} kips up and {attacker}'s strut turns into a retreat!",
        "heel_only": True,
    },

    # === PSYCHOLOGY MOVES (PSY) ===
    "counter": {
        "name": "Counter",
        "type": "technical",
        "stat": "psy",
        "difficulty": 5,
        "damage": 3,
        "phase": ["opening", "heat", "comeback"],
        "desc": "{attacker} reads {defender} like a book and counters into a devastating reversal!",
        "fail_desc": "{attacker} goes for the counter but gets caught!",
    },
    "psychology_sell": {
        "name": "Expert Sell",
        "type": "charisma",
        "stat": "psy",
        "difficulty": 4,
        "damage": 0,
        "phase": ["heat", "hope"],
        "desc": "{attacker} sells the damage beautifully -- the crowd believes every second of it!",
        "fail_desc": "{attacker} oversells and it looks fake. The crowd murmurs.",
    },
    "false_finish": {
        "name": "False Finish",
        "type": "charisma",
        "stat": "psy",
        "difficulty": 7,
        "damage": 0,
        "phase": ["finish"],
        "desc": "NEAR FALL! {defender} kicks out at the LAST SECOND! The crowd can't believe it!",
        "fail_desc": "The near fall doesn't get the reaction -- the crowd saw it coming.",
    },

    # === TOUGHNESS MOVES (TOU) ===
    "no_sell": {
        "name": "No-Sell",
        "type": "power",
        "stat": "tou",
        "difficulty": 5,
        "damage": 0,
        "phase": ["comeback"],
        "desc": "{attacker} takes the hit and DOESN'T GO DOWN! They're shaking it off! The crowd is stunned!",
        "fail_desc": "{attacker} tries to no-sell but crumples anyway. That one hurt.",
    },
    "chop": {
        "name": "Knife-Edge Chop",
        "type": "power",
        "stat": "tou",
        "difficulty": 2,
        "damage": 3,
        "phase": ["opening", "heat", "comeback"],
        "desc": "WOOO! {attacker} lights up {defender}'s chest with a knife-edge chop!",
        "fail_desc": "{defender} catches {attacker}'s hand and wrenches the arm!",
    },
    "headbutt": {
        "name": "Headbutt",
        "type": "power",
        "stat": "tou",
        "difficulty": 3,
        "damage": 4,
        "phase": ["heat", "comeback"],
        "desc": "{attacker} drives their skull into {defender}'s forehead! Both wrestlers stagger!",
        "fail_desc": "{attacker} goes for the headbutt but {defender} moves and {attacker} hits the turnbuckle!",
    },
}


def get_moves_for_phase(phase):
    """Return list of move keys valid for a given match phase."""
    return [k for k, v in MOVES.items() if phase in v["phase"]]


def get_moves_for_type(move_type):
    """Return list of move keys of a given type."""
    return [k for k, v in MOVES.items() if v["type"] == move_type]


def get_moves_for_stat(stat):
    """Return list of move keys that use a given stat."""
    return [k for k, v in MOVES.items() if v["stat"] == stat]


def get_move(key):
    """Return a move dict by key, or None."""
    return MOVES.get(key)
