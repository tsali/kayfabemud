"""
Kayfabe: Protect the Business — Training commands.

train <stat>  — train a stat in a gym room
learn [vet]   — learn signature moves from veteran NPCs
"""

import time
import random
from evennia.commands.command import Command


STAT_NAMES = {
    "str": "Strength",
    "agi": "Agility",
    "tec": "Technical",
    "cha": "Charisma",
    "tou": "Toughness",
    "psy": "Psychology",
}

NAME_TO_KEY = {
    "str": "str", "strength": "str",
    "agi": "agi", "agility": "agi",
    "tec": "tec", "technical": "tec", "tech": "tec",
    "cha": "cha", "charisma": "cha",
    "tou": "tou", "toughness": "tou", "tough": "tou",
    "psy": "psy", "psychology": "psy", "psych": "psy",
}

TRAINING_COOLDOWN = 300  # 5 minutes between training attempts


class CmdTrain(Command):
    """
    Train a stat at a gym.

    Usage:
      train <stat>
      train str / agi / tec / cha / tou / psy

    Must be in a gym room. Some gyms give bonuses to specific stats.
    Training has a cooldown and diminishing returns at higher stat values.
    """

    key = "train"
    aliases = ["workout"]
    locks = "cmd:all()"
    help_category = "Wrestling"

    def func(self):
        caller = self.caller
        if not caller.db.chargen_complete:
            caller.msg("Finish character creation first.")
            return

        if caller.scripts.get("match_script"):
            caller.msg("You're in a match. Train later.")
            return

        # Check if in a gym room
        location = caller.location
        room_type = getattr(location.db, 'room_type', '')
        is_gym = room_type == "gym"
        is_training = room_type == "training"
        is_pit = "pit" in (location.key or "").lower()

        if not (is_gym or is_training or is_pit):
            caller.msg("You need to be in a gym or training area to train.")
            return

        if not self.args:
            caller.msg(
                "|wTrainable stats:|n\n"
                "  |cstr|n — Strength    |ctou|n — Toughness\n"
                "  |cagi|n — Agility     |cpsy|n — Psychology\n"
                "  |ctec|n — Technical   |ccha|n — Charisma\n\n"
                "Usage: |wtrain <stat>|n"
            )
            # Show room bonus if any
            bonus_stat = getattr(location.db, 'stat_bonus', '')
            if bonus_stat:
                bonus_amt = getattr(location.db, 'bonus_amount', 0)
                caller.msg(
                    f"|yThis room gives a bonus to {STAT_NAMES.get(bonus_stat, bonus_stat)}"
                    f" (+{bonus_amt})|n"
                )
            return

        stat_input = self.args.strip().lower()
        stat_key = NAME_TO_KEY.get(stat_input)

        if not stat_key:
            caller.msg(f"Unknown stat '{stat_input}'. Options: str, agi, tec, cha, tou, psy")
            return

        # Check cooldown
        last_train = caller.attributes.get("last_train_time", default=0)
        now = time.time()
        if now - last_train < TRAINING_COOLDOWN:
            remaining = int(TRAINING_COOLDOWN - (now - last_train))
            mins = remaining // 60
            secs = remaining % 60
            caller.msg(f"You're still recovering from your last session. ({mins}m {secs}s remaining)")
            return

        # Room bonus
        room_bonus = 0
        bonus_stat = getattr(location.db, 'stat_bonus', '')
        if bonus_stat == stat_key:
            room_bonus = getattr(location.db, 'bonus_amount', 0)

        # Attempt training
        from world.rules import training_gain
        gained, amount, msg = training_gain(caller, stat_key, room_bonus=room_bonus)

        stat_name = STAT_NAMES.get(stat_key, stat_key)

        if gained:
            new_val = caller.get_stat(stat_key)
            caller.msg(
                f"\n|w--- TRAINING: {stat_name} ---|n\n"
                f"You push yourself hard...\n"
                f"|g{msg}|n\n"
                f"{stat_name}: |w{new_val:.1f}|n"
            )
            if room_bonus > 0:
                caller.msg(f"|y(Room bonus: +{room_bonus * 0.3:.1f})|n")

            # Small XP for training
            caller.db.xp = (caller.db.xp or 0) + 5

            # Rapport gain for training near vets
            vets = _find_vets_in_room(location)
            if vets:
                rapport = caller.db.vet_rapport or {}
                for vet in vets:
                    old_r = rapport.get(vet.key, 0)
                    rapport[vet.key] = min(100, old_r + 2)
                caller.db.vet_rapport = rapport

            from world.rules import check_level_up
            levels = check_level_up(caller)
            if levels > 0:
                caller.msg(f"|YLEVEL UP! Now level {caller.db.level}!|n")
        else:
            caller.msg(
                f"\n|w--- TRAINING: {stat_name} ---|n\n"
                f"|x{msg}|n"
            )

        # Set cooldown regardless
        caller.attributes.add("last_train_time", now)

        # Post-training breadcrumb
        if gained:
            caller.msg(
                "\n|wType |cstats|w to check your stats, or |cwrestle|w to test them.|n"
            )


LEARN_COOLDOWN = 300  # 5 minutes between learn attempts

# Rapport thresholds for unlocking moves
RAPPORT_THRESHOLDS = [20, 50, 80]

# Flavor text for learning
_LEARN_SUCCESS = [
    "takes you aside and walks you through the move step by step.",
    "nods approvingly. 'You're ready for this one, kid.'",
    "shows you the move three times, then watches you drill it.",
    "grabs your arm and positions you. 'Feel that? That's the hold.'",
    "demonstrates the move at full speed, then slows it down for you.",
]

_LEARN_FAIL = [
    "shakes their head. 'Not quite. Come back when you've got it.'",
    "watches your attempt and sighs. 'You need more seasoning.'",
    "stops you mid-attempt. 'Your form is off. Keep drilling.'",
]


def _find_vets_in_room(location):
    """Find NPCs with signature_moves in the current room."""
    from typeclasses.npcs import NPCWrestler
    vets = []
    for obj in location.contents:
        if isinstance(obj, NPCWrestler) and getattr(obj.db, 'signature_moves', None):
            vets.append(obj)
    return vets


class CmdLearn(Command):
    """
    Learn signature moves from veteran NPCs.

    Usage:
        learn                    - List nearby vets and what they teach
        learn <vet name>         - See their moves, your rapport, unlocks
        learn <vet name> <move>  - Attempt to learn a move

    Veterans teach their signature moves when you build enough rapport.
    Rapport increases by wrestling in their territory and training near them.
    """

    key = "learn"
    aliases = ["study"]
    locks = "cmd:all()"
    help_category = "Wrestling"

    def func(self):
        from world.moves import MOVES

        caller = self.caller
        if not caller.db.chargen_complete:
            caller.msg("Finish character creation first.")
            return

        if caller.scripts.get("match_script"):
            caller.msg("You're in a match right now.")
            return

        location = caller.location
        if not location:
            return

        vets = _find_vets_in_room(location)

        if not self.args:
            # List nearby vets
            if not vets:
                caller.msg(
                    "There are no veterans here who can teach you moves.\n"
                    "Look for trainers and top wrestlers in territory arenas."
                )
                return

            msg = f"\n|w{'=' * 50}|n\n|w  VETERANS WHO CAN TEACH|n\n|w{'=' * 50}|n\n"
            rapport = caller.db.vet_rapport or {}
            for vet in vets:
                sig_moves = vet.db.signature_moves or []
                r = rapport.get(vet.key, 0)
                move_names = []
                for mk in sig_moves:
                    m = MOVES.get(mk)
                    if m:
                        move_names.append(m["name"])
                msg += (
                    f"  |c{vet.key}|n (Rapport: {r}/100)\n"
                    f"    Teaches: {', '.join(move_names) if move_names else 'None'}\n"
                )
            msg += (
                f"\n  |wType |clearn <vet name>|w for details.|n\n"
                f"|w{'=' * 50}|n"
            )
            caller.msg(msg)
            return

        # Parse args: could be "vet name" or "vet name move"
        args = self.args.strip()

        # Try to match a vet by name (longest match first)
        matched_vet = None
        remaining = ""
        args_lower = args.lower()

        # Pass 1: full name match at start of args
        for vet in vets:
            vet_lower = vet.key.lower()
            if args_lower.startswith(vet_lower):
                if len(args_lower) == len(vet_lower) or args_lower[len(vet_lower)] == " ":
                    matched_vet = vet
                    remaining = args[len(vet_lower):].strip()
                    break

        # Pass 2: try matching any sub-name of the vet (e.g. "afa" matches "Chief Afa Savea")
        # Prefer longer matches to avoid ambiguity
        if not matched_vet:
            best_match = None
            best_len = 0
            for vet in vets:
                vet_parts = vet.key.lower().split()
                # Try progressively longer combos from each starting word
                for start in range(len(vet_parts)):
                    for end in range(start + 1, len(vet_parts) + 1):
                        fragment = " ".join(vet_parts[start:end])
                        if args_lower.startswith(fragment):
                            after = args_lower[len(fragment):]
                            if not after or after[0] == " ":
                                if len(fragment) > best_len:
                                    best_match = vet
                                    best_len = len(fragment)
                                    remaining = args[len(fragment):].strip()
            if best_match:
                matched_vet = best_match

        if not matched_vet:
            if vets:
                vet_names = ", ".join(v.key for v in vets)
                caller.msg(f"No vet named '{args}' here. Available: {vet_names}")
            else:
                caller.msg("No veterans here who can teach moves.")
            return

        rapport = caller.db.vet_rapport or {}
        r = rapport.get(matched_vet.key, 0)
        sig_moves = matched_vet.db.signature_moves or []
        known = caller.db.known_moves or []

        if not remaining:
            # Show vet details
            msg = (
                f"\n|w{'=' * 50}|n\n"
                f"|w  {matched_vet.key}|n\n"
                f"|w{'=' * 50}|n\n"
                f"  Rapport: |c{r}|n/100\n\n"
                f"  |wSignature Moves:|n\n"
            )
            for i, mk in enumerate(sig_moves):
                m = MOVES.get(mk)
                if not m:
                    continue
                threshold = RAPPORT_THRESHOLDS[i] if i < len(RAPPORT_THRESHOLDS) else 80
                if mk in known:
                    status = "|g[LEARNED]|n"
                elif r >= threshold:
                    status = "|y[AVAILABLE]|n"
                else:
                    status = f"|x[Requires {threshold} rapport]|n"
                msg += f"    |c{m['name']}|n {status}\n"
                msg += f"      {m['type'].title()} — Diff:{m['difficulty']} Dmg:{m['damage']}\n"

            msg += (
                f"\n  |wTo learn: |clearn {matched_vet.key.split()[0].lower()} <move name>|n\n"
                f"|w{'=' * 50}|n"
            )
            caller.msg(msg)
            return

        # Try to learn a move
        move_search = remaining.lower().replace(" ", "_")
        target_move = None
        target_key = None
        for mk in sig_moves:
            m = MOVES.get(mk)
            if not m:
                continue
            if move_search in mk or move_search in m["name"].lower().replace(" ", "_"):
                target_move = m
                target_key = mk
                break

        if not target_move:
            caller.msg(
                f"{matched_vet.key} doesn't teach a move matching '{remaining}'.\n"
                f"Type |wlearn {matched_vet.key.split()[0].lower()}|n to see their moves."
            )
            return

        # Already known?
        if target_key in known:
            caller.msg(f"You already know {target_move['name']}.")
            return

        # Check rapport threshold
        move_idx = sig_moves.index(target_key) if target_key in sig_moves else 0
        threshold = RAPPORT_THRESHOLDS[move_idx] if move_idx < len(RAPPORT_THRESHOLDS) else 80
        if r < threshold:
            caller.msg(
                f"|rYour rapport with {matched_vet.key} is {r}/100.\n"
                f"You need {threshold} rapport to learn {target_move['name']}.\n"
                f"Keep wrestling in their territory to build rapport.|n"
            )
            return

        # Check cooldown
        last_learn = caller.attributes.get("last_learn_time", default=0)
        now = time.time()
        if now - last_learn < LEARN_COOLDOWN:
            remaining_t = int(LEARN_COOLDOWN - (now - last_learn))
            mins = remaining_t // 60
            secs = remaining_t % 60
            caller.msg(f"You need to rest before trying to learn again. ({mins}m {secs}s)")
            return

        # Stat check — use the move's primary stat
        from world.rules import stat_check
        stat_val = caller.get_stat(target_move["stat"])
        dc = target_move["difficulty"] + 5  # Base DC
        success, roll, total, margin = stat_check(stat_val, dc)

        caller.attributes.add("last_learn_time", now)

        if success:
            known.append(target_key)
            caller.db.known_moves = known
            flavor = random.choice(_LEARN_SUCCESS)
            caller.msg(
                f"\n|g*** MOVE LEARNED: {target_move['name']} ***|n\n"
                f"  {matched_vet.key} {flavor}\n"
                f"  You can now use |wwork {target_key}|n in matches.\n"
            )
        else:
            caller.msg(
                f"\n|y--- TRAINING SESSION ---\n"
                f"  {matched_vet.key} {random.choice(_LEARN_FAIL)}\n"
                f"  Keep training and try again.|n\n"
            )
