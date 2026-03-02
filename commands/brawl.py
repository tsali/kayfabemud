"""
Kayfabe: Protect the Business — Bar brawl command.

brawl <target> — Quick 3-round bar fight in BarRooms.
"""

import random
from evennia.commands.command import Command


# Brawl round stat checks (STR, AGI, TOU)
BRAWL_ROUNDS = [
    {
        "stat": "str",
        "name": "Strength",
        "win_msg": "{a} lands a stiff right hand on {b}! Glasses shatter on the bar!",
        "lose_msg": "{b} ducks and cracks {a} with a barstool!",
    },
    {
        "stat": "agi",
        "name": "Agility",
        "win_msg": "{a} dodges a wild swing and slams {b} into the jukebox!",
        "lose_msg": "{b} sidesteps and shoves {a} face-first into a table!",
    },
    {
        "stat": "tou",
        "name": "Toughness",
        "win_msg": "{a} takes a hit and keeps coming — and drops {b} with a headbutt!",
        "lose_msg": "{b} absorbs everything {a} throws and keeps standing. Brutal counter!",
    },
]


class CmdBrawl(Command):
    """
    Start a quick bar brawl with an NPC or player.

    Usage:
      brawl <target>

    A quick 3-round bar fight using STR, AGI, and TOU checks.
    Win 2/3 rounds to win. Rewards: $5-15, 5-10 XP, +1 kayfabe.
    Must be in a bar room.
    """

    key = "brawl"
    aliases = ["barfight", "fight"]
    locks = "cmd:all()"
    help_category = "Wrestling"

    def func(self):
        caller = self.caller
        if not caller.db.chargen_complete:
            caller.msg("Finish character creation first.")
            return

        if caller.scripts.get("match_script"):
            caller.msg("You're already in a match. Finish that first.")
            return

        from typeclasses.rooms import BarRoom
        if not isinstance(caller.location, BarRoom):
            caller.msg("You can only start a brawl in a bar.")
            return

        if not self.args:
            caller.msg("Brawl who? Usage: brawl <target>")
            return

        target_name = self.args.strip()
        target = caller.search(target_name, location=caller.location)
        if not target:
            return

        if target == caller:
            caller.msg("You can't brawl yourself.")
            return

        # Check if target is a valid opponent
        from typeclasses.characters import Wrestler
        from typeclasses.npcs import NPCWrestler, BackyardNPC
        is_npc = isinstance(target, (NPCWrestler, BackyardNPC))
        is_player = isinstance(target, Wrestler) and target.db.chargen_complete

        if not (is_npc or is_player):
            caller.msg(f"You can't brawl {target.key}.")
            return

        # Run the brawl
        a_name = caller.key
        b_name = target.key

        caller.location.msg_contents(
            f"\n|R*** BAR BRAWL ***\n"
            f"{a_name} throws a punch at {b_name}! It's ON!|n\n"
        )

        a_wins = 0
        b_wins = 0

        for round_data in BRAWL_ROUNDS:
            stat_key = round_data["stat"]
            stat_name = round_data["name"]

            a_stat = caller.get_stat(stat_key)
            b_stat = target.get_stat(stat_key) if hasattr(target, 'get_stat') else 10

            # d20 + mod vs DC 10
            a_roll = random.randint(1, 20)
            a_mod = (a_stat - 10) // 2
            a_total = a_roll + a_mod

            b_roll = random.randint(1, 20)
            b_mod = (b_stat - 10) // 2
            b_total = b_roll + b_mod

            fmt = {"a": a_name, "b": b_name}

            if a_total >= b_total:
                msg = round_data["win_msg"].format(**fmt)
                a_wins += 1
                result = f"|g{a_name} wins the exchange!|n"
            else:
                msg = round_data["lose_msg"].format(**fmt)
                b_wins += 1
                result = f"|r{b_name} wins the exchange!|n"

            caller.location.msg_contents(
                f"|w[{stat_name} Check]|n {msg}\n{result}"
            )

        # Determine winner
        if a_wins >= 2:
            won = True
            money_reward = random.randint(5, 15)
            xp_reward = random.randint(5, 10)

            caller.location.msg_contents(
                f"\n|Y*** {a_name} WINS THE BRAWL! ***\n"
                f"{a_name} stands over {b_name}, catching their breath.\n"
                f"The bartender shakes his head and starts sweeping up glass.|n\n"
            )

            caller.db.money = (caller.db.money or 0) + money_reward
            caller.db.xp = (caller.db.xp or 0) + xp_reward

            from world.rules import kayfabe_change, check_level_up
            kayfabe_change(caller, 1, "bar brawl win")
            levels = check_level_up(caller)

            caller.msg(
                f"|gRewards: ${money_reward}, {xp_reward} XP, +1 kayfabe|n"
            )
            if levels > 0:
                caller.msg(f"|YLEVEL UP! Now level {caller.db.level}!|n")
        else:
            caller.location.msg_contents(
                f"\n|r*** {b_name} WINS THE BRAWL! ***\n"
                f"{b_name} dusts off and orders another drink.\n"
                f"{a_name} picks themselves up off the floor.|n\n"
            )

            # Small consolation XP
            caller.db.xp = (caller.db.xp or 0) + 3
            caller.msg("|xYou lost, but gained 3 XP for the effort.|n")
