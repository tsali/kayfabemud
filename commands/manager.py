"""
Kayfabe: Protect the Business — Manager commands.

hire <manager>      — hire a manager
fire                — fire your current manager
manager promo       — let your manager cut a promo for you
manager interfere   — signal your manager to interfere (heel only)
"""

from evennia.commands.command import Command


class CmdHire(Command):
    """
    Hire a manager.

    Usage:
      hire <manager>

    The manager must be in the same room and available.
    Managers charge a weekly retainer plus a cut of match payoffs.
    """

    key = "hire"
    locks = "cmd:all()"
    help_category = "Career"

    def func(self):
        caller = self.caller
        if not caller.db.chargen_complete:
            caller.msg("Finish character creation first.")
            return

        if not self.args:
            caller.msg("Usage: hire <manager name>")
            return

        # Check if already has a manager
        if caller.db.manager:
            caller.msg(
                f"You already have a manager ({caller.db.manager_name}). "
                f"Type |wfire|n first."
            )
            return

        target = caller.search(self.args.strip(), location=caller.location)
        if not target:
            return

        from typeclasses.npcs import NPCManager
        if not isinstance(target, NPCManager):
            caller.msg(f"{target.key} isn't a manager you can hire.")
            return

        if not target.db.available:
            caller.msg(f"{target.key} is already managing someone else.")
            return

        # Check alignment compatibility
        mgr_align = target.db.alignment
        char_align = caller.db.alignment

        if mgr_align == "Face" and char_align == "Heel":
            caller.msg(f"{target.key} won't work with a heel. They have standards.")
            return
        if mgr_align == "Heel" and char_align == "Face":
            # Some heel managers will work with faces for money, but warn
            caller.msg(
                f"|y{target.key} raises an eyebrow. 'A face? Fine. "
                f"But don't expect me to play nice.'|n"
            )

        # Check cost
        retainer = target.db.retainer_cost or 100
        if (caller.db.money or 0) < retainer:
            caller.msg(
                f"{target.key} wants ${retainer} retainer up front. "
                f"You have ${caller.db.money or 0}."
            )
            return

        # Hire
        caller.db.money -= retainer
        caller.db.manager = target
        caller.db.manager_name = target.key
        target.db.managed_wrestler = caller
        target.db.available = False

        cha_bonus = target.get_cha_bonus()
        psy_bonus = target.get_psy_bonus()

        caller.msg(
            f"\n|Y*** MANAGER HIRED ***|n\n"
            f"|w{target.key}|n is now your manager!\n"
            f"  Retainer: |y${retainer}|n/week\n"
            f"  Cut: |y{target.db.cut_percent}%|n of match payoffs\n"
            f"  CHA Bonus: |g+{cha_bonus}|n\n"
            f"  PSY Bonus: |g+{psy_bonus}|n\n"
            f"  Style: |c{target.db.style}|n\n"
        )

        if caller.location:
            caller.location.msg_contents(
                f"|w{caller.key} has hired {target.key} as their manager!|n",
                exclude=[caller],
            )


class CmdFire(Command):
    """
    Fire your current manager.

    Usage:
      fire

    Firing a manager publicly can generate a storyline.
    """

    key = "fire"
    aliases = ["fire manager"]
    locks = "cmd:all()"
    help_category = "Career"

    def func(self):
        caller = self.caller
        manager = caller.db.manager

        if not manager:
            caller.msg("You don't have a manager to fire.")
            return

        mgr_name = caller.db.manager_name or "your manager"

        # Release the manager
        if hasattr(manager, 'db'):
            manager.db.managed_wrestler = None
            manager.db.available = True

        caller.db.manager = None
        caller.db.manager_name = ""

        # Public firing generates heat
        if caller.location:
            from world.rules import kayfabe_change
            actual = kayfabe_change(caller, 2, "public manager firing")
            caller.msg(
                f"\n|Y*** MANAGER FIRED ***|n\n"
                f"You've released {mgr_name}!\n"
                f"|gKayfabe +{actual}|n (public firing generates heat)\n"
            )
            caller.location.msg_contents(
                f"|w{caller.key} just FIRED {mgr_name}! "
                f"The crowd gasps!|n",
                exclude=[caller],
            )
        else:
            caller.msg(f"You've released {mgr_name}.")


class CmdManagerPromo(Command):
    """
    Have your manager cut a promo on your behalf.

    Usage:
      manager promo

    Uses your manager's CHA instead of yours.
    Great if you're a strong in-ring worker but weak on the mic.
    """

    key = "manager promo"
    aliases = ["mpromo"]
    locks = "cmd:all()"
    help_category = "Career"

    def func(self):
        caller = self.caller
        if not caller.db.chargen_complete:
            caller.msg("Finish character creation first.")
            return

        if caller.scripts.get("match_script"):
            caller.msg("You're in a match. Focus on the ring work.")
            return

        manager = caller.db.manager
        if not manager:
            caller.msg("You don't have a manager. Hire one first.")
            return

        if not hasattr(manager, 'cut_promo_for'):
            caller.msg("Your manager can't cut promos (error).")
            return

        xp, quality = manager.cut_promo_for(caller)
        caller.db.xp = (caller.db.xp or 0) + xp
        caller.msg(f"  XP: +{xp}")

        from world.rules import check_level_up
        levels = check_level_up(caller)
        if levels > 0:
            caller.msg(f"|YLEVEL UP! Now level {caller.db.level}!|n")


class CmdManagerInterfere(Command):
    """
    Signal your manager to interfere in a match.

    Usage:
      manager interfere

    Heel managers only. Risk of getting caught (DQ).
    If successful, deals damage to your opponent.
    """

    key = "manager interfere"
    aliases = ["minterfere"]
    locks = "cmd:all()"
    help_category = "Career"

    def func(self):
        caller = self.caller
        scripts = caller.scripts.get("match_script")
        if not scripts:
            caller.msg("You're not in a match.")
            return
        script = scripts[0]

        manager = caller.db.manager
        if not manager:
            caller.msg("You don't have a manager at ringside.")
            return

        if not hasattr(manager, 'attempt_interference'):
            caller.msg("Your manager can't interfere (error).")
            return

        success, msg = manager.attempt_interference(script, is_helping_a=True)
        caller.msg(f"\n{msg}")
        if caller.location:
            caller.location.msg_contents(f"\n{msg}", exclude=[caller])

        if not success:
            # Risk of DQ — crowd heat drops
            script.db.crowd_heat = max(0, script.db.crowd_heat - 5)
            caller.msg("|rThe referee is watching your manager closely now!|n")
