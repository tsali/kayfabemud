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
        scripts = caller.scripts.get("match_script")
        if not scripts:
            caller.msg("You're not in a match.")
            return
        script = scripts[0]

        if script.db.match_over:
            caller.msg("The match is over.")
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
            # Auto-select a move for the phase
            if not valid_keys:
                valid_keys = list(MOVES.keys())[:5]
            move_key = random.choice(valid_keys)
            move_data = MOVES[move_key]

        # Check alignment restrictions
        if move_data.get("heel_only") and caller.db.alignment == "Face":
            caller.msg("That's a dirty tactic! Faces can't do that without breaking kayfabe.")
            return
        if move_data.get("face_only") and caller.db.alignment == "Heel":
            caller.msg("That's a babyface move. Heels don't rally the crowd.")
            return

        # Execute
        success, damage, msg = script.execute_move(caller, move_data, is_player_a=True)
        caller.msg(f"\n{msg}")
        if caller.location:
            caller.location.msg_contents(f"\n{msg}", exclude=[caller])

        # Check for phase advance
        _check_advance(script, caller)


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
        scripts = caller.scripts.get("match_script")
        if not scripts:
            caller.msg("You're not in a match.")
            return
        script = scripts[0]

        if script.db.match_over:
            caller.msg("The match is over.")
            return

        msg = script.do_sell(is_player_a=True)
        caller.msg(f"\n{msg}")
        caller.msg("|xYou sell it like death. Good work.|n")
        if caller.location:
            caller.location.msg_contents(f"\n{msg}", exclude=[caller])

        _check_advance(script, caller)


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
        caller.msg(f"\n{msg}")
        if caller.location:
            caller.location.msg_contents(f"\n{msg}", exclude=[caller])

        if success and phase == "comeback":
            # Advance to finish
            script.advance_phase()


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


class CmdKickout(Command):
    """
    Kick out of a pin attempt.

    Usage:
      kickout

    When the opponent attempts a pin, try to kick out.
    Uses Toughness. Harder when you're beaten down.
    """

    key = "kickout"
    aliases = ["ko"]
    locks = "cmd:all()"
    help_category = "Wrestling"

    def func(self):
        caller = self.caller
        scripts = caller.scripts.get("match_script")
        if not scripts:
            caller.msg("You're not in a match. Nothing to kick out of.")
            return
        script = scripts[0]

        success, msg = script.do_kickout(is_player_a=True)
        caller.msg(f"\n{msg}")
        if caller.location:
            caller.location.msg_contents(f"\n{msg}", exclude=[caller])


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

        for key in sorted(valid):
            m = MOVES[key]
            align_tag = ""
            if m.get("heel_only"):
                align_tag = " |r[Heel]|n"
            elif m.get("face_only"):
                align_tag = " |g[Face]|n"
            caller.msg(
                f"  |c{m['name']:25s}|n  {m['type']:10s}  "
                f"Diff:{m['difficulty']}  Dmg:{m['damage']}{align_tag}"
            )
        caller.msg(f"\n|wUsage: |cwork <move name>|n to use a specific move.")


class CmdCard(Command):
    """
    See who's in the building — available opponents.

    Usage:
      card
    """

    key = "card"
    aliases = ["roster", "opponents"]
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

        if success:
            script.db.crowd_heat = min(100, script.db.crowd_heat + 4)
            script.db.a_momentum += 2
            caller.msg(
                f"\n|y{caller.key} fires back with a flurry! The crowd stirs--\n"
                f"but they get cut off! Not yet... but the crowd FELT that!|n"
            )
        else:
            caller.msg(
                f"\n|x{caller.key} tries to fight back but gets shut down immediately.|n"
            )

        script.db.move_count += 1
        _check_advance(script, caller)


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

    # Auto-end if someone's health hits 0 in finish phase
    if phase == "finish":
        if script.db.b_health <= 0:
            # NPC is done, auto-finisher opportunity
            caller.msg(
                f"\n|Y{script.db.wrestler_b.key} is barely standing! "
                f"NOW is the time -- hit your finisher!|n"
            )
        elif script.db.a_health <= 0:
            # Player is down — NPC finishes
            _npc_finishes(script, caller)


def _npc_finishes(script, caller):
    """NPC hits their finisher on the player."""
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
