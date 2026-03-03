"""
Kayfabe: Protect the Business — Wrestling match commands.

wrestle <target> — start a match against an NPC
work [move]       — execute a wrestling move during a match
sell              — sell for your opponent (let them do a move)
comeback          — attempt a comeback (during comeback phase)
finish            — attempt your finishing move
kickout           — kick out of a pin attempt
card              — show tonight's match card (who's in the building)
"""

import random
from evennia.commands.command import Command
from evennia.utils.create import create_script
from commands.command import pause_then_look


def _check_tutorial(caller, command_name):
    """
    Check if player is in tutorial mode and forward command.
    Returns True if tutorial handled the command (caller should return).
    """
    if not getattr(caller.ndb, 'in_tutorial', False):
        return False
    scripts = caller.scripts.all()
    for script in scripts:
        if script.key == "tutorial_match":
            script.process_command(command_name)
            return True
    # Tutorial flag set but no script found — clean up
    caller.ndb.in_tutorial = False
    return False


class CmdWrestle(Command):
    """
    Start a wrestling match against an NPC.

    Usage:
      wrestle <target>

    Challenges an NPC wrestler in the same room to a match.
    The match plays out in phases — use work, sell, comeback,
    and finish commands during the match.
    """

    key = "wrestle"
    aliases = ["challenge_npc", "match"]
    locks = "cmd:all()"
    help_category = "Wrestling"

    def func(self):
        caller = self.caller
        if not caller.db.chargen_complete:
            caller.msg("You need to finish character creation first.")
            return

        # Check if already in a match
        if caller.scripts.get("match_script"):
            caller.msg("You're already in a match! Finish it first.")
            return

        if not self.args:
            caller.msg("Usage: wrestle <target>")
            return

        target = caller.search(self.args.strip(), location=caller.location)
        if not target:
            return

        # Check target is an NPC wrestler
        from typeclasses.npcs import NPCWrestler, BackyardNPC
        if not isinstance(target, (NPCWrestler, BackyardNPC)):
            caller.msg(f"{target.key} isn't a wrestler you can challenge.")
            return

        # Check target role
        if hasattr(target.db, 'role') and target.db.role in ("trainer", "announcer", "authority"):
            caller.msg(f"{target.key} is a {target.db.role}, not available for a match right now.")
            return

        # Determine booking (player usually wins at lower tiers)
        tier = caller.db.tier or 1
        player_level = caller.db.level or 1
        npc_level = target.db.level or 1

        if tier <= 2:
            win_chance = 0.7  # backyard/training, player wins most
        elif player_level >= npc_level:
            win_chance = 0.6
        else:
            win_chance = 0.4

        booked_winner = "a" if random.random() < win_chance else "b"

        # Create the match script
        script = create_script(
            "typeclasses.scripts.MatchScript",
            key="match_script",
            obj=caller,
        )
        script.setup_match(caller, target, booked_winner=booked_winner)

        # Announce
        caller.msg(
            f"\n|w{'=' * 44}|n\n"
            f"|w  MATCH: {caller.key} vs {target.key}|n\n"
            f"|w{'=' * 44}|n\n"
            f"The bell rings!\n"
        )

        if caller.location:
            caller.location.msg_contents(
                f"\n|w*** MATCH: {caller.key} vs {target.key} ***|n\n"
                f"The bell rings!",
                exclude=[caller],
            )

        # Show first phase
        script.announce_phase()


class CmdWork(Command):
    """
    Execute a wrestling move during a match.

    Usage:
      work             — auto-select a move for the current phase
      work <move name> — attempt a specific move

    Available moves depend on the current match phase.
    Type 'moves' to see available moves.
    """

    key = "work"
    aliases = ["move", "hit"]
    locks = "cmd:all()"
    help_category = "Wrestling"

    def func(self):
        caller = self.caller

        if _check_tutorial(caller, "work"):
            return

        scripts = caller.scripts.get("match_script")
        if not scripts:
            caller.msg("You're not in a match.")
            return
        script = scripts[0]

        if script.db.match_over:
            caller.msg("The match is over.")
            return

        if script.db.pending_pin:
            caller.msg("|rYou're being pinned! Type |wkickout|r to kick out!|n")
            return

        from world.moves import MOVES, get_moves_for_phase

        phase = script.current_phase()
        valid_keys = get_moves_for_phase(phase)

        if self.args:
            # Try to find the named move
            search = self.args.strip().lower().replace(" ", "_")
            move_data = MOVES.get(search)
            if not move_data:
                # Fuzzy search
                for k, v in MOVES.items():
                    if search in v["name"].lower().replace(" ", "_") or search in k:
                        move_data = v
                        break
            if not move_data:
                caller.msg(f"Unknown move '{self.args.strip()}'. Type |wmoves|n to see options.")
                return
        else:
            # Auto-select a move for the phase (skip learned_only moves player hasn't learned)
            known = caller.db.known_moves or []
            available = [k for k in valid_keys
                         if not MOVES[k].get("learned_only") or k in known]
            if not available:
                available = [k for k in list(MOVES.keys())[:5]
                             if not MOVES[k].get("learned_only") or k in known]
            if not available:
                available = list(MOVES.keys())[:5]
            move_key = random.choice(available)
            move_data = MOVES[move_key]

        # Check alignment restrictions
        if move_data.get("heel_only") and caller.db.alignment == "Face":
            caller.msg("That's a dirty tactic! Faces can't do that without breaking kayfabe.")
            return
        if move_data.get("face_only") and caller.db.alignment == "Heel":
            caller.msg("That's a babyface move. Heels don't rally the crowd.")
            return

        # Check learned_only moves require knowing them
        if move_data.get("learned_only"):
            known = caller.db.known_moves or []
            # Find the key for this move_data
            move_key = None
            for k, v in MOVES.items():
                if v is move_data:
                    move_key = k
                    break
            if move_key and move_key not in known:
                caller.msg(
                    f"|rYou haven't learned {move_data['name']} yet.\n"
                    f"Find a veteran who knows it and use |wlearn|r to study under them.|n"
                )
                return

        # Execute
        success, damage, msg = script.execute_move(caller, move_data, is_player_a=True)
        caller.msg(f"\n|w>> YOUR OFFENSE:|n {msg}")
        if caller.location:
            caller.location.msg_contents(f"\n{msg}", exclude=[caller])

        # Check for phase advance and show status
        _check_advance(script, caller)
        if not script.db.match_over:
            script._show_status(caller)


class CmdSell(Command):
    """
    Sell for your opponent — let them execute a move on you.

    Usage:
      sell

    Good selling makes the match better. It increases crowd heat
    and contributes to a higher star rating. Essential during the
    heat segment.
    """

    key = "sell"
    locks = "cmd:all()"
    help_category = "Wrestling"

    def func(self):
        caller = self.caller

        if _check_tutorial(caller, "sell"):
            return

        scripts = caller.scripts.get("match_script")
        if not scripts:
            caller.msg("You're not in a match.")
            return
        script = scripts[0]

        if script.db.match_over:
            caller.msg("The match is over.")
            return

        if script.db.pending_pin:
            caller.msg("|rYou're being pinned! Type |wkickout|r to kick out!|n")
            return

        npc = script.db.wrestler_b
        npc_name = npc.key if npc else "Your opponent"
        msg = script.do_sell(is_player_a=True)
        caller.msg(f"\n|r>> YOU SELL:|n You let {npc_name} take control --")
        caller.msg(f"{msg}")
        caller.msg("|xGood selling builds crowd heat and star ratings.|n")
        if caller.location:
            caller.location.msg_contents(f"\n{msg}", exclude=[caller])

        _check_advance(script, caller)
        if not script.db.match_over:
            script._show_status(caller)


class CmdComeback(Command):
    """
    Fire up your comeback — the crowd moment.

    Usage:
      comeback

    Best used during the comeback phase. Uses CHA + crowd heat.
    Success builds massive momentum for the finish.
    """

    key = "comeback"
    aliases = ["fireup", "hulkup"]
    locks = "cmd:all()"
    help_category = "Wrestling"

    def func(self):
        caller = self.caller

        if _check_tutorial(caller, "comeback"):
            return

        scripts = caller.scripts.get("match_script")
        if not scripts:
            caller.msg("You're not in a match.")
            return
        script = scripts[0]

        if script.db.match_over:
            caller.msg("The match is over.")
            return

        phase = script.current_phase()
        if phase not in ("comeback", "finish"):
            caller.msg("It's not time for the comeback yet. Build to it.")
            return

        success, msg = script.do_comeback(is_player_a=True)
        caller.msg(f"\n|g>> COMEBACK!|n {msg}")
        if caller.location:
            caller.location.msg_contents(f"\n{msg}", exclude=[caller])

        if success and phase == "comeback":
            # Advance to finish
            script.advance_phase()
        elif not script.db.match_over:
            script._show_status(caller)


class CmdFinish(Command):
    """
    Attempt your finishing move!

    Usage:
      finish

    Go for the pin with your finisher. Best saved for the finish
    phase when your opponent is worn down and momentum is high.
    If it fails, you get a dramatic near-fall.
    """

    key = "finish"
    aliases = ["finisher", "pin"]
    locks = "cmd:all()"
    help_category = "Wrestling"

    def func(self):
        caller = self.caller

        if _check_tutorial(caller, "finish"):
            return

        scripts = caller.scripts.get("match_script")
        if not scripts:
            caller.msg("You're not in a match.")
            return
        script = scripts[0]

        if script.db.match_over:
            caller.msg("The match is over.")
            return

        phase = script.current_phase()
        if phase not in ("comeback", "finish"):
            caller.msg("Too early for the finisher! The crowd isn't ready.")
            return

        success, msg = script.attempt_finisher(is_player_a=True)
        caller.msg(f"\n{msg}")
        if caller.location:
            caller.location.msg_contents(f"\n{msg}", exclude=[caller])

        if success:
            _end_match(script, caller)
        elif phase == "comeback":
            # Failed finisher in comeback — advance to finish phase
            script.advance_phase()
        elif not script.db.match_over:
            script._show_status(caller)


class CmdKickout(Command):
    """
    Kick out of a pin attempt.

    Usage:
      kickout

    When the opponent has you pinned, try to kick out.
    Uses Toughness. Harder when you're beaten down.
    Only available when you're being pinned.
    """

    key = "kickout"
    aliases = ["ko"]
    locks = "cmd:all()"
    help_category = "Wrestling"

    def func(self):
        caller = self.caller
        scripts = caller.scripts.get("match_script")
        if not scripts:
            caller.msg("You're not in a match.")
            return
        script = scripts[0]

        if not script.db.pending_pin:
            caller.msg("Nobody is pinning you right now.")
            return

        success, msg = script.do_kickout(is_player_a=True)
        caller.msg(f"\n{msg}")
        if caller.location:
            caller.location.msg_contents(f"\n{msg}", exclude=[caller])

        script.db.pending_pin = False

        if not success:
            # Failed kickout means the NPC wins
            npc = script.db.wrestler_b
            npc_name = npc.key if npc else "opponent"
            finisher = npc.db.finisher_name if npc else "finisher"
            caller.msg(
                f"\n|r*** {npc_name} WINS with the {finisher}! ***|n"
            )
            script.db.match_over = True
            script.db.winner = "b"
            _end_match(script, caller)
        else:
            if not script.db.match_over:
                script._show_status(caller)


class CmdMoves(Command):
    """
    List available wrestling moves.

    Usage:
      moves          — show moves for current match phase
      moves all      — show all moves
    """

    key = "moves"
    aliases = ["movelist"]
    locks = "cmd:all()"
    help_category = "Wrestling"

    def func(self):
        from world.moves import MOVES, get_moves_for_phase

        caller = self.caller
        show_all = self.args and "all" in self.args.lower()

        scripts = caller.scripts.get("match_script")
        if scripts and not show_all:
            phase = scripts[0].current_phase()
            valid = get_moves_for_phase(phase)
            caller.msg(f"\n|wMoves available in {phase} phase:|n")
        else:
            valid = list(MOVES.keys())
            caller.msg(f"\n|wAll wrestling moves:|n")

        known = caller.db.known_moves or []
        for key in sorted(valid):
            m = MOVES[key]
            tags = ""
            if m.get("heel_only"):
                tags += " |r[Heel]|n"
            elif m.get("face_only"):
                tags += " |g[Face]|n"
            if m.get("learned_only"):
                if key in known:
                    tags += " |g[KNOWN]|n"
                else:
                    tags += " |x[LOCKED]|n"
            caller.msg(
                f"  |c{m['name']:25s}|n  {m['type']:10s}  "
                f"Diff:{m['difficulty']}  Dmg:{m['damage']}{tags}"
            )
        caller.msg(f"\n|wUsage: |cwork <move name>|n to use a specific move.")
        locked_count = sum(1 for k in valid if MOVES[k].get("learned_only") and k not in known)
        if locked_count:
            caller.msg(f"|x{locked_count} locked move{'s' if locked_count != 1 else ''} — use |wlearn|x near a veteran to unlock.|n")


class CmdCard(Command):
    """
    See who's in the building — available opponents.

    Usage:
      card
    """

    key = "card"
    aliases = ["opponents"]
    locks = "cmd:all()"
    help_category = "Wrestling"

    def func(self):
        caller = self.caller
        from typeclasses.npcs import NPCWrestler, BackyardNPC

        location = caller.location
        if not location:
            caller.msg("You're nowhere.")
            return

        npcs = [
            obj for obj in location.contents
            if isinstance(obj, (NPCWrestler, BackyardNPC))
            and obj != caller
            and getattr(obj.db, 'role', 'wrestler') not in ('announcer',)
        ]

        if not npcs:
            caller.msg("No wrestlers here to challenge.")
            return

        caller.msg(f"\n|wWrestlers at {location.key}:|n")
        for npc in npcs:
            align = npc.db.alignment or "?"
            level = npc.db.level or 1
            role = npc.db.role or "wrestler"
            finisher = npc.db.finisher_name or "Unknown"
            gender = getattr(npc.db, 'gender', 'Male') or "Male"

            if align == "Face":
                a_tag = "|g[Face]|n"
            elif align == "Heel":
                a_tag = "|r[Heel]|n"
            elif align == "Anti-Hero":
                a_tag = "|y[Anti-Hero]|n"
            else:
                a_tag = ""

            # Division tag
            if gender == "Male":
                d_tag = " |w[M]|n"
            elif gender == "Female":
                d_tag = " |m[W]|n"
            else:
                d_tag = ""

            role_tag = ""
            if role == "trainer":
                role_tag = " |m[Trainer]|n"

            caller.msg(
                f"  |c{npc.key}|n {a_tag}{d_tag}{role_tag}\n"
                f"    Level {level} — Finisher: {finisher}"
            )
        caller.msg(f"\n|wAnyone can challenge anyone.|n")
        caller.msg(f"|wType 'wrestle <name>' to start a match.|n")
        pause_then_look(caller)


class CmdHope(Command):
    """
    Attempt a brief hope spot during the heat segment.

    Usage:
      hope

    A brief flurry of offense that the heel cuts off.
    Builds crowd anticipation for the real comeback.
    """

    key = "hope"
    locks = "cmd:all()"
    help_category = "Wrestling"

    def func(self):
        caller = self.caller

        if _check_tutorial(caller, "hope"):
            return

        scripts = caller.scripts.get("match_script")
        if not scripts:
            caller.msg("You're not in a match.")
            return
        script = scripts[0]

        phase = script.current_phase()
        if phase not in ("heat", "hope"):
            caller.msg("Hope spots work best during the heat segment.")
            return

        from world.rules import stat_check
        cha = caller.get_stat("cha")
        success, roll, total, margin = stat_check(cha, 13)

        npc = script.db.wrestler_b
        npc_name = npc.key if npc else "your opponent"
        if success:
            script.db.crowd_heat = min(100, script.db.crowd_heat + 4)
            script.db.a_momentum += 2
            caller.msg(
                f"\n|y>> HOPE SPOT:|n You fire back with a flurry! The crowd stirs--\n"
                f"but {npc_name} cuts you off! Not yet... but the crowd FELT that!"
            )
        else:
            caller.msg(
                f"\n|x>> HOPE SPOT:|n You try to fight back but {npc_name} shuts you down."
            )

        script.db.move_count += 1
        _check_advance(script, caller)
        if not script.db.match_over:
            script._show_status(caller)


def _check_advance(script, caller):
    """Check if the match should advance to the next phase based on move count."""
    phase = script.current_phase()
    mc = script.db.move_count

    # Phase thresholds based on total move count
    advance_at = {
        "opening": 4,
        "heat": 9,
        "hope": 11,
        "comeback": 15,
        "finish": 999,  # finish doesn't auto-advance
    }

    threshold = advance_at.get(phase, 999)
    if mc >= threshold:
        if script.db.phase_index < 4:  # don't go past finish
            script.advance_phase()

    # Finish phase: check for pin opportunities
    if phase == "finish":
        if script.db.b_health <= 0:
            # NPC is done, prompt player to finish
            npc = script.db.wrestler_b
            npc_name = npc.key if npc else "Your opponent"
            caller.msg(
                f"\n|Y{npc_name} is barely standing! "
                f"NOW is the time -- type |wfinish|Y to hit your finisher!|n"
            )
        elif script.db.a_health <= 30 and not script.db.pending_pin:
            # NPC goes for a pin attempt -- player must kickout
            npc = script.db.wrestler_b
            npc_name = npc.key if npc else "opponent"
            finisher = npc.db.finisher_name if npc else "finishing move"
            script.db.pending_pin = True
            caller.msg(
                f"\n|r{npc_name} hits the {finisher}! COVER!\n"
                f"ONE... TWO...\n"
                f"Type |wkickout|r NOW to kick out!|n"
            )
            if caller.location:
                caller.location.msg_contents(
                    f"\n|r{npc_name} goes for the pin on {caller.key}!|n",
                    exclude=[caller],
                )


def _npc_finishes(script, caller):
    """NPC hits their finisher on the player (no kickout chance)."""
    npc = script.db.wrestler_b
    if not npc:
        return
    finisher = npc.db.finisher_name or "finishing move"

    caller.msg(
        f"\n|r{npc.key} hits the {finisher}!!!\n"
        f"COVER! ONE! TWO! THREE!!!\n\n"
        f"*** {npc.key} WINS! ***|n"
    )
    if caller.location:
        caller.location.msg_contents(
            f"\n|r*** {npc.key} defeats {caller.key} with the {finisher}! ***|n",
            exclude=[caller],
        )

    script.db.match_over = True
    script.db.winner = "b"
    script.db.pending_pin = False
    _end_match(script, caller)


def _end_match(script, caller):
    """End the match, show results, clean up."""
    stars, payoff, xp, summary = script.end_match()
    caller.msg(summary)
    if caller.location:
        from world.rules import star_rating_display
        rating = star_rating_display(stars)
        caller.location.msg_contents(
            f"\n|w*** Match over: {rating} ***|n",
            exclude=[caller],
        )

    # Clean up the script — delete() removes it from the character entirely
    # stop() only pauses it but leaves it attached to the character
    script.delete()
