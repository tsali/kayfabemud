"""
Kayfabe: Protect the Business — NPC typeclasses.
"""

import random
from evennia.objects.objects import DefaultCharacter
from evennia.utils import lazy_property

from .objects import ObjectParent


# Ambient promo lines by alignment
AMBIENT_PROMOS = {
    "Face": [
        "{name} stretches in the corner, warming up for the crowd.",
        "{name} high-fives a fan at ringside.",
        "{name} shadowboxes, working through combinations.",
        "{name} waves to the crowd, who cheer loudly.",
        '{name} shouts: "I\'m ready for anyone tonight!"',
        "{name} checks the ring ropes, testing their tautness.",
        "{name} signs a t-shirt for a young fan.",
        "{name} does push-ups in the corner, getting pumped.",
        "{name} claps their hands, rallying the crowd.",
        "{name} paces the ring, eyes locked on the entrance ramp.",
        "{name} rolls their neck and bounces on the balls of their feet.",
        "{name} shakes hands with the timekeeper.",
        '{name} points to the crowd: "This one\'s for all of you!"',
        "{name} adjusts their elbow pad and takes a deep breath.",
        "{name} gives a thumbs-up to the announcer.",
    ],
    "Heel": [
        "{name} sneers at the crowd, drawing boos.",
        "{name} berates a nearby fan for wearing a cheap t-shirt.",
        '{name} mutters: "None of you deserve to see me wrestle."',
        "{name} polishes their boots, ignoring everyone.",
        "{name} flexes in a mirror, admiring themselves.",
        '{name} yells: "I\'m the best in this building and you all know it!"',
        "{name} shoves a ringside chair out of their way.",
        "{name} demands a ring attendant hold the ropes open.",
        "{name} spits on the floor and glares at the crowd.",
        '{name} laughs: "You people paid to see greatness. You\'re welcome."',
        "{name} checks their reflection in a phone screen.",
        "{name} points at the camera and mouths something threatening.",
        "{name} leans on the turnbuckle, looking bored.",
        "{name} cracks their knuckles menacingly.",
        '{name} snaps at a fan: "Get that phone out of my face!"',
    ],
    "Anti-Hero": [
        "{name} leans against the wall, arms crossed, watching everyone.",
        "{name} cracks their knuckles, staring at no one in particular.",
        "{name} drinks a beer in the corner and doesn't seem to care.",
        '{name} says: "I don\'t follow the script. I AM the script."',
        "{name} acknowledges the crowd with a curt nod.",
        "{name} scans the room like they're sizing up every last person.",
        "{name} sits on the top turnbuckle, feet dangling.",
        "{name} stares at the ceiling, lost in thought.",
        "{name} tosses a water bottle into the crowd without looking.",
        '{name} mutters: "Same crap, different night."',
        "{name} pulls their hood up and lurks in the shadows.",
        "{name} stretches against the ropes, stone-faced.",
        "{name} lights a cigarette backstage, breaking about three rules.",
        "{name} gives a barely perceptible nod to a passerby.",
        "{name} leans on the barricade, ignoring both cheers and boos.",
    ],
}

TARGETED_PROMOS = {
    ("Heel", "Face"): [
        '{npc} sneers at {player}: "You don\'t belong here, kid."',
        '{npc} gets in {player}\'s face: "I\'m everything you wish you were."',
        '{npc} points at {player}: "That title run of yours? I\'m ending it."',
        '{npc} mocks {player}\'s entrance pose, drawing laughs.',
        '{npc} tells {player}: "The crowd cheers for you now. Wait until I\'m done."',
    ],
    ("Face", "Face"): [
        '{npc} nods at {player}: "Keep fighting the good fight."',
        '{npc} offers {player} a fist bump: "Respect."',
        '{npc} claps {player} on the shoulder: "You\'re getting better."',
        '{npc} tells {player}: "We should tag up sometime."',
    ],
    ("Heel", "Heel"): [
        '{npc} gives {player} a knowing look: "We should talk business."',
        '{npc} sidles up to {player}: "Stay out of my way, and I\'ll stay out of yours."',
        '{npc} whispers to {player}: "I know who\'s getting the push. Play it smart."',
        '{npc} raises an eyebrow at {player}: "Temporary alliance?"',
    ],
    ("Face", "Heel"): [
        '{npc} stares down {player}: "I know what you\'re about. It won\'t work on me."',
        '{npc} steps between {player} and a fan: "Leave them alone."',
        '{npc} tells {player}: "Sooner or later, you\'ll answer for all of it."',
    ],
    ("Anti-Hero", "Face"): [
        '{npc} glances at {player}: "Don\'t expect me to save you."',
        '{npc} shrugs at {player}: "You do you. I\'ll do me."',
    ],
    ("Anti-Hero", "Heel"): [
        '{npc} locks eyes with {player}: "Try me. See what happens."',
        '{npc} smirks at {player}: "You\'re not as tough as you think."',
    ],
    ("Anti-Hero", "Anti-Hero"): [
        '{npc} and {player} share a long, silent stare. Mutual respect? Maybe.',
        '{npc} raises their beer toward {player}. Not a toast -- a warning.',
    ],
}

TRAINER_LINES = [
    "{name} barks: \"Again! Do it again! That was sloppy!\"",
    "{name} demonstrates a hold with practiced precision.",
    "{name} watches from their chair, arms crossed, face unreadable.",
    "{name} nods approvingly at a student's technique.",
    "{name} shakes their head. \"You call that a bump?\"",
]

ANNOUNCER_LINES = [
    "{name} adjusts their headset and tests the mic.",
    "{name} reviews tonight's match card.",
    "{name} chats with a timekeeper about the finish order.",
]


class NPCWrestler(ObjectParent, DefaultCharacter):
    """
    An NPC wrestler in the game world.

    Attributes:
        npc_id (int): Unique ID from npc_data (#1-380)
        based_on (str): Real wrestler this is based on
        alignment (str): Face/Heel/Anti-Hero
        finisher_name (str): Finishing move name
        finisher_type (str): power/technical/aerial/charisma
        home_territory (str): Territory key where this NPC is based
        is_champion (bool): Currently holds a title
        title_held (str): Name of title held
        is_guest (bool): Currently on a guest appearance
        guest_territory (str): Where they're guesting
        level (int): NPC level (determines stat ranges)
    """

    @lazy_property
    def traits(self):
        from evennia.contrib.rpg.traits import TraitHandler
        return TraitHandler(self)

    def at_object_creation(self):
        super().at_object_creation()
        self.db.npc_id = 0
        self.db.based_on = ""
        self.db.gender = "Male"
        self.db.alignment = "Face"
        self.db.finisher_name = ""
        self.db.finisher_type = "power"
        self.db.home_territory = ""
        self.db.is_champion = False
        self.db.title_held = ""
        self.db.is_guest = False
        self.db.guest_territory = ""
        self.db.level = 1
        self.db.role = "wrestler"  # wrestler, trainer, announcer, authority

    def setup_stats(self, str_val, agi_val, tec_val, cha_val, tou_val, psy_val):
        """Set up traits with given values."""
        for key, name, val in [
            ("str", "Strength", str_val),
            ("agi", "Agility", agi_val),
            ("tec", "Technical", tec_val),
            ("cha", "Charisma", cha_val),
            ("tou", "Toughness", tou_val),
            ("psy", "Psychology", psy_val),
        ]:
            self.traits.add(key, name, trait_type="static", base=val, min=1, max=30)

    def get_stat(self, stat_key):
        trait = self.traits.get(stat_key)
        return trait.value if trait else 0

    def get_display_name(self, looker=None, **kwargs):
        name = super().get_display_name(looker, **kwargs)
        align = self.db.alignment
        if align == "Face":
            tag = "|g[Face]|n"
        elif align == "Heel":
            tag = "|r[Heel]|n"
        elif align == "Anti-Hero":
            tag = "|y[Anti-Hero]|n"
        else:
            tag = ""
        role = self.db.role or "wrestler"
        if role == "trainer":
            tag = f"|m[Trainer]|n {tag}"
        elif role == "announcer":
            tag = f"|x[Announcer]|n"
        elif role == "authority":
            tag = f"|w[Authority]|n {tag}"
        guest = ""
        if self.db.is_guest:
            guest = " |c[Guest]|n"
        return f"{name} {tag}{guest}".strip()

    def do_ambient_action(self):
        """
        Perform a random ambient action visible to the room.
        Called periodically by NPCSchedulerScript.
        """
        if not self.location:
            return

        role = self.db.role or "wrestler"
        alignment = self.db.alignment or "Face"

        if role == "trainer":
            lines = TRAINER_LINES
        elif role == "announcer":
            lines = ANNOUNCER_LINES
        else:
            # 30% chance for player-targeted line
            from typeclasses.characters import Wrestler
            players = [
                obj for obj in self.location.contents
                if isinstance(obj, Wrestler) and obj.db.chargen_complete
                and obj.sessions.count()
            ]
            if players and random.random() < 0.3:
                target = random.choice(players)
                p_align = target.db.alignment or "Face"
                key = (alignment, p_align)
                targeted = TARGETED_PROMOS.get(key, [])
                if targeted:
                    line = random.choice(targeted).format(npc=self.key, player=target.key)
                    self.location.msg_contents(f"|x{line}|n")
                    return
            lines = AMBIENT_PROMOS.get(alignment, AMBIENT_PROMOS["Face"])

        line = random.choice(lines).format(name=self.key)
        self.location.msg_contents(f"|x{line}|n")

    def do_ambient_promo(self):
        """Cut a promo to the room, using alignment-appropriate lines."""
        if not self.location:
            return

        alignment = self.db.alignment or "Face"
        cha = self.get_stat("cha")

        if alignment == "Face":
            promos = [
                f'|g{self.key} grabs the mic: "I came here to fight for every '
                f'single one of you tonight! Let\'s GO!"|n',
                f'|g{self.key}: "This is OUR house! And nobody takes '
                f'it from us!"|n',
            ]
        elif alignment == "Heel":
            promos = [
                f'|r{self.key} snatches the mic: "Every last one of you '
                f'paid to watch a REAL wrestler. You\'re welcome."|n',
                f'|r{self.key}: "I\'m better than everyone in this building '
                f'and that includes the boys in the back!"|n',
            ]
        else:
            promos = [
                f'|y{self.key} takes the mic and stares silently at the crowd '
                f'for ten long seconds before dropping it and walking away.|n',
                f'|y{self.key}: "I don\'t care about your cheers or your boos. '
                f'I care about the bell."|n',
            ]

        if cha >= 16:
            promos.append(
                f"|Y*** {self.key} cuts a LEGENDARY promo that has the crowd "
                f"absolutely losing their minds! ***|n"
            )

        line = random.choice(promos)
        self.location.msg_contents(line)

    def issue_challenge(self):
        """
        Issue a challenge to players in the room.
        Called occasionally by NPCSchedulerScript for high-level NPCs.
        """
        if not self.location:
            return

        from typeclasses.characters import Wrestler
        players = [
            obj for obj in self.location.contents
            if isinstance(obj, Wrestler) and obj.db.chargen_complete
        ]
        if not players:
            return

        target = random.choice(players)
        alignment = self.db.alignment or "Face"

        if alignment == "Heel":
            msg = (
                f'\n|r{self.key} points at {target.key}: "You! Yeah, you! '
                f"I've seen better wrestling at a school play. "
                f'Get in this ring and I\'ll show you what a REAL '
                f'wrestler looks like!"|n\n'
                f"|w(Type |cwrestle {self.key}|w to accept the challenge)|n"
            )
        elif alignment == "Face":
            msg = (
                f'\n|g{self.key} nods at {target.key}: "Hey, I\'ve been '
                f"watching you work. You've got something. "
                f'How about we go a few rounds and see what you\'re made of?"|n\n'
                f"|w(Type |cwrestle {self.key}|w to accept the challenge)|n"
            )
        else:
            msg = (
                f'\n|y{self.key} locks eyes with {target.key}. No words. '
                f'Just a slow, deliberate nod toward the ring.|n\n'
                f"|w(Type |cwrestle {self.key}|w to accept the challenge)|n"
            )

        self.location.msg_contents(msg)

    def react_to_match(self, winner, loser, stars):
        """
        React to a match that just happened in this NPC's room.
        Called from _end_match() in wrestling.py.
        40% chance to react.
        """
        if not self.location or random.random() > 0.4:
            return

        alignment = self.db.alignment or "Face"
        w_name = winner.key if winner else "the winner"
        l_name = loser.key if loser else "the loser"

        if alignment == "Heel":
            reactions = [
                f'|r{self.key} slow-claps mockingly: "Was that supposed to impress me?"|n',
                f"|r{self.key} sneers at {l_name}: \"Pathetic. I could've beaten both of you.\"|n",
                f"|r{self.key} yawns theatrically: \"Wake me when someone good gets in the ring.\"|n",
                f'|r{self.key} shakes their head at {w_name}: "Lucky. That\'s all that was."|n',
            ]
            if stars >= 4:
                reactions.append(
                    f'|r{self.key} looks annoyed that {w_name} is getting all the attention.|n'
                )
        elif alignment == "Face":
            reactions = [
                f"|g{self.key} applauds the match. \"Hell of a fight!\"|n",
                f"|g{self.key} nods at {w_name}: \"Great match out there.\"|n",
                f"|g{self.key} pats {l_name} on the back: \"You'll get 'em next time.\"|n",
            ]
            if stars >= 4:
                reactions.append(
                    f"|g{self.key} leads the crowd in a standing ovation for both wrestlers!|n"
                )
        else:
            reactions = [
                f"|y{self.key} watches silently, giving nothing away.|n",
                f"|y{self.key} nods once -- barely perceptible -- at {w_name}.|n",
                f"|y{self.key} stares at the ring. Processing. Planning.|n",
            ]

        self.location.msg_contents(random.choice(reactions))


class NPCManager(ObjectParent, DefaultCharacter):
    """
    An NPC manager who can be hired by players.

    Provides CHA/PSY bonuses and special abilities.
    """

    @lazy_property
    def traits(self):
        from evennia.contrib.rpg.traits import TraitHandler
        return TraitHandler(self)

    def at_object_creation(self):
        super().at_object_creation()
        self.db.npc_id = 0
        self.db.based_on = ""
        self.db.alignment = "Heel"
        self.db.style = ""  # cowardly genius, fast-talking, etc.
        self.db.specialty = ""  # what they're known for
        self.db.home_territory = ""
        self.db.retainer_cost = 100  # weekly cost
        self.db.cut_percent = 20  # % of match payoffs
        self.db.managed_wrestler = None  # dbref of current client
        self.db.available = True  # can be hired

    def setup_stats(self, cha_val, psy_val):
        """Managers only have CHA and PSY."""
        self.traits.add("cha", "Charisma", trait_type="static", base=cha_val, min=1, max=30)
        self.traits.add("psy", "Psychology", trait_type="static", base=psy_val, min=1, max=30)

    def get_stat(self, stat_key):
        trait = self.traits.get(stat_key)
        return trait.value if trait else 0

    def get_display_name(self, looker=None, **kwargs):
        name = super().get_display_name(looker, **kwargs)
        avail = "|g[Available]|n" if self.db.available else "|r[Hired]|n"
        return f"{name} |m[Manager]|n {avail}"

    def get_cha_bonus(self):
        """CHA bonus provided to managed wrestler (partial)."""
        cha = int(self.get_stat("cha"))
        return max(1, cha // 4)

    def get_psy_bonus(self):
        """PSY bonus provided to managed wrestler (partial)."""
        psy = int(self.get_stat("psy"))
        return max(1, psy // 5)

    def cut_promo_for(self, wrestler):
        """Cut a promo on behalf of the managed wrestler."""
        if not self.location:
            return 0, ""

        cha = self.get_stat("cha")
        psy = self.get_stat("psy")

        from world.rules import stat_check
        success, roll, total, margin = stat_check(cha, 10, bonus=psy // 4)

        if margin >= 8:
            quality = "legendary"
            msg = (
                f"|Y{self.key} grabs the mic and cuts a promo so scorching "
                f"that {wrestler.key} doesn't even need to speak. The crowd "
                f"is RIVETED. This is why you hire the best.|n"
            )
            xp = 20
        elif success:
            quality = "good"
            msg = (
                f"|w{self.key} takes the mic and hypes up {wrestler.key} "
                f"with a passionate promo. The crowd responds!|n"
            )
            xp = 10
        else:
            quality = "flat"
            msg = (
                f"|x{self.key} tries to cut a promo for {wrestler.key} "
                f"but the crowd isn't buying it tonight.|n"
            )
            xp = 3

        if self.location:
            self.location.msg_contents(msg)

        return xp, quality

    def attempt_interference(self, match_script, is_helping_a=True):
        """
        Attempt to interfere in a match on behalf of managed wrestler.
        Heel managers only. Risk of DQ.
        """
        if self.db.alignment == "Face":
            return False, "Face managers don't cheat."

        psy = self.get_stat("psy")
        from world.rules import stat_check
        # High difficulty — getting caught means DQ
        success, roll, total, margin = stat_check(psy, 14)

        if success:
            # Successful interference — bonus damage to opponent
            if is_helping_a:
                match_script.db.b_health = max(0, match_script.db.b_health - 10)
            else:
                match_script.db.a_health = max(0, match_script.db.a_health - 10)
            return True, f"|r{self.key} distracts the referee! Cheap shot!|n"
        else:
            return False, f"|r{self.key} gets caught by the referee! WARNING!|n"

    def do_ambient_action(self):
        """Ambient manager behavior."""
        if not self.location:
            return

        lines = [
            f"{self.key} adjusts their tie and surveys the room.",
            f"{self.key} whispers strategy to a nearby wrestler.",
            f"{self.key} talks loudly into a cell phone about 'the deal'.",
            f"{self.key} polishes their championship ring.",
            f"{self.key} scribbles notes on a legal pad.",
        ]

        if self.db.alignment == "Heel":
            lines.extend([
                f"{self.key} counts a thick stack of bills, sneering.",
                f'{self.key} mutters: "Everyone has a price."',
            ])
        elif self.db.alignment == "Face":
            lines.extend([
                f"{self.key} encourages a young wrestler with a pep talk.",
                f"{self.key} signs an autograph for a fan.",
            ])

        line = random.choice(lines)
        self.location.msg_contents(f"|x{line}|n")


class BackyardNPC(NPCWrestler):
    """
    Randomly-generated low-level NPC for Tier 1 backyard feds.
    Silly names, low stats. Generated by backyard_npcs.py.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.role = "backyard"
        self.db.is_generated = True
