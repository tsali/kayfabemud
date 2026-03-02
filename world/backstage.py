"""
Kayfabe: Protect the Business — Backstage Segments.

Triggered in LockerRoom/BarRoom on entry (~20% chance).
Types: rival confrontation, interview, prank war, contract offer, fan encounter.
Narrative text + 2-3 choices via EvMenu-style input.
"""

import random


BACKSTAGE_SEGMENTS = [
    # --- Rival Confrontation ---
    {
        "type": "rival_confrontation",
        "trigger_rooms": ["locker", "bar"],
        "title": "BACKSTAGE CONFRONTATION",
        "setup": (
            "You turn a corner and bump right into {rival}.\n"
            "They get in your face. \"You think you're hot stuff around here?\n"
            "I've been working this territory since before you laced your boots.\""
        ),
        "choices": [
            {
                "desc": "Stand your ground",
                "msg": (
                    "You stare {rival} dead in the eyes. \"I earned my spot. "
                    "Step up or shut up.\"\n"
                    "The boys in the back nod approvingly. Respect gained."
                ),
                "kayfabe": 3, "trust": 2, "money": 0,
            },
            {
                "desc": "Shove them",
                "msg": (
                    "You shove {rival} into the wall! Before it escalates, "
                    "some of the boys pull you apart.\n"
                    "The promoter hears about it. Heat with the office."
                ),
                "kayfabe": 5, "trust": -3, "money": 0,
            },
            {
                "desc": "Walk away",
                "msg": (
                    "You shake your head and walk away. {rival} laughs behind you.\n"
                    "\"That's what I thought!\" The locker room watches silently."
                ),
                "kayfabe": -2, "trust": 0, "money": 0,
            },
        ],
    },
    # --- Interview ---
    {
        "type": "interview",
        "trigger_rooms": ["locker", "bar"],
        "title": "BACKSTAGE INTERVIEW",
        "setup": (
            "A local reporter with a tape recorder corners you.\n"
            "\"Hey, can I get a quick word about your match tonight?\""
        ),
        "choices": [
            {
                "desc": "Stay in character",
                "msg": (
                    "You cut a promo right there in the hallway. The reporter "
                    "eats it up.\nGreat kayfabe. The fans will love this clip."
                ),
                "kayfabe": 4, "trust": 1, "money": 0,
            },
            {
                "desc": "Give a shoot interview",
                "msg": (
                    "You break kayfabe and talk about the business. Real talk.\n"
                    "The reporter is thrilled. The promoter... less so."
                ),
                "kayfabe": -5, "trust": -2, "money": 25,
            },
            {
                "desc": "Decline politely",
                "msg": (
                    "\"Not tonight, brother.\" You walk away.\n"
                    "No harm done. The reporter finds someone else."
                ),
                "kayfabe": 0, "trust": 0, "money": 0,
            },
        ],
    },
    # --- Prank War ---
    {
        "type": "prank_war",
        "trigger_rooms": ["locker"],
        "title": "LOCKER ROOM PRANK",
        "setup": (
            "You open your gear bag and find it filled with baby powder.\n"
            "The veterans are watching from across the room, trying not to laugh.\n"
            "This is a rib. How you handle it determines your standing."
        ),
        "choices": [
            {
                "desc": "Laugh it off",
                "msg": (
                    "You dust yourself off and laugh. \"Good one, boys.\"\n"
                    "The veterans nod. You passed the test. You're one of them now."
                ),
                "kayfabe": 1, "trust": 3, "money": 0,
            },
            {
                "desc": "Get revenge",
                "msg": (
                    "You find the ringleader's boots and fill them with hot sauce.\n"
                    "When they find out, the whole locker room is howling.\n"
                    "You've earned your spot in the prank pecking order."
                ),
                "kayfabe": 2, "trust": 1, "money": 0,
            },
            {
                "desc": "Lose your temper",
                "msg": (
                    "You flip out and start yelling. The room goes silent.\n"
                    "\"He can't take a rib.\" That label sticks for weeks."
                ),
                "kayfabe": -3, "trust": -4, "money": 0,
            },
        ],
    },
    # --- Contract Offer ---
    {
        "type": "contract_offer",
        "trigger_rooms": ["locker", "bar"],
        "title": "SURPRISE CONTRACT OFFER",
        "setup": (
            "A man in a suit approaches you. \"I represent a promoter who's\n"
            "been watching your work. They're interested in bringing you in.\n"
            "But there's a catch — you'd have to leave your current territory.\""
        ),
        "choices": [
            {
                "desc": "Take the meeting",
                "msg": (
                    "You sit down and hear them out. The money is decent.\n"
                    "Whether you sign or not, it's nice to be wanted.\n"
                    "Word gets back to your current promoter. They take notice."
                ),
                "kayfabe": 0, "trust": 3, "money": 50,
            },
            {
                "desc": "Decline — loyal to your territory",
                "msg": (
                    "\"I appreciate it, but I'm building something here.\"\n"
                    "The suit nods and leaves. Your promoter hears about your loyalty."
                ),
                "kayfabe": 2, "trust": 5, "money": 0,
            },
        ],
    },
    # --- Fan Backstage ---
    {
        "type": "fan_backstage",
        "trigger_rooms": ["locker", "bar"],
        "title": "FAN SNUCK BACKSTAGE",
        "setup": (
            "A wide-eyed fan has somehow gotten backstage. They spot you\n"
            "and freeze. \"Oh my God, it's really you!\""
        ),
        "choices": [
            {
                "desc": "Stay in character",
                "msg": (
                    "You stay in character and give the fan the full experience.\n"
                    "They'll tell this story for the rest of their life.\n"
                    "Kayfabe: protected. The business: alive."
                ),
                "kayfabe": 5, "trust": 1, "money": 0,
            },
            {
                "desc": "Be friendly out of character",
                "msg": (
                    "You break character and chat with them. Sign an autograph.\n"
                    "They're thrilled... but they also saw the curtain pulled back."
                ),
                "kayfabe": -3, "trust": 0, "money": 0,
            },
            {
                "desc": "Get security",
                "msg": (
                    "\"Hey, we got a mark back here!\" Security escorts them out.\n"
                    "Professional. No kayfabe broken. The promoter approves."
                ),
                "kayfabe": 1, "trust": 2, "money": 0,
            },
        ],
    },
    # --- Veteran Advice ---
    {
        "type": "veteran_advice",
        "trigger_rooms": ["locker"],
        "title": "VETERAN'S WISDOM",
        "setup": (
            "An old-timer pulls you aside. \"Kid, let me give you some advice.\n"
            "I've been in this business thirty years. You've got talent,\n"
            "but talent ain't enough.\""
        ),
        "choices": [
            {
                "desc": "Listen respectfully",
                "msg": (
                    "You shut up and listen. The veteran drops some real knowledge\n"
                    "about ring psychology and working the crowd.\n"
                    "You feel like you learned something tonight."
                ),
                "kayfabe": 2, "trust": 2, "money": 0, "stat_gain": "psy",
            },
            {
                "desc": "\"I know what I'm doing\"",
                "msg": (
                    "The veteran stares at you for a long moment, then walks away.\n"
                    "\"Good luck, kid. You're gonna need it.\"\n"
                    "The locker room noticed you blew off a legend."
                ),
                "kayfabe": 0, "trust": -3, "money": 0,
            },
        ],
    },
    # --- Promoter Pressure ---
    {
        "type": "promoter_pressure",
        "trigger_rooms": ["locker"],
        "title": "PROMOTER PULLS YOU ASIDE",
        "setup": (
            "The promoter grabs your arm. \"We need to talk about your gimmick.\n"
            "I've got an idea that'll get you over big... but you might not like it.\n"
            "How about we make you 'The Garbage Man'?\""
        ),
        "choices": [
            {
                "desc": "Go with it",
                "msg": (
                    "You swallow your pride. \"If it gets me on the card, I'll do it.\"\n"
                    "The promoter grins. \"That's the attitude, kid.\"\n"
                    "Sometimes you gotta eat the dirt to reach the mountaintop."
                ),
                "kayfabe": 3, "trust": 5, "money": 20,
            },
            {
                "desc": "Push back creatively",
                "msg": (
                    "\"How about a compromise? I keep my name but work a blue-collar\n"
                    "gimmick?\" The promoter thinks it over. \"...Not bad, kid.\"\n"
                    "You protected your identity AND got the promoter's respect."
                ),
                "kayfabe": 4, "trust": 3, "money": 0,
            },
            {
                "desc": "Flat-out refuse",
                "msg": (
                    "\"No way. I didn't get into this business to be a garbage man.\"\n"
                    "The promoter's face hardens. \"Your call. Hope you like dark matches.\""
                ),
                "kayfabe": 0, "trust": -5, "money": 0,
            },
        ],
    },
    # --- Bar Brawl ---
    {
        "type": "bar_brawl",
        "trigger_rooms": ["bar"],
        "title": "BAR CONFRONTATION",
        "setup": (
            "A drunk at the bar gets mouthy. \"Wrestling's fake! You couldn't\n"
            "beat me in a real fight!\" He shoves you. The whole bar is watching."
        ),
        "choices": [
            {
                "desc": "Stay cool",
                "msg": (
                    "You smile and buy the guy a beer. \"You're right, brother.\n"
                    "It's all a work.\" He calms down. Crisis averted.\n"
                    "But some of the boys saw you back down from a mark."
                ),
                "kayfabe": -2, "trust": 1, "money": -5,
            },
            {
                "desc": "Stretch him",
                "msg": (
                    "You put him in a legit hold. Nothing that'll leave marks,\n"
                    "but he taps out in seconds. \"Still think it's fake?\"\n"
                    "The bar erupts. Kayfabe: VERY protected."
                ),
                "kayfabe": 6, "trust": 0, "money": 0,
            },
            {
                "desc": "Leave before it escalates",
                "msg": (
                    "You settle your tab and walk out. No point proving\n"
                    "anything to a drunk. Smart move."
                ),
                "kayfabe": 0, "trust": 0, "money": 0,
            },
        ],
    },
    # --- Merchandise Opportunity ---
    {
        "type": "merch_opportunity",
        "trigger_rooms": ["locker", "bar"],
        "title": "MERCHANDISE DEAL",
        "setup": (
            "A guy with a screen-printing setup approaches you.\n"
            "\"I can make you 100 t-shirts with your face on 'em.\n"
            "Fifty bucks, you keep all the profit.\""
        ),
        "choices": [
            {
                "desc": "Take the deal ($50)",
                "msg": (
                    "You hand over the cash. A week later, you've got 100 shirts.\n"
                    "You sell them at shows for $10 each. Not bad."
                ),
                "kayfabe": 1, "trust": 0, "money": 50,
            },
            {
                "desc": "Negotiate ($25)",
                "msg": (
                    "\"How about $25 and I give you a shout-out on the mic?\"\n"
                    "He thinks about it... \"Deal.\" Smart business."
                ),
                "kayfabe": 0, "trust": 0, "money": 75,
            },
            {
                "desc": "Pass",
                "msg": (
                    "\"Not right now, brother.\" He shrugs and moves on.\n"
                    "Maybe next time."
                ),
                "kayfabe": 0, "trust": 0, "money": 0,
            },
        ],
    },
    # --- Training Tip ---
    {
        "type": "training_tip",
        "trigger_rooms": ["locker"],
        "title": "TRAINING INSIGHT",
        "setup": (
            "You're stretching in the locker room when you notice a veteran\n"
            "doing an unusual warm-up routine. They catch you watching.\n"
            "\"Want me to show you?\""
        ),
        "choices": [
            {
                "desc": "Learn the routine",
                "msg": (
                    "The veteran walks you through their conditioning program.\n"
                    "It's grueling but effective. You feel tougher already."
                ),
                "kayfabe": 0, "trust": 1, "money": 0, "stat_gain": "tou",
            },
            {
                "desc": "\"I've got my own routine\"",
                "msg": (
                    "\"Suit yourself.\" The veteran goes back to their business.\n"
                    "No harm done, but you might have missed an opportunity."
                ),
                "kayfabe": 0, "trust": 0, "money": 0,
            },
        ],
    },
    # --- Booker's Pet ---
    {
        "type": "booker_pet",
        "trigger_rooms": ["locker"],
        "title": "BACKSTAGE POLITICS",
        "setup": (
            "You overhear a conversation: the booker's nephew is getting\n"
            "pushed over more deserving talent. A group of wrestlers wants\n"
            "to confront the booker about it. They want you in on it."
        ),
        "choices": [
            {
                "desc": "Join the group",
                "msg": (
                    "You join the meeting with the booker. It's tense but productive.\n"
                    "The booker agrees to look at it. Solidarity with the boys."
                ),
                "kayfabe": 0, "trust": -2, "money": 0,
            },
            {
                "desc": "Stay out of it",
                "msg": (
                    "\"I just work here, brother.\" You keep your head down.\n"
                    "The boys are disappointed but the booker remembers who\n"
                    "didn't cause trouble."
                ),
                "kayfabe": 0, "trust": 3, "money": 0,
            },
        ],
    },
    # --- Lucky Break ---
    {
        "type": "lucky_break",
        "trigger_rooms": ["locker", "bar"],
        "title": "LUCKY BREAK",
        "setup": (
            "The main eventer just called in sick. The promoter is scrambling.\n"
            "He spots you. \"Kid, how'd you like to work the semi-main tonight?\""
        ),
        "choices": [
            {
                "desc": "\"Hell yes!\"",
                "msg": (
                    "You jump at the chance. It's your biggest match yet.\n"
                    "Even if you don't win, the exposure is invaluable.\n"
                    "The crowd doesn't know who you are — yet."
                ),
                "kayfabe": 3, "trust": 4, "money": 30,
            },
            {
                "desc": "\"I'm not ready\"",
                "msg": (
                    "The promoter frowns. \"Opportunity knocks once, kid.\"\n"
                    "He finds someone else. You wonder if you blew it."
                ),
                "kayfabe": 0, "trust": -2, "money": 0,
            },
        ],
    },
    # --- Ride Share ---
    {
        "type": "ride_share",
        "trigger_rooms": ["locker"],
        "title": "ROAD STORY",
        "setup": (
            "After the show, a group of wrestlers invites you to ride\n"
            "with them to the next town. It's cheaper than driving alone\n"
            "and you'll hear some incredible road stories."
        ),
        "choices": [
            {
                "desc": "Ride with the crew",
                "msg": (
                    "You pile into the van. The stories are legendary.\n"
                    "By dawn, you feel like part of the family.\n"
                    "You saved gas money too."
                ),
                "kayfabe": 1, "trust": 2, "money": 15,
            },
            {
                "desc": "Drive alone",
                "msg": (
                    "You prefer your own company on the road.\n"
                    "Nothing wrong with that. Some wrestlers need their space."
                ),
                "kayfabe": 0, "trust": 0, "money": 0,
            },
        ],
    },
    # --- Autograph Session ---
    {
        "type": "autograph_session",
        "trigger_rooms": ["bar"],
        "title": "AUTOGRAPH SESSION",
        "setup": (
            "The bar owner asks if you'd sign some autographs for the regulars.\n"
            "\"They're big fans. And I'll comp your tab.\""
        ),
        "choices": [
            {
                "desc": "Sign in character",
                "msg": (
                    "You sign autographs with your ring name and stay in character.\n"
                    "The fans eat it up. The bar owner is thrilled.\n"
                    "Free drinks and good kayfabe. Perfect night."
                ),
                "kayfabe": 4, "trust": 1, "money": 10,
            },
            {
                "desc": "Sign as yourself",
                "msg": (
                    "You sign your real name and chat with everyone normally.\n"
                    "Nice evening, but some fans look confused.\n"
                    "\"Wait, I thought you were supposed to be a heel?\""
                ),
                "kayfabe": -3, "trust": 0, "money": 10,
            },
            {
                "desc": "Decline",
                "msg": (
                    "\"Not tonight, I'm keeping to myself.\"\n"
                    "The bar owner shrugs. Fair enough."
                ),
                "kayfabe": 0, "trust": 0, "money": 0,
            },
        ],
    },
    # --- Stolen Finish ---
    {
        "type": "stolen_finish",
        "trigger_rooms": ["locker"],
        "title": "STOLEN FINISH",
        "setup": (
            "You're watching the show from backstage and see another wrestler\n"
            "do YOUR finishing move. They even got a pop from it.\n"
            "The boys are looking at you to see how you react."
        ),
        "choices": [
            {
                "desc": "Confront them professionally",
                "msg": (
                    "You pull them aside. \"That's my finish. We need to talk.\"\n"
                    "They apologize — they didn't know. Handled like a pro.\n"
                    "The boys respect how you dealt with it."
                ),
                "kayfabe": 2, "trust": 3, "money": 0,
            },
            {
                "desc": "Let it go",
                "msg": (
                    "It's not worth the drama. Besides, imitation is flattery.\n"
                    "But some of the boys wonder if you're a pushover."
                ),
                "kayfabe": -1, "trust": -1, "money": 0,
            },
            {
                "desc": "Make a scene",
                "msg": (
                    "You storm over and get in their face in front of everyone.\n"
                    "\"THAT'S MY MOVE!\" It's dramatic. The locker room is split.\n"
                    "The promoter is NOT happy about backstage drama."
                ),
                "kayfabe": 3, "trust": -4, "money": 0,
            },
        ],
    },
]


def trigger_backstage_segment(character, room_type):
    """
    Attempt to trigger a backstage segment.
    ~20% chance on room entry.

    Args:
        character: Wrestler character
        room_type: "locker" or "bar"

    Returns:
        segment dict or None
    """
    if random.random() > 0.20:
        return None

    eligible = [
        s for s in BACKSTAGE_SEGMENTS
        if room_type in s["trigger_rooms"]
    ]

    if not eligible:
        return None

    return random.choice(eligible)


def resolve_backstage_choice(character, segment, choice_index):
    """
    Resolve a backstage segment choice.

    Returns:
        (message, effects_dict)
    """
    choices = segment.get("choices", [])
    if choice_index < 0 or choice_index >= len(choices):
        return "Invalid choice.", {}

    choice = choices[choice_index]

    # Get a rival name for formatting
    rival_name = _get_rival_name(character)

    msg = choice["msg"].format(rival=rival_name)
    effects = {}

    # Apply kayfabe
    kayfabe_delta = choice.get("kayfabe", 0)
    if kayfabe_delta:
        from world.rules import kayfabe_change
        actual = kayfabe_change(character, kayfabe_delta)
        effects["kayfabe"] = actual
        if actual > 0:
            msg += f"\n|g  Kayfabe +{actual}|n"
        elif actual < 0:
            msg += f"\n|r  Kayfabe {actual}|n"

    # Apply trust
    trust_delta = choice.get("trust", 0)
    if trust_delta:
        territory = character.db.territory or ""
        if territory:
            from world.rules import change_promoter_trust
            actual = change_promoter_trust(character, territory, trust_delta)
            effects["trust"] = actual
            if actual > 0:
                msg += f"\n|g  Promoter Trust +{actual}|n"
            elif actual < 0:
                msg += f"\n|r  Promoter Trust {actual}|n"

    # Apply money
    money_delta = choice.get("money", 0)
    if money_delta:
        character.db.money = (character.db.money or 0) + money_delta
        effects["money"] = money_delta
        if money_delta > 0:
            msg += f"\n|g  +${money_delta}|n"
        elif money_delta < 0:
            msg += f"\n|r  -${abs(money_delta)}|n"

    # Apply stat gain
    stat_gain = choice.get("stat_gain")
    if stat_gain:
        from world.rules import training_gain
        gained, amount, _ = training_gain(character, stat_gain)
        if gained:
            effects["stat_gain"] = (stat_gain, amount)
            msg += f"\n|c  +{amount:.1f} {stat_gain.upper()}|n"

    return msg, effects


def _get_rival_name(character):
    """Get a rival name for segment formatting."""
    rivals = character.db.rivals or {}
    if rivals:
        return max(rivals, key=rivals.get)
    # Fallback: pick a random NPC name
    return "a veteran wrestler"


def format_segment_prompt(segment, character):
    """Format the backstage segment for display to the player."""
    rival_name = _get_rival_name(character)
    title = segment["title"]
    setup = segment["setup"].format(rival=rival_name)

    msg = (
        f"\n|Y*** {title} ***|n\n"
        f"{setup}\n\n"
    )

    for i, choice in enumerate(segment["choices"], 1):
        msg += f"  |w{i}|n. {choice['desc']}\n"

    msg += "\nChoose (enter number):"
    return msg
