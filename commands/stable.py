"""
Kayfabe: Protect the Business — Stable/Faction commands.

Commands:
    stable           - View your stable
    stable list      - List all stables
    stable create    - Create a new stable ($500)
    stable invite    - Invite a player (leader only)
    stable join      - Accept an invitation
    stable leave     - Leave your stable (leader leaving disbands)
    stable kick      - Remove a member (leader only)

Benefits:
    +2 all stats in tag team with stable mate
    +10% merch per member
    Promo intimidation bonus
"""

from evennia.commands.command import Command
from evennia.utils.search import search_object


def _get_registry():
    """Get or create the StableRegistryScript."""
    from evennia.scripts.models import ScriptDB
    try:
        registry = ScriptDB.objects.get(db_key="stable_registry")
        return registry
    except ScriptDB.DoesNotExist:
        from typeclasses.scripts import StableRegistryScript
        registry = StableRegistryScript.objects.create(db_key="stable_registry")
        registry.db.stables = {}
        return registry
    except ScriptDB.MultipleObjectsReturned:
        return ScriptDB.objects.filter(db_key="stable_registry").first()


class CmdStable(Command):
    """
    Manage your wrestling stable (faction).

    Usage:
        stable                - View your stable info
        stable list           - List all stables
        stable create <name>  - Create a new stable ($500)
        stable invite <player>- Invite a player (leader only)
        stable join <name>    - Join a stable you've been invited to
        stable leave          - Leave your stable
        stable kick <player>  - Remove a member (leader only)

    Stables give bonuses: +2 stats in tag matches with stable mates,
    +10% merch per member, promo intimidation bonus.
    Max 5 members per stable.
    """
    key = "stable"
    aliases = ["faction"]
    locks = "cmd:all()"
    help_category = "Social"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            self._view_stable(caller)
            return

        parts = args.split(None, 1)
        subcmd = parts[0].lower()
        subarg = parts[1].strip() if len(parts) > 1 else ""

        if subcmd == "list":
            self._list_stables(caller)
        elif subcmd == "create":
            self._create_stable(caller, subarg)
        elif subcmd == "invite":
            self._invite_player(caller, subarg)
        elif subcmd == "join":
            self._join_stable(caller, subarg)
        elif subcmd == "leave":
            self._leave_stable(caller)
        elif subcmd == "kick":
            self._kick_player(caller, subarg)
        else:
            caller.msg(
                "|wUsage:|n stable [list|create|invite|join|leave|kick] [arg]\n"
                "Type |whelp stable|n for details."
            )

    def _view_stable(self, caller):
        stable_name = caller.db.stable or ""
        if not stable_name:
            caller.msg(
                "You're not in a stable.\n"
                "Use |wstable create <name>|n to start one, or "
                "|wstable join <name>|n to join one."
            )
            return

        registry = _get_registry()
        stables = registry.db.stables or {}
        info = stables.get(stable_name)
        if not info:
            caller.msg(f"|rStable '{stable_name}' not found in registry.|n")
            caller.db.stable = ""
            return

        msg = (
            f"\n|w{'=' * 44}|n\n"
            f"|w  {stable_name}|n\n"
            f"|w{'=' * 44}|n\n"
            f"  Leader:    |c{info['leader']}|n\n"
            f"  Territory: |c{info.get('territory', 'N/A')}|n\n"
            f"  Alignment: |c{info.get('alignment', 'Mixed')}|n\n"
            f"  Members:   {len(info['members'])}/5\n\n"
        )
        for m in info["members"]:
            is_leader = " |y(Leader)|n" if m == info["leader"] else ""
            msg += f"    |c{m}|n{is_leader}\n"

        # Show bonuses
        member_count = len(info["members"])
        merch_bonus = member_count * 10
        msg += (
            f"\n  |wBonuses:|n\n"
            f"    +2 all stats in tag matches with stable mates\n"
            f"    +{merch_bonus}% merch income bonus\n"
            f"    Promo intimidation bonus\n"
        )

        # Show pending invites
        invites = info.get("invites", [])
        if invites and caller.key == info["leader"]:
            msg += f"\n  |wPending Invites:|n {', '.join(invites)}\n"

        msg += f"|w{'=' * 44}|n"
        caller.msg(msg)

    def _list_stables(self, caller):
        registry = _get_registry()
        stables = registry.db.stables or {}

        if not stables:
            caller.msg("No stables have been formed yet.")
            return

        msg = (
            f"\n|w{'=' * 50}|n\n"
            f"|w  ALL STABLES|n\n"
            f"|w{'=' * 50}|n\n"
            f"  {'Name':20s} {'Leader':15s} {'Members':8s} {'Territory':12s}\n"
            f"  {'-' * 20} {'-' * 15} {'-' * 8} {'-' * 12}\n"
        )

        for name, info in stables.items():
            leader = info["leader"][:15]
            count = f"{len(info['members'])}/5"
            territory = info.get("territory", "???")[:12]
            msg += f"  {name:20s} {leader:15s} {count:8s} {territory:12s}\n"

        msg += f"|w{'=' * 50}|n"
        caller.msg(msg)

    def _create_stable(self, caller, name):
        if not name:
            caller.msg("|rUsage: stable create <name>|n")
            return

        if len(name) > 30:
            caller.msg("|rStable name must be 30 characters or less.|n")
            return

        if caller.db.stable:
            caller.msg(f"|rYou're already in '{caller.db.stable}'. Leave first.|n")
            return

        money = caller.db.money or 0
        if money < 500:
            caller.msg(f"|rCreating a stable costs $500. You have ${money}.|n")
            return

        registry = _get_registry()
        stables = registry.db.stables or {}

        if name in stables:
            caller.msg(f"|rA stable named '{name}' already exists.|n")
            return

        caller.db.money = money - 500
        stables[name] = {
            "leader": caller.key,
            "members": [caller.key],
            "territory": caller.db.territory or "",
            "alignment": caller.db.alignment or "Mixed",
            "invites": [],
        }
        registry.db.stables = stables
        caller.db.stable = name

        # Dirt sheet: log stable formation
        from world.dirtsheet import log_event
        log_event("stable", action="formed", name=name, leader=caller.key)

        caller.msg(
            f"|g*** {name} HAS BEEN FORMED ***|n\n"
            f"You are the leader. Use |wstable invite <player>|n to recruit.\n"
            f"Cost: |r-$500|n. Balance: |y${caller.db.money}|n"
        )
        if caller.location:
            caller.location.msg_contents(
                f"|w{caller.key} has formed a new stable: |c{name}|w!|n",
                exclude=[caller],
            )

    def _invite_player(self, caller, target_name):
        if not target_name:
            caller.msg("|rUsage: stable invite <player>|n")
            return

        stable_name = caller.db.stable or ""
        if not stable_name:
            caller.msg("|rYou're not in a stable.|n")
            return

        registry = _get_registry()
        stables = registry.db.stables or {}
        info = stables.get(stable_name)
        if not info:
            caller.msg("|rStable not found.|n")
            return

        if info["leader"] != caller.key:
            caller.msg("|rOnly the stable leader can invite members.|n")
            return

        if len(info["members"]) >= 5:
            caller.msg("|rStable is full (max 5 members).|n")
            return

        # Find target
        results = search_object(target_name)
        target = None
        for r in results:
            if hasattr(r, 'db') and getattr(r.db, 'chargen_complete', False):
                target = r
                break
        if not target:
            caller.msg(f"|rCouldn't find wrestler '{target_name}'.|n")
            return

        if target.db.stable:
            caller.msg(f"|r{target.key} is already in a stable.|n")
            return

        invites = info.get("invites", [])
        if target.key in invites:
            caller.msg(f"|r{target.key} already has a pending invite.|n")
            return

        invites.append(target.key)
        info["invites"] = invites
        stables[stable_name] = info
        registry.db.stables = stables

        caller.msg(f"|gInvited |c{target.key}|g to {stable_name}.|n")
        if target.sessions.count():
            target.msg(
                f"|y{caller.key} has invited you to join |c{stable_name}|y!|n\n"
                f"Type |wstable join {stable_name}|n to accept."
            )

    def _join_stable(self, caller, stable_name):
        if not stable_name:
            caller.msg("|rUsage: stable join <name>|n")
            return

        if caller.db.stable:
            caller.msg(f"|rYou're already in '{caller.db.stable}'. Leave first.|n")
            return

        registry = _get_registry()
        stables = registry.db.stables or {}
        info = stables.get(stable_name)
        if not info:
            caller.msg(f"|rStable '{stable_name}' not found.|n")
            return

        invites = info.get("invites", [])
        if caller.key not in invites:
            caller.msg(f"|rYou don't have an invitation to {stable_name}.|n")
            return

        if len(info["members"]) >= 5:
            caller.msg("|rStable is full (max 5 members).|n")
            return

        invites.remove(caller.key)
        info["invites"] = invites
        info["members"].append(caller.key)
        stables[stable_name] = info
        registry.db.stables = stables
        caller.db.stable = stable_name

        caller.msg(f"|gYou have joined |c{stable_name}|g!|n")
        # Notify stable members
        for m_name in info["members"]:
            if m_name != caller.key:
                results = search_object(m_name)
                for r in results:
                    if hasattr(r, 'sessions') and r.sessions.count():
                        r.msg(f"|c{caller.key}|w has joined {stable_name}!|n")

    def _leave_stable(self, caller):
        stable_name = caller.db.stable or ""
        if not stable_name:
            caller.msg("|rYou're not in a stable.|n")
            return

        registry = _get_registry()
        stables = registry.db.stables or {}
        info = stables.get(stable_name)
        if not info:
            caller.db.stable = ""
            caller.msg("|rStable not found. Cleared your membership.|n")
            return

        if info["leader"] == caller.key:
            # Leader leaving disbands the stable
            for m_name in info["members"]:
                results = search_object(m_name)
                for r in results:
                    if hasattr(r, 'db'):
                        r.db.stable = ""
                    if hasattr(r, 'sessions') and r.sessions.count() and r.key != caller.key:
                        r.msg(
                            f"|r{caller.key} has disbanded {stable_name}!|n"
                        )
            del stables[stable_name]
            registry.db.stables = stables
            caller.db.stable = ""
            # Dirt sheet: log stable disbanding
            from world.dirtsheet import log_event
            log_event("stable", action="disbanded", name=stable_name, leader=caller.key)
            caller.msg(f"|rYou disbanded {stable_name}.|n")
        else:
            info["members"].remove(caller.key)
            stables[stable_name] = info
            registry.db.stables = stables
            caller.db.stable = ""
            caller.msg(f"|yYou left {stable_name}.|n")
            # Notify
            for m_name in info["members"]:
                results = search_object(m_name)
                for r in results:
                    if hasattr(r, 'sessions') and r.sessions.count():
                        r.msg(f"|y{caller.key} has left {stable_name}.|n")

    def _kick_player(self, caller, target_name):
        if not target_name:
            caller.msg("|rUsage: stable kick <player>|n")
            return

        stable_name = caller.db.stable or ""
        if not stable_name:
            caller.msg("|rYou're not in a stable.|n")
            return

        registry = _get_registry()
        stables = registry.db.stables or {}
        info = stables.get(stable_name)
        if not info:
            caller.msg("|rStable not found.|n")
            return

        if info["leader"] != caller.key:
            caller.msg("|rOnly the stable leader can kick members.|n")
            return

        # Find exact match in members
        target_key = None
        for m in info["members"]:
            if m.lower() == target_name.lower():
                target_key = m
                break

        if not target_key:
            caller.msg(f"|r'{target_name}' is not in your stable.|n")
            return

        if target_key == caller.key:
            caller.msg("|rYou can't kick yourself. Use |wstable leave|r to disband.|n")
            return

        info["members"].remove(target_key)
        stables[stable_name] = info
        registry.db.stables = stables

        # Clear kicked player's stable
        results = search_object(target_key)
        for r in results:
            if hasattr(r, 'db'):
                r.db.stable = ""
            if hasattr(r, 'sessions') and r.sessions.count():
                r.msg(f"|rYou have been kicked from {stable_name} by {caller.key}!|n")

        caller.msg(f"|yKicked |c{target_key}|y from {stable_name}.|n")
