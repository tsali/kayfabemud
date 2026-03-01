"""
Kayfabe: Protect the Business — Training command.

train <stat> — train a stat in a gym room
"""

import time
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
