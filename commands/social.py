"""
Kayfabe: Protect the Business — Social commands.

Commands:
    who      - List all online players
    roster   - Show all players in a territory
    record   - View match history and record
    respond  - Respond to a backstage segment
"""

import time
from evennia.commands.command import Command
from commands.career import STAT_NAMES, RANK_COLORS


class CmdWho(Command):
    """
    List all connected players.

    Usage:
        who
        online

    Shows all currently online wrestlers with their territory,
    tier, rank, and alignment.
    """
    key = "who"
    aliases = ["online"]
    locks = "cmd:all()"
    help_category = "Social"

    def func(self):
        import evennia

        sessions = evennia.SESSION_HANDLER.get_sessions()
        wrestlers = []
        for sess in sessions:
            puppet = sess.get_puppet()
            if puppet and puppet.db.chargen_complete:
                wrestlers.append(puppet)

        # Deduplicate (multi-session)
        seen = set()
        unique = []
        for w in wrestlers:
            if w.id not in seen:
                seen.add(w.id)
                unique.append(w)

        if not unique:
            self.caller.msg("No wrestlers are currently online.")
            return

        msg = (
            f"\n|w{'=' * 54}|n\n"
            f"|w  WHO'S IN THE BUILDING|n\n"
            f"|w{'=' * 54}|n\n"
        )
        msg += f"  {'Name':20s} {'Territory':12s} {'Rank':16s} {'Align':10s}\n"
        msg += f"  {'-' * 20} {'-' * 12} {'-' * 16} {'-' * 10}\n"

        for w in unique:
            name = w.key[:20]
            territory = (w.db.territory or "???")[:12]
            rank = w.get_rank()
            rank_color = RANK_COLORS.get(rank, "|w")
            alignment = w.db.alignment or "???"
            if alignment == "Face":
                align_str = "|gFace|n"
            elif alignment == "Heel":
                align_str = "|rHeel|n"
            elif alignment == "Anti-Hero":
                align_str = "|yAnti-Hero|n"
            else:
                align_str = alignment
            msg += f"  {name:20s} {territory:12s} {rank_color}{rank:16s}|n {align_str}\n"

        msg += f"\n  |w{len(unique)}|n wrestler{'s' if len(unique) != 1 else ''} online.\n"
        msg += f"|w{'=' * 54}|n"
        self.caller.msg(msg)


class CmdRoster(Command):
    """
    View the roster of wrestlers in a territory.

    Usage:
        roster              - Show all players in your territory
        roster <territory>  - Show players in named territory

    Lists all player wrestlers (online and offline) present
    in the specified territory.
    """
    key = "roster"
    aliases = ["players"]
    locks = "cmd:all()"
    help_category = "Social"

    def func(self):
        from typeclasses.characters import Wrestler

        caller = self.caller
        args = self.args.strip().lower()

        territory = args if args else (caller.db.territory or "")
        if not territory:
            caller.msg("|rYou're not in a territory. Use: roster <territory>|n")
            return

        wrestlers = Wrestler.objects.filter(
            db_typeclass_path="typeclasses.characters.Wrestler"
        )

        roster = []
        for w in wrestlers:
            if not w.db.chargen_complete:
                continue
            w_terr = (w.db.territory or "").lower()
            if w_terr == territory:
                roster.append(w)

        if not roster:
            caller.msg(f"|rNo wrestlers found in '{territory}'.|n")
            return

        msg = (
            f"\n|w{'=' * 60}|n\n"
            f"|w  ROSTER — {territory.upper()}|n\n"
            f"|w{'=' * 60}|n\n"
        )
        msg += f"  {'Name':20s} {'Rank':16s} {'Align':10s} {'Record':10s} {'Status':8s}\n"
        msg += f"  {'-' * 20} {'-' * 16} {'-' * 10} {'-' * 10} {'-' * 8}\n"

        for w in roster:
            name = w.key[:20]
            rank = w.get_rank()
            rank_color = RANK_COLORS.get(rank, "|w")
            alignment = w.db.alignment or "???"
            if alignment == "Face":
                align_str = "|gFace|n"
            elif alignment == "Heel":
                align_str = "|rHeel|n"
            elif alignment == "Anti-Hero":
                align_str = "|yAnti-Hero|n"
            else:
                align_str = alignment[:10]

            wins = w.db.wins or 0
            losses = w.db.losses or 0
            draws = w.db.draws or 0
            record = f"{wins}-{losses}-{draws}"

            online = "|gON|n" if w.sessions.count() > 0 else "|xOFF|n"

            msg += f"  {name:20s} {rank_color}{rank:16s}|n {align_str:10s} {record:10s} {online}\n"

        msg += f"\n  |w{len(roster)}|n wrestler{'s' if len(roster) != 1 else ''} in {territory}.\n"
        msg += f"|w{'=' * 60}|n"
        caller.msg(msg)


class CmdRecord(Command):
    """
    View match history and career record.

    Usage:
        record          - Show your own record
        record <player> - Show another player's record

    Displays win-loss-draw record, average star rating, best match,
    top rivals, and recent match history.
    """
    key = "record"
    aliases = ["history", "matches"]
    locks = "cmd:all()"
    help_category = "Social"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if args:
            # Look up another player
            from evennia.utils.search import search_object
            results = search_object(args)
            target = None
            for r in results:
                if hasattr(r, 'db') and getattr(r.db, 'chargen_complete', False):
                    target = r
                    break
            if not target:
                caller.msg(f"|rCouldn't find wrestler '{args}'.|n")
                return
        else:
            target = caller

        if not target.db.chargen_complete:
            caller.msg("That character hasn't been created yet.")
            return

        wins = target.db.wins or 0
        losses = target.db.losses or 0
        draws = target.db.draws or 0
        total = target.db.matches_wrestled or 0
        avg_stars = target.get_match_quality_avg()
        best_stars = target.db.best_match_stars or 0.0
        best_opp = target.db.best_match_opponent or "N/A"
        rivals = target.db.rivals or {}

        msg = (
            f"\n|w{'=' * 50}|n\n"
            f"|w  CAREER RECORD — {target.key}|n\n"
            f"|w{'=' * 50}|n\n"
            f"  W-L-D:        |g{wins}|n-|r{losses}|n-|y{draws}|n\n"
            f"  Total Matches: {total}\n"
            f"  Avg Stars:     |y{'%.2f' % avg_stars}|n\n"
            f"  Best Match:    |y{'%.2f' % best_stars}|n stars vs |c{best_opp}|n\n"
        )

        # Top 3 rivals
        if rivals:
            sorted_rivals = sorted(rivals.items(), key=lambda x: x[1], reverse=True)[:3]
            msg += f"\n  |wTop Rivals:|n\n"
            for rname, count in sorted_rivals:
                msg += f"    |c{rname}|n — {count} match{'es' if count != 1 else ''}\n"

        # Recent match history (last 10)
        history = target.db.match_history or []
        if history:
            recent = history[-10:]
            recent.reverse()
            msg += f"\n  |wRecent Matches:|n\n"
            msg += f"  {'Opponent':20s} {'Result':6s} {'Stars':6s} {'Territory':12s}\n"
            msg += f"  {'-' * 20} {'-' * 6} {'-' * 6} {'-' * 12}\n"
            for m in recent:
                opp = m.get("opponent", "???")[:20]
                result = m.get("result", "???")
                if result == "win":
                    r_str = "|gW|n"
                elif result == "loss":
                    r_str = "|rL|n"
                else:
                    r_str = "|yD|n"
                stars = m.get("stars", 0.0)
                terr = m.get("territory", "???")[:12]
                msg += f"  {opp:20s} {r_str:6s}   {stars:4.2f}  {terr:12s}\n"

        msg += f"|w{'=' * 50}|n"
        caller.msg(msg)


class CmdSkipTutorial(Command):
    """
    Skip Learning the Ropes.

    Usage:
        skip

    Skips the guided tutorial match and moves on to picking
    your starting fed. Only works during the tutorial.
    """
    key = "skip"
    locks = "cmd:all()"
    help_category = "Social"

    def func(self):
        caller = self.caller
        if not caller.ndb.in_tutorial:
            caller.msg("There's no tutorial to skip.")
            return

        # Find and stop the tutorial script
        scripts = caller.scripts.all()
        for script in scripts:
            if script.key == "tutorial_match":
                script.skip_tutorial()
                return

        caller.ndb.in_tutorial = False
        caller.msg("|yTutorial skipped.|n")


class CmdRespond(Command):
    """
    Respond to a backstage segment.

    Usage:
        respond <number>

    When a backstage segment triggers (in locker rooms or bars),
    choose your response by entering the number.
    """
    key = "respond"
    aliases = ["choose"]
    locks = "cmd:all()"
    help_category = "Social"

    def func(self):
        caller = self.caller
        segment = caller.ndb.pending_backstage

        if not segment:
            caller.msg("There's nothing to respond to right now.")
            return

        args = self.args.strip()
        if not args:
            from world.backstage import format_segment_prompt
            caller.msg(format_segment_prompt(segment, caller))
            return

        try:
            choice_idx = int(args) - 1
        except ValueError:
            caller.msg("|rEnter a number to choose.|n")
            return

        from world.backstage import resolve_backstage_choice
        msg, effects = resolve_backstage_choice(caller, segment, choice_idx)

        if msg == "Invalid choice.":
            num_choices = len(segment.get("choices", []))
            caller.msg(f"|rInvalid choice. Pick 1-{num_choices}.|n")
            return

        caller.msg(f"\n{msg}\n")
        caller.ndb.pending_backstage = None
