"""
Kayfabe: Protect the Business — Promo command.

promo <type> [target] — cut a promo
Types: fire, heat, challenge, shoot, manager
"""

from evennia.commands.command import Command
from world.rules import resolve_promo, kayfabe_change, check_level_up, PROMO_TYPES


class CmdPromo(Command):
    """
    Cut a promo — the verbal side of wrestling.

    Usage:
      promo fire             — rally the crowd (Face)
      promo heat             — insult the fans (Heel)
      promo challenge <name> — call out an opponent
      promo shoot            — break kayfabe, speak truth (Anti-Hero/risky)
      promo manager          — let your manager talk for you

    Promos use CHA + PSY. Alignment-matching promos get bonuses.
    Good promos earn XP and boost kayfabe. Bad ones hurt both.
    """

    key = "promo"
    aliases = ["cut"]
    locks = "cmd:all()"
    help_category = "Wrestling"

    def func(self):
        caller = self.caller
        if not caller.db.chargen_complete:
            caller.msg("Finish character creation first.")
            return

        # Can't promo during a match (that's what work/sell is for)
        if caller.scripts.get("match_script"):
            caller.msg("You're in a match. Focus on the ring work.")
            return

        if not self.args:
            caller.msg(
                "|wPromo types:|n\n"
                "  |cfire|n      — Rally the crowd (Face)\n"
                "  |cheat|n      — Insult the fans (Heel)\n"
                "  |cchallenge|n — Call out an opponent\n"
                "  |cshoot|n     — Break kayfabe (Anti-Hero/risky)\n"
                "  |cmanager|n   — Let your manager talk\n\n"
                "Usage: |wpromo <type> [target]|n"
            )
            return

        parts = self.args.strip().split(None, 1)
        promo_type = parts[0].lower()
        target_name = parts[1] if len(parts) > 1 else ""

        if promo_type not in PROMO_TYPES:
            caller.msg(f"Unknown promo type '{promo_type}'. Types: fire, heat, challenge, shoot, manager")
            return

        # Manager promo requires having a manager
        manager_name = ""
        if promo_type == "manager":
            if not caller.db.manager:
                caller.msg("You don't have a manager. Hire one first.")
                return
            manager_name = caller.db.manager

        # Challenge promo requires a target
        if promo_type == "challenge" and not target_name:
            caller.msg("Challenge who? Usage: |wpromo challenge <name>|n")
            return

        # Resolve the promo
        quality, margin, xp, kayfabe_delta, msg = resolve_promo(
            caller, promo_type, target_name=target_name, manager_name=manager_name
        )

        # Apply results
        caller.db.xp = (caller.db.xp or 0) + xp
        actual_delta = kayfabe_change(caller, kayfabe_delta)

        # Announce to room
        ptype_data = PROMO_TYPES[promo_type]
        caller.msg(f"\n|w--- PROMO ---\n{ptype_data['desc']}|n")
        caller.msg(f"\n{msg}")

        if caller.location:
            caller.location.msg_contents(f"\n{msg}", exclude=[caller])

        # Show results to player
        result_parts = [f"  XP: |c+{xp}|n"]
        if actual_delta > 0:
            result_parts.append(f"  Kayfabe: |g+{actual_delta}|n")
        elif actual_delta < 0:
            result_parts.append(f"  Kayfabe: |r{actual_delta}|n")

        # Level up check
        levels = check_level_up(caller)
        if levels > 0:
            result_parts.append(f"  |YLEVEL UP! Now level {caller.db.level}!|n")

        caller.msg("\n".join(result_parts))
