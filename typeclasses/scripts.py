"""
Kayfabe: Protect the Business — Scripts.

MatchScript: State machine for wrestling matches.
Phases: opening -> heat -> hope -> comeback -> finish
"""

import random
from evennia.scripts.scripts import DefaultScript
from evennia.utils import logger


# Match phases in order
MATCH_PHASES = ["opening", "heat", "hope", "comeback", "finish"]

PHASE_DESCRIPTIONS = {
    "opening": (
        "|w--- OPENING ---\n"
        "The bell rings! Both wrestlers circle each other, feeling out the opponent.\n"
        "Technical exchanges and basic moves set the pace.|n"
    ),
    "heat": (
        "|r--- HEAT SEGMENT ---\n"
        "The {heel_name} takes control! They're dominating the match,\n"
        "cutting the ring in half and working over {face_name}.|n"
    ),
    "hope": (
        "|y--- HOPE SPOT ---\n"
        "{face_name} fires back briefly! The crowd stirs--\n"
        "but {heel_name} cuts them off! Not yet...|n"
    ),
    "comeback": (
        "|g--- THE COMEBACK ---\n"
        "{face_name} is fighting back! The crowd is getting louder!\n"
        "They're feeding off the energy! This is the moment!|n"
    ),
    "finish": (
        "|w--- THE FINISH ---\n"
        "We're in the home stretch! Both wrestlers are throwing everything\n"
        "they have! Someone's going down!|n"
    ),
}


class Script(DefaultScript):
    """Base script typeclass."""
    pass


class MatchScript(DefaultScript):
    """
    State machine for a wrestling match.

    Attached to the player character during a match.
    Tracks phase, crowd heat, move count, and resolves each phase.

    Attributes:
        wrestler_a: The player character (or challenger)
        wrestler_b: The opponent (NPC or player)
        phase_index: Current phase (0-4)
        crowd_heat: Current crowd heat (0-100)
        move_count: Total moves executed
        a_health: Wrestler A's remaining stamina (0-100)
        b_health: Wrestler B's remaining stamina (0-100)
        a_momentum: Wrestler A's momentum (affects comeback)
        b_momentum: Wrestler B's momentum
        awaiting_input: Whether we're waiting for the player's next action
        match_over: Whether the match has ended
        winner: Who won ("a", "b", or "draw")
        booked_winner: Pre-determined winner ("a" or "b") — this is wrestling
        is_pvp: Whether this is player vs player
    """

    def at_script_creation(self):
        self.key = "match_script"
        self.desc = "Active wrestling match"
        self.persistent = False
        self.interval = 0  # No auto-repeat; player-driven

        # Match state
        self.db.wrestler_a = None
        self.db.wrestler_b = None
        self.db.phase_index = 0
        self.db.crowd_heat = 30  # starts warm
        self.db.move_count = 0
        self.db.a_health = 100
        self.db.b_health = 100
        self.db.a_momentum = 0
        self.db.b_momentum = 0
        self.db.awaiting_input = True
        self.db.match_over = False
        self.db.winner = None
        self.db.booked_winner = "a"  # player wins by default vs NPCs
        self.db.is_pvp = False
        self.db.star_breakdown = {}
        self.db.pending_pin = False

    def setup_match(self, wrestler_a, wrestler_b, booked_winner="a"):
        """Initialize match participants."""
        self.db.wrestler_a = wrestler_a
        self.db.wrestler_b = wrestler_b
        self.db.booked_winner = booked_winner

        # Determine face/heel for phase descriptions
        align_a = getattr(wrestler_a.db, 'alignment', 'Face')
        align_b = getattr(wrestler_b.db, 'alignment', 'Face')

        if align_a in ("Heel", ) and align_b != "Heel":
            self.db.heel = "a"
        elif align_b in ("Heel", ) and align_a != "Heel":
            self.db.heel = "b"
        else:
            # If both same alignment, the one losing is the "face" of the match
            self.db.heel = "b" if booked_winner == "a" else "a"

    def get_face_heel_names(self):
        """Return (face_name, heel_name) for match descriptions."""
        a = self.db.wrestler_a
        b = self.db.wrestler_b
        if not a or not b:
            return "Wrestler A", "Wrestler B"
        if self.db.heel == "a":
            return b.key, a.key
        return a.key, b.key

    def current_phase(self):
        """Return current phase name."""
        idx = min(self.db.phase_index, len(MATCH_PHASES) - 1)
        return MATCH_PHASES[idx]

    def announce_phase(self):
        """Send phase description to participants."""
        phase = self.current_phase()
        face_name, heel_name = self.get_face_heel_names()
        desc = PHASE_DESCRIPTIONS.get(phase, "")
        desc = desc.format(face_name=face_name, heel_name=heel_name)

        a = self.db.wrestler_a
        b = self.db.wrestler_b
        if a:
            a.msg(f"\n{desc}")
            self._show_status(a)
        if b and self.db.is_pvp and hasattr(b, 'msg'):
            b.msg(f"\n{desc}")
            self._show_status(b)

        # Also announce to room
        if a and a.location:
            a.location.msg_contents(
                f"\n{desc}",
                exclude=[a] + ([b] if self.db.is_pvp and b else []),
            )

    def _show_status(self, viewer):
        """Show match status HUD to a participant."""
        a = self.db.wrestler_a
        b = self.db.wrestler_b
        if not a or not b:
            return

        a_hp = max(0, self.db.a_health)
        b_hp = max(0, self.db.b_health)
        a_mom = self.db.a_momentum or 0
        b_mom = self.db.b_momentum or 0
        heat = self.db.crowd_heat

        phase = self.current_phase()
        phase_colors = {
            "opening": "|w",
            "heat": "|r",
            "hope": "|y",
            "comeback": "|g",
            "finish": "|c",
        }
        phase_hints = {
            "opening": "Both wrestlers are feeling each other out",
            "heat": "The heel is in control",
            "hope": "A brief flurry — cut off!",
            "comeback": "The crowd is behind the comeback!",
            "finish": "This is it — someone is going down!",
        }
        pc = phase_colors.get(phase, "|w")
        hint = phase_hints.get(phase, "")

        # Determine which wrestler is which from viewer's perspective
        a_align = getattr(a.db, 'alignment', '') or ''
        b_align = getattr(b.db, 'alignment', '') or ''
        a_align_tag = f" |g[Face]|n" if a_align == "Face" else f" |r[Heel]|n" if a_align == "Heel" else f" |y[Anti-Hero]|n" if a_align == "Anti-Hero" else ""
        b_align_tag = f" |g[Face]|n" if b_align == "Face" else f" |r[Heel]|n" if b_align == "Heel" else f" |y[Anti-Hero]|n" if b_align == "Anti-Hero" else ""

        # Build HUD
        bar_w = 16
        viewer.msg(f"\n|w{'=' * 56}|n")
        viewer.msg(f"  {pc}{phase.upper()} PHASE|n — {hint}")
        viewer.msg(f"|w{'=' * 56}|n")

        # Wrestler B (opponent) first
        viewer.msg(f"  {b.key}{b_align_tag}")
        viewer.msg(f"  Health:   {_health_bar(b_hp, bar_w)} {b_hp:>3}%")
        viewer.msg(f"  Momentum: {_momentum_bar(b_mom, bar_w)} {b_mom:>3}")
        viewer.msg("")

        # Viewer/Player
        if viewer == a:
            viewer.msg(f"  |wYou|n{a_align_tag}")
            viewer.msg(f"  Health:   {_health_bar(a_hp, bar_w)} {a_hp:>3}%")
            viewer.msg(f"  Momentum: {_momentum_bar(a_mom, bar_w)} {a_mom:>3}")
        else:
            viewer.msg(f"  {a.key}{a_align_tag}")
            viewer.msg(f"  Health:   {_health_bar(a_hp, bar_w)} {a_hp:>3}%")
            viewer.msg(f"  Momentum: {_momentum_bar(a_mom, bar_w)} {a_mom:>3}")

        viewer.msg("")
        viewer.msg(f"  Crowd Heat: {_heat_bar(heat, bar_w)} {heat:>3}%")
        viewer.msg(f"|w{'-' * 56}|n")

        # Action prompts per phase
        if self.db.pending_pin:
            viewer.msg("|r  >>> Type |wkickout|r to kick out of the pin! <<<|n")
        elif phase == "opening":
            viewer.msg("  Actions: |cwork|n (attack)  |csell|n (let them work you)")
        elif phase == "heat":
            viewer.msg("  Actions: |cwork|n (attack)  |csell|n (take a beating)  |chope|n (fight back)")
        elif phase == "hope":
            viewer.msg("  Actions: |csell|n (get cut off)  |cwork|n (sneak in a shot)")
        elif phase == "comeback":
            viewer.msg("  Actions: |cwork|n (attack)  |ccomeback|n (fire up!)  |cfinish|n (hit finisher)")
        elif phase == "finish":
            viewer.msg("  Actions: |cwork|n (attack)  |cfinish|n (hit finisher)")

        viewer.msg(f"|w{'=' * 56}|n")

    def execute_move(self, attacker, move_data, is_player_a=True):
        """
        Execute a wrestling move during the match.
        Returns (success: bool, damage: int, message: str).
        """
        from world.rules import stat_check, opposed_check

        defender = self.db.wrestler_b if is_player_a else self.db.wrestler_a

        stat_key = move_data["stat"]
        difficulty = move_data["difficulty"] + 8  # base DC

        attacker_stat = attacker.get_stat(stat_key)
        success, roll, total, margin = stat_check(attacker_stat, difficulty)

        a_name = attacker.key
        d_name = defender.key if defender else "opponent"
        fmt = {"attacker": a_name, "defender": d_name}

        if success:
            damage = move_data["damage"] + max(0, margin // 3)
            msg = move_data["desc"].format(**fmt)

            # Apply damage
            if is_player_a:
                self.db.b_health = max(0, self.db.b_health - damage * 3)
                self.db.a_momentum += 2
            else:
                self.db.a_health = max(0, self.db.a_health - damage * 3)
                self.db.b_momentum += 2

            # Crowd heat
            phase = self.current_phase()
            if phase == "comeback":
                self.db.crowd_heat = min(100, self.db.crowd_heat + 5)
            elif phase == "finish":
                self.db.crowd_heat = min(100, self.db.crowd_heat + 3)
            else:
                self.db.crowd_heat = min(100, self.db.crowd_heat + 1)

            self.db.move_count += 1

            # Commentary
            from world.commentary import get_commentary, find_announcer_in_room
            announcer = find_announcer_in_room(attacker.location if attacker else None)
            commentary = get_commentary(
                self.current_phase(), True, a_name, d_name, announcer
            )
            if commentary and attacker and attacker.location:
                attacker.location.msg_contents(commentary)

            return True, damage, msg
        else:
            msg = move_data["fail_desc"].format(**fmt)
            # Botch gives opponent momentum
            if is_player_a:
                self.db.b_momentum += 1
            else:
                self.db.a_momentum += 1
            self.db.move_count += 1

            # Commentary
            from world.commentary import get_commentary, find_announcer_in_room
            announcer = find_announcer_in_room(attacker.location if attacker else None)
            commentary = get_commentary(
                self.current_phase(), False, a_name, d_name, announcer
            )
            if commentary and attacker and attacker.location:
                attacker.location.msg_contents(commentary)

            return False, 0, msg

    def do_sell(self, is_player_a=True):
        """Player sells for opponent — opponent gets a free move."""
        from world.moves import MOVES, get_moves_for_phase

        phase = self.current_phase()
        valid_moves = get_moves_for_phase(phase)
        if not valid_moves:
            valid_moves = list(MOVES.keys())[:5]

        move_key = random.choice(valid_moves)
        move_data = MOVES[move_key]

        # Opponent executes the move (always succeeds when sold for)
        if is_player_a:
            attacker = self.db.wrestler_b
            defender = self.db.wrestler_a
        else:
            attacker = self.db.wrestler_a
            defender = self.db.wrestler_b

        a_name = attacker.key if attacker else "Opponent"
        d_name = defender.key if defender else "You"
        fmt = {"attacker": a_name, "defender": d_name}

        damage = move_data["damage"]
        msg = move_data["desc"].format(**fmt)

        if is_player_a:
            self.db.a_health = max(0, self.db.a_health - damage * 3)
            self.db.b_momentum += 2
        else:
            self.db.b_health = max(0, self.db.b_health - damage * 3)
            self.db.a_momentum += 2

        # Selling well increases crowd heat and match quality
        self.db.crowd_heat = min(100, self.db.crowd_heat + 3)
        self.db.move_count += 1

        return msg

    def do_comeback(self, is_player_a=True):
        """Fire up comeback — CHA + crowd heat check."""
        from world.rules import stat_check

        char = self.db.wrestler_a if is_player_a else self.db.wrestler_b
        cha = char.get_stat("cha")
        heat_bonus = self.db.crowd_heat // 20

        success, roll, total, margin = stat_check(cha, 12, bonus=heat_bonus)

        name = char.key
        if success:
            self.db.crowd_heat = min(100, self.db.crowd_heat + 10)
            if is_player_a:
                self.db.a_momentum += 5
            else:
                self.db.b_momentum += 5
            msg = (
                f"|g{name} is FIRING UP! The crowd is going INSANE!\n"
                f"{name} feeds off the energy and storms back into the match!|n"
            )
        else:
            msg = (
                f"|r{name} tries to mount a comeback but gets cut off!\n"
                f"Not yet... the crowd groans in sympathy.|n"
            )

        return success, msg

    def attempt_finisher(self, is_player_a=True):
        """
        Attempt to hit the finisher. This is the big moment.
        Success based on momentum, health differential, and the booking.
        """
        from world.rules import stat_check

        char = self.db.wrestler_a if is_player_a else self.db.wrestler_b
        opp = self.db.wrestler_b if is_player_a else self.db.wrestler_a

        finisher_name = char.db.finisher_name or "Finisher"
        finisher_type = char.db.finisher_type or "power"

        # Stat for finisher
        type_to_stat = {"power": "str", "technical": "tec", "aerial": "agi", "charisma": "cha"}
        stat_key = type_to_stat.get(finisher_type, "str")
        stat_val = char.get_stat(stat_key)

        # Momentum bonus
        momentum = self.db.a_momentum if is_player_a else self.db.b_momentum
        momentum_bonus = momentum // 3

        # Check if this is the booked finish
        is_booked = (
            (is_player_a and self.db.booked_winner == "a") or
            (not is_player_a and self.db.booked_winner == "b")
        )

        # Difficulty is lower if you're the booked winner and opponent is low on health
        opp_health = self.db.b_health if is_player_a else self.db.a_health
        health_bonus = max(0, (100 - opp_health) // 15)

        difficulty = 14
        if is_booked and opp_health < 30:
            difficulty = 8  # the finish is protected
        elif is_booked:
            difficulty = 11

        success, roll, total, margin = stat_check(
            stat_val, difficulty, bonus=momentum_bonus + health_bonus
        )

        name = char.key
        opp_name = opp.key if opp else "opponent"

        if success:
            msg = (
                f"\n|Y{name} hits {finisher_name}!!!\n"
                f"COVER! ONE! TWO! THREE!!!\n\n"
                f"*** {name} WINS! ***|n\n"
            )
            self.db.match_over = True
            self.db.winner = "a" if is_player_a else "b"
        else:
            # Near fall!
            self.db.crowd_heat = min(100, self.db.crowd_heat + 8)
            msg = (
                f"\n|y{name} goes for the {finisher_name}--\n"
                f"but {opp_name} KICKS OUT! NEAR FALL!\n"
                f"The crowd ERUPTS!|n\n"
            )

        return success, msg

    def do_kickout(self, is_player_a=True):
        """Attempt to kick out of a pin (when opponent is finishing)."""
        from world.rules import stat_check

        char = self.db.wrestler_a if is_player_a else self.db.wrestler_b
        tou = char.get_stat("tou")
        health = self.db.a_health if is_player_a else self.db.b_health
        health_penalty = max(0, (100 - health) // 20)

        success, roll, total, margin = stat_check(tou, 12 + health_penalty)

        name = char.key
        if success:
            self.db.crowd_heat = min(100, self.db.crowd_heat + 5)
            msg = f"|g{name} KICKS OUT at {random.choice(['one', 'two', 'two and a half'])}!|n"
        else:
            msg = f"|r{name} can't kick out! They're done!|n"

        return success, msg

    def advance_phase(self):
        """Move to the next match phase with dramatic announcement."""
        if self.db.phase_index < len(MATCH_PHASES) - 1:
            self.db.phase_index += 1
            phase = self.current_phase()

            phase_colors = {
                "heat": "|r",
                "hope": "|y",
                "comeback": "|g",
                "finish": "|c",
            }
            phase_announcements = {
                "heat": ("HEAT SEGMENT", "The heel takes control! You're being worked over!"),
                "hope": ("HOPE SPOT", "A brief glimmer -- fight back!"),
                "comeback": ("THE COMEBACK", "You're firing up! The crowd feels it!\n  New action: |wcomeback|n (full momentum!)"),
                "finish": ("THE FINISH", "This is it! Go for the finisher!\n  New action: |wfinish|n (hit your finisher!)"),
            }
            pc = phase_colors.get(phase, "|w")
            name, hint = phase_announcements.get(phase, (phase.upper(), ""))

            a = self.db.wrestler_a
            if a:
                a.msg(
                    f"\n{pc}{'=' * 40}|n\n"
                    f"  {pc}>>> {name} <<<|n\n"
                    f"  {hint}\n"
                    f"{pc}{'=' * 40}|n"
                )

            self.announce_phase()
            return True
        return False

    def should_advance(self):
        """Check if phase should auto-advance based on move count."""
        phase = self.current_phase()
        moves_in_phase = self.db.move_count

        # Rough guide: ~3-5 moves per phase
        thresholds = {
            "opening": 3,
            "heat": 5,
            "hope": 2,
            "comeback": 4,
            "finish": 6,  # finish can go longer with near falls
        }

        # Phase advances after enough moves in that phase
        # We use total move count with phase-based offsets
        phase_starts = [0, 3, 8, 10, 14]
        idx = self.db.phase_index
        if idx < len(phase_starts) - 1:
            return moves_in_phase >= phase_starts[idx + 1]
        return False

    def end_match(self):
        """
        Resolve the match — calculate stars, award XP, update records.
        Returns (stars, payoff, xp, summary_msg).
        """
        from world.rules import (
            calculate_match_quality, star_rating_display,
            xp_for_match, match_payoff, check_level_up, kayfabe_change
        )

        a = self.db.wrestler_a
        b = self.db.wrestler_b
        winner = self.db.winner

        if not a or not b:
            return 0, 0, 0, "Match ended (error: missing participants)."

        # Star rating
        stars, breakdown = calculate_match_quality(
            a, b,
            crowd_heat=self.db.crowd_heat,
            match_length=self.db.move_count,
        )
        self.db.star_breakdown = breakdown

        # Determine player won/lost
        player_won = (winner == "a")

        # Determine card position from promoter trust
        from world.rules import get_card_position
        territory = getattr(a.db, 'territory', '') or ''
        card_pos = get_card_position(a, territory) if territory else "opener"

        # XP
        xp = xp_for_match(stars, player_won, card_pos)

        # Payoff
        tier = getattr(a.db, 'tier', 1)
        payoff = match_payoff(tier, card_pos, stars, player_won)

        # Apply manager cut to payoff
        manager_cut = 0
        if a.db.manager:
            from evennia.utils.search import search_tag
            mgr_list = search_tag("npc_manager", category="npc_type")
            for m in mgr_list:
                if m.key == a.db.manager:
                    cut_pct = m.db.cut_percent or 20
                    manager_cut = int(payoff * cut_pct / 100)
                    payoff -= manager_cut
                    break

        # Update player stats
        a.db.xp = (a.db.xp or 0) + xp
        a.db.money = (a.db.money or 0) + payoff
        a.db.matches_wrestled = (a.db.matches_wrestled or 0) + 1
        a.db.match_quality_total = (a.db.match_quality_total or 0) + stars

        if player_won:
            a.db.wins = (a.db.wins or 0) + 1
        else:
            a.db.losses = (a.db.losses or 0) + 1

        # Kayfabe bonus for good match
        if stars >= 3.0:
            kayfabe_change(a, 2, "great match")
        elif stars >= 2.0:
            kayfabe_change(a, 1, "good match")

        # Dirt sheet: log notable matches (3+ stars)
        if stars >= 3.0:
            from world.dirtsheet import log_event
            log_event("match_result",
                      winner=a.key if player_won else b.key,
                      loser=b.key if player_won else a.key,
                      stars=stars,
                      territory=territory)

        # Promoter trust gain for good matches
        if territory:
            from world.rules import change_promoter_trust
            if stars >= 3.0:
                change_promoter_trust(a, territory, 3, "great match")
            elif stars >= 2.0:
                change_promoter_trust(a, territory, 1, "good match")
            elif stars < 1.0:
                change_promoter_trust(a, territory, -2, "bad match")

        # Vet rapport gain from wrestling in their territory
        if territory and a.location:
            from typeclasses.npcs import NPCWrestler
            rapport = a.db.vet_rapport or {}
            for obj in a.location.contents:
                if isinstance(obj, NPCWrestler) and getattr(obj.db, 'signature_moves', None):
                    vet_terr = (obj.db.territory or obj.db.home_territory or "").lower()
                    if vet_terr == territory.lower() or obj.location == a.location:
                        gain = 10 if player_won else 5
                        old_r = rapport.get(obj.key, 0)
                        rapport[obj.key] = min(100, old_r + gain)
            a.db.vet_rapport = rapport

        # Record match history for player A
        import time as _time
        history_entry = {
            "opponent": b.key,
            "result": "win" if player_won else "loss",
            "stars": stars,
            "territory": territory,
            "timestamp": _time.time(),
        }
        hist = a.db.match_history or []
        hist.append(history_entry)
        if len(hist) > 50:
            hist = hist[-50:]
        a.db.match_history = hist

        # Update best match
        if stars > (a.db.best_match_stars or 0.0):
            a.db.best_match_stars = stars
            a.db.best_match_opponent = b.key

        # Update rivals
        rivals = a.db.rivals or {}
        rivals[b.key] = rivals.get(b.key, 0) + 1
        a.db.rivals = rivals

        # Record history for wrestler B if PvP
        if self.db.is_pvp and hasattr(b, 'db'):
            b_won = not player_won
            b_entry = {
                "opponent": a.key,
                "result": "win" if b_won else "loss",
                "stars": stars,
                "territory": territory,
                "timestamp": _time.time(),
            }
            b_hist = b.db.match_history or []
            b_hist.append(b_entry)
            if len(b_hist) > 50:
                b_hist = b_hist[-50:]
            b.db.match_history = b_hist

            if stars > (b.db.best_match_stars or 0.0):
                b.db.best_match_stars = stars
                b.db.best_match_opponent = a.key

            b_rivals = b.db.rivals or {}
            b_rivals[a.key] = b_rivals.get(a.key, 0) + 1
            b.db.rivals = b_rivals

        # Level up check
        levels = check_level_up(a)

        # Build summary
        rating = star_rating_display(stars)
        result = "|gWIN|n" if player_won else "|rLOSS|n"

        pos_display = card_pos.replace("_", " ").title()
        summary = (
            f"\n|w{'=' * 44}|n\n"
            f"|w  MATCH RESULT|n\n"
            f"|w{'=' * 44}|n\n"
            f"  {a.key} vs {b.key}\n"
            f"  Card Position: |c{pos_display}|n\n"
            f"  Result: {result}\n"
            f"  Star Rating: {rating}\n"
            f"  Crowd Heat: {self.db.crowd_heat}%\n"
            f"  Moves: {self.db.move_count}\n"
            f"  Payoff: |y${payoff}|n\n"
            f"  XP Earned: |c{xp}|n\n"
        )

        if manager_cut > 0:
            summary += f"  Manager Cut: |r-${manager_cut}|n ({a.db.manager})\n"

        if levels > 0:
            summary += f"  |YLEVEL UP! Now level {a.db.level}!|n\n"

        # Injury check
        from world.injuries import check_injury, apply_injury, format_injury_status
        injury = check_injury(a, match_intensity=self.db.crowd_heat)
        if injury:
            apply_injury(a, injury)
            summary += f"  |r*** INJURED: {injury['severity_name']} {injury['name']}|n\n"

        # Title match resolution
        title_match = getattr(a.db, 'pending_title_match', None)
        if title_match and player_won:
            self._resolve_title_win(a, title_match)
            summary += f"  |Y*** NEW CHAMPION: {title_match['title_name']} ***|n\n"
            # Dirt sheet: log title change
            from world.dirtsheet import log_event as _log_title
            _log_title("title_change",
                       winner=a.key,
                       title_name=title_match["title_name"],
                       territory=territory)
        if title_match:
            a.db.pending_title_match = None

        summary += f"|w{'=' * 44}|n"

        return stars, payoff, xp, summary

    def _resolve_title_win(self, winner, title_match):
        """Transfer a title to the winner."""
        import time as _time
        from evennia.scripts.models import ScriptDB

        territory = title_match["territory"]
        title_type = title_match.get("title_type", "main")

        try:
            registry = ScriptDB.objects.get(db_key="championship_registry")
        except (ScriptDB.DoesNotExist, ScriptDB.MultipleObjectsReturned):
            return

        if title_type == "womens":
            holders = registry.db.womens_title_holders or {}
        else:
            holders = registry.db.title_holders or {}

        holders[territory] = {
            "holder": winner.key,
            "defenses": 0,
            "won_at": _time.time(),
        }

        if title_type == "womens":
            registry.db.womens_title_holders = holders
        else:
            registry.db.title_holders = holders


def _health_bar(pct, width=20):
    """Render a health bar."""
    filled = int(pct / 100 * width)
    empty = width - filled
    if pct > 60:
        color = "|g"
    elif pct > 30:
        color = "|y"
    else:
        color = "|r"
    return f"[{color}{'|' * filled}|x{'.' * empty}|n]"


def _heat_bar(pct, width=20):
    """Render a crowd heat bar."""
    filled = int(pct / 100 * width)
    empty = width - filled
    if pct > 70:
        color = "|Y"
    elif pct > 40:
        color = "|y"
    else:
        color = "|x"
    return f"[{color}{'!' * filled}|x{'.' * empty}|n]"


def _momentum_bar(value, width=16):
    """Render a momentum bar (0-20+ scale)."""
    max_val = 20
    filled = min(int(value / max_val * width), width)
    empty = width - filled
    if value >= 15:
        color = "|Y"
    elif value >= 8:
        color = "|c"
    else:
        color = "|x"
    return f"[{color}{'>' * filled}|x{'.' * empty}|n]"


class FatigueScript(DefaultScript):
    """
    Global script that checks once per day at midnight Central Time.

    For each offline character NOT in an InnRoom or owned PlayerHouse:
    +1 fatigue stack. Each stack = -5% to all stat checks and skill gains.
    Online (puppeted) players at midnight are exempt.
    """

    def at_script_creation(self):
        self.key = "fatigue_script"
        self.desc = "Daily fatigue check at midnight Central"
        self.persistent = True
        self.interval = 60  # Poll every 60 seconds, fire once per day
        self.db.last_fire_date = ""  # YYYY-MM-DD of last firing

    def at_repeat(self):
        """Check if it's midnight Central and fire once per day."""
        import datetime
        try:
            from zoneinfo import ZoneInfo
        except ImportError:
            from backports.zoneinfo import ZoneInfo

        central = ZoneInfo("America/Chicago")
        now = datetime.datetime.now(central)
        today_str = now.strftime("%Y-%m-%d")
        last_date = self.db.last_fire_date or ""

        # Fire once per day, at or after midnight
        if today_str != last_date and now.hour >= 0:
            self.db.last_fire_date = today_str
            self._apply_fatigue()

    def _apply_fatigue(self):
        """Apply fatigue to all offline characters not in safe lodging."""
        from typeclasses.characters import Wrestler

        wrestlers = Wrestler.objects.filter(
            db_typeclass_path="typeclasses.characters.Wrestler"
        )

        affected = 0
        for char in wrestlers:
            if not char.db.chargen_complete:
                continue

            # Online (puppeted) players are exempt
            if char.sessions.count() > 0:
                continue

            # Check if in safe lodging
            if char.is_in_safe_lodging():
                continue

            # Apply fatigue
            char.db.fatigue_stacks = (char.db.fatigue_stacks or 0) + 1
            affected += 1

        if affected > 0:
            logger.log_info(
                f"KAYFABE FATIGUE: Midnight tick — {affected} character(s) gained fatigue."
            )


class EconomyTickScript(DefaultScript):
    """
    Global economy script that runs weekly (every 30 minutes real time = 1 game week).

    Each tick:
    - Deducts manager retainer fees from wrestlers who have managers
    - Processes any passive income (merch based on CHA + kayfabe)
    - Checks for rank-ups based on career progress
    """

    def at_script_creation(self):
        self.key = "economy_tick"
        self.desc = "Weekly economy processing"
        self.persistent = True
        self.interval = 1800  # 30 minutes = 1 game week

        self.db.week_count = 0

    def at_repeat(self):
        """Called every interval (one game week)."""
        self.db.week_count = (self.db.week_count or 0) + 1
        week = self.db.week_count

        self._process_manager_fees()
        self._process_contract_wages()
        self._process_merch_income()
        self._process_injury_recovery()
        self._process_rank_ups()
        self._process_rapport_decay()
        self._process_dirtsheet(week)

        # Log every 4 weeks (game month)
        if week % 4 == 0:
            logger.log_info(f"KAYFABE ECONOMY: Month {week // 4} processed.")

    def _process_manager_fees(self):
        """Deduct weekly manager retainer fees."""
        from typeclasses.characters import Wrestler
        from evennia.utils.search import search_tag

        wrestlers = Wrestler.objects.filter(
            db_typeclass_path="typeclasses.characters.Wrestler"
        )

        for char in wrestlers:
            mgr_name = char.db.manager
            if not mgr_name:
                continue

            # Find the manager NPC
            managers = search_tag("npc_manager", category="npc_type")
            mgr = None
            for m in managers:
                if m.key == mgr_name:
                    mgr = m
                    break

            if not mgr:
                continue

            retainer = mgr.db.retainer_cost or 100
            money = char.db.money or 0

            if money >= retainer:
                char.db.money = money - retainer
                if char.sessions.count():
                    char.msg(
                        f"|y[Economy] Manager retainer: -${retainer} to {mgr_name}. "
                        f"Balance: ${char.db.money}|n"
                    )
            else:
                # Can't afford — manager leaves
                char.db.manager = ""
                if char.sessions.count():
                    char.msg(
                        f"|r[Economy] You can't afford {mgr_name}'s retainer (${retainer}). "
                        f"They've dropped you as a client.|n"
                    )
                # Mark manager as available again
                mgr.db.available = True

    def _process_contract_wages(self):
        """Pay weekly contract wages and decrement remaining weeks."""
        from typeclasses.characters import Wrestler

        wrestlers = Wrestler.objects.filter(
            db_typeclass_path="typeclasses.characters.Wrestler"
        )

        for char in wrestlers:
            contract = char.db.contract
            if not contract:
                continue

            pay = contract.get("weekly_pay", 0)
            weeks = contract.get("weeks_remaining", 0)

            if weeks <= 0:
                # Contract expired
                char.db.contract = None
                if char.sessions.count():
                    char.msg(
                        f"|y[Contract] Your contract with {contract.get('territory', '???')} "
                        f"has expired. Visit a Promoter's Office to re-sign.|n"
                    )
                continue

            # Pay wages
            char.db.money = (char.db.money or 0) + pay
            contract["weeks_remaining"] = weeks - 1
            char.db.contract = contract

            if char.sessions.count():
                char.msg(
                    f"|g[Contract] Weekly wages: +${pay} from {contract.get('territory', '???')}. "
                    f"Balance: ${char.db.money}. ({weeks - 1} weeks left)|n"
                )

    def _process_injury_recovery(self):
        """Process injury recovery for all characters."""
        from typeclasses.characters import Wrestler
        from world.injuries import process_injury_recovery

        wrestlers = Wrestler.objects.filter(
            db_typeclass_path="typeclasses.characters.Wrestler"
        )

        for char in wrestlers:
            if not char.db.injury:
                continue
            is_resting = char.is_in_safe_lodging() if hasattr(char, 'is_in_safe_lodging') else False
            process_injury_recovery(char, is_resting=is_resting)

    def _process_merch_income(self):
        """Passive merch income based on CHA, kayfabe, and rank."""
        from typeclasses.characters import Wrestler

        wrestlers = Wrestler.objects.filter(
            db_typeclass_path="typeclasses.characters.Wrestler"
        )

        for char in wrestlers:
            if not char.db.chargen_complete:
                continue

            cha = char.get_stat("cha")
            kayfabe = char.db.kayfabe or 50
            rank_idx = char.db.rank_index or 0

            # Base merch: CHA/4 * rank multiplier * kayfabe factor
            # Only kicks in at Midcarder (rank 3) or above
            if rank_idx < 3:
                continue

            rank_mult = {3: 1, 4: 2, 5: 4, 6: 8, 7: 15}.get(rank_idx, 1)
            kayfabe_factor = kayfabe / 50.0  # 1.0 at 50 kayfabe, 2.0 at 100
            merch = int((cha / 4) * rank_mult * kayfabe_factor)

            if merch > 0:
                # Gear bonus to merch
                from commands.economy import GEAR_TIERS
                gear_tier = char.db.gear_tier or 0
                gear_bonus = GEAR_TIERS.get(gear_tier, {}).get("cha_bonus", 0)
                merch += gear_bonus * rank_mult

                # Manager cut
                if char.db.manager:
                    from evennia.utils.search import search_tag
                    managers = search_tag("npc_manager", category="npc_type")
                    for m in managers:
                        if m.key == char.db.manager:
                            cut_pct = m.db.cut_percent or 20
                            cut = int(merch * cut_pct / 100)
                            merch -= cut
                            break

                char.db.money = (char.db.money or 0) + merch
                if char.sessions.count():
                    char.msg(f"|g[Economy] Merchandise sales: +${merch}. Balance: ${char.db.money}|n")

    def _process_rank_ups(self):
        """Check all active players for rank promotions."""
        from typeclasses.characters import Wrestler
        from world.rules import check_rank_up

        wrestlers = Wrestler.objects.filter(
            db_typeclass_path="typeclasses.characters.Wrestler"
        )

        for char in wrestlers:
            if not char.db.chargen_complete:
                continue

            new_rank = check_rank_up(char)
            if new_rank:
                # Dirt sheet: log rank up
                from world.dirtsheet import log_event as _log_rank
                _log_rank("rank_up", name=char.key, new_rank=new_rank)
                if char.sessions.count():
                    char.msg(
                        f"\n|Y*** RANK UP ***\n"
                        f"You have been promoted to |w{new_rank}|Y!\n"
                        f"The wrestling world is taking notice.|n\n"
                    )

    def _process_rapport_decay(self):
        """Decay vet rapport by 1/week for vets not in player's territory."""
        from typeclasses.characters import Wrestler

        wrestlers = Wrestler.objects.filter(
            db_typeclass_path="typeclasses.characters.Wrestler"
        )

        for char in wrestlers:
            if not char.db.chargen_complete:
                continue
            rapport = char.db.vet_rapport
            if not rapport:
                continue

            territory = (char.db.territory or "").lower()
            changed = False
            for vet_name in list(rapport.keys()):
                # Check if vet is in same territory (approximate by room)
                in_territory = False
                if char.location:
                    for obj in char.location.contents:
                        if obj.key == vet_name:
                            in_territory = True
                            break
                if not in_territory:
                    if rapport[vet_name] > 0:
                        rapport[vet_name] = max(0, rapport[vet_name] - 1)
                        changed = True
                    if rapport[vet_name] <= 0:
                        del rapport[vet_name]
                        changed = True

            if changed:
                char.db.vet_rapport = rapport

    def _process_dirtsheet(self, week):
        """Generate the weekly dirt sheet newsletter."""
        from world.dirtsheet import process_dirtsheet
        process_dirtsheet(week)


class NPCSchedulerScript(DefaultScript):
    """
    Global script that manages NPC ambient behavior and guest appearances.

    Runs every 5 minutes (300s). Each tick:
    - Random NPCs in rooms with players perform ambient actions
    - Occasionally NPCs cut promos or issue challenges
    - Manages guest appearance rotation (move big names to smaller territories)
    """

    def at_script_creation(self):
        self.key = "npc_scheduler"
        self.desc = "NPC ambient behavior and guest appearances"
        self.persistent = True
        self.interval = 120  # 2 minutes

        self.db.guest_slots = {}  # territory_key -> {npc_id, expires_at}
        self.db.tick_count = 0

    def at_repeat(self):
        """Called every interval."""
        self.db.tick_count = (self.db.tick_count or 0) + 1

        # Ambient NPC actions
        self._do_ambient_actions()

        # Return roaming NPCs to home after 3 ticks
        if self.db.tick_count % 3 == 0:
            self._return_roaming_npcs()

        # Guest appearance rotation every 30 ticks (~1 hour)
        if self.db.tick_count % 30 == 0:
            self._rotate_guests()

    def _do_ambient_actions(self):
        """Make NPCs in rooms with players do ambient things."""
        from typeclasses.npcs import NPCWrestler, NPCManager
        from typeclasses.characters import Wrestler
        from evennia.utils.search import search_tag

        # Find all rooms that have players in them
        active_rooms = set()
        for obj in Wrestler.objects.filter(db_typeclass_path="typeclasses.characters.Wrestler"):
            if obj.location and obj.db.chargen_complete and obj.sessions.count():
                active_rooms.add(obj.location)

        for room in active_rooms:
            npcs = [
                obj for obj in room.contents
                if isinstance(obj, (NPCWrestler, NPCManager))
            ]
            if not npcs:
                continue

            # 30% chance per tick that an NPC does something
            if random.random() < 0.3:
                npc = random.choice(npcs)
                npc.do_ambient_action()

            # 10% chance an NPC cuts a promo
            if random.random() < 0.1:
                wrestlers = [n for n in npcs if isinstance(n, NPCWrestler)
                             and n.db.role == "wrestler"]
                if wrestlers:
                    npc = random.choice(wrestlers)
                    npc.do_ambient_promo()

            # 5% chance an NPC issues a challenge to a player
            if random.random() < 0.15:
                wrestlers = [n for n in npcs if isinstance(n, NPCWrestler)
                             and n.db.role == "wrestler"
                             and n.db.level >= 1]
                if wrestlers:
                    # Gender-weighted selection: prefer same-division NPCs
                    players_in_room = [
                        obj for obj in room.contents
                        if isinstance(obj, Wrestler) and obj.db.chargen_complete
                        and obj.sessions.count()
                    ]
                    if players_in_room:
                        target_player = random.choice(players_in_room)
                        p_gender = getattr(target_player.db, 'gender', 'Undisclosed') or 'Undisclosed'
                        if p_gender in ("Non-Binary", "Undisclosed"):
                            # 50/50, just pick anyone
                            npc = random.choice(wrestlers)
                        else:
                            # 70% same division, 30% cross
                            same = [n for n in wrestlers
                                    if (getattr(n.db, 'gender', 'Male') or 'Male') == p_gender]
                            cross = [n for n in wrestlers
                                     if (getattr(n.db, 'gender', 'Male') or 'Male') != p_gender]
                            if same and random.random() < 0.7:
                                npc = random.choice(same)
                            elif cross:
                                npc = random.choice(cross)
                            else:
                                npc = random.choice(wrestlers)
                        npc.issue_challenge()
                    else:
                        npc = random.choice(wrestlers)
                        npc.issue_challenge()

            # NPC roaming: move NPCs toward rooms with players
            if random.random() < 0.2:
                self._roam_npcs(room)

    def _roam_npcs(self, player_room):
        """Move an NPC from elsewhere in the territory to a room with a player."""
        from typeclasses.npcs import NPCWrestler
        from typeclasses.rooms import TerritoryRoom
        from evennia.utils.search import search_tag

        territory_key = getattr(player_room.db, 'territory_key', '')
        if not territory_key:
            return

        # Find all territory rooms
        territory_rooms = search_tag(territory_key, category="territory")
        if not territory_rooms:
            return

        # Find NPCs NOT in the player's room but in the same territory
        candidates = []
        for room in territory_rooms:
            if room == player_room:
                continue
            for obj in room.contents:
                if isinstance(obj, NPCWrestler) and obj.db.role in ("wrestler", "backyard"):
                    # Don't move NPCs that have been away from home too long
                    ticks_away = getattr(obj.db, 'roam_ticks', 0) or 0
                    if ticks_away < 3:
                        candidates.append(obj)

        if not candidates:
            return

        npc = random.choice(candidates)
        alignment = npc.db.alignment or "Face"

        # Track roaming state
        if not getattr(npc.db, 'home_room', None):
            npc.db.home_room = npc.location
        npc.db.roam_ticks = (getattr(npc.db, 'roam_ticks', 0) or 0) + 1

        # Move NPC to player's room
        npc.move_to(player_room, quiet=True)

        # Announce arrival with alignment flavor
        if alignment == "Heel":
            arrival = f"|c{npc.key}|n swagger into the room, eyeing everyone with contempt."
        elif alignment == "Face":
            arrival = f"|c{npc.key}|n walks in and nods respectfully to the crowd."
        else:
            arrival = f"|c{npc.key}|n slips into the room, sizing up everyone silently."

        player_room.msg_contents(arrival)

    def _return_roaming_npcs(self):
        """Return roaming NPCs to their home rooms after a few ticks."""
        from typeclasses.npcs import NPCWrestler

        for npc in NPCWrestler.objects.filter(db_typeclass_path="typeclasses.npcs.NPCWrestler"):
            home = getattr(npc.db, 'home_room', None)
            ticks = getattr(npc.db, 'roam_ticks', 0) or 0
            if home and ticks >= 3 and npc.location != home:
                npc.move_to(home, quiet=True)
                npc.db.roam_ticks = 0
                if npc.location:
                    npc.location.msg_contents(
                        f"|x{npc.key} heads back to their usual spot.|n"
                    )

    def _rotate_guests(self):
        """
        Move big-name NPCs to smaller territories for guest spots.
        A guest spot lasts ~6 hours (72 ticks).
        """
        import time
        from evennia.utils.search import search_tag
        from typeclasses.npcs import NPCWrestler

        now = time.time()
        guests = self.db.guest_slots or {}

        # Expire old guests — send them home
        for terr_key in list(guests.keys()):
            slot = guests[terr_key]
            if now > slot.get("expires_at", 0):
                npc_id = slot["npc_id"]
                npcs = search_tag(f"npc_{npc_id}", category="npc_id")
                if npcs:
                    npc = npcs[0]
                    # Send home
                    home_rooms = search_tag(npc.db.home_territory, category="territory")
                    arena_rooms = [r for r in home_rooms
                                   if hasattr(r.db, 'room_type')
                                   and r.db.room_type in ("arena", "backstage")]
                    if arena_rooms:
                        npc.move_to(arena_rooms[0], quiet=True)
                    npc.db.is_guest = False
                    npc.db.guest_territory = ""

                    # Announce departure
                    dest_rooms = search_tag(terr_key, category="territory")
                    for room in dest_rooms:
                        room.msg_contents(
                            f"|w{npc.key}'s guest appearance has ended. "
                            f"They head back to their home territory.|n"
                        )

                del guests[terr_key]

        # Maybe start a new guest spot (20% chance per rotation)
        if random.random() < 0.3 and len(guests) < 3:
            self._start_guest_spot(guests, now)

        self.db.guest_slots = guests

    def _start_guest_spot(self, guests, now):
        """Pick a big-name NPC and send them to a smaller territory."""
        from evennia.utils.search import search_tag
        from typeclasses.npcs import NPCWrestler

        # Eligible guests: tier 4 territory NPCs with level >= 30
        eligible = search_tag("named_npc", category="npc_type")
        eligible = [
            n for n in eligible
            if isinstance(n, NPCWrestler)
            and n.db.level >= 30
            and not n.db.is_guest
            and n.db.role == "wrestler"
        ]

        if not eligible:
            return

        # Pick a random big name
        guest_npc = random.choice(eligible)

        # Pick a destination territory (tier 1-3, not their home)
        dest_territories = ["fhwa", "gccw", "gsg", "bba", "lsu", "psc",
                            "pensacola", "slaughterhouse", "beastworks",
                            "conservatory", "dungeon", "proving_grounds",
                            "memphis", "midsouth", "midatlantic", "florida",
                            "georgia", "wccw", "awa", "stampede", "pnw"]
        dest_territories = [t for t in dest_territories
                            if t != guest_npc.db.home_territory
                            and t not in guests]

        if not dest_territories:
            return

        dest_key = random.choice(dest_territories)

        # Find arena room in destination
        dest_rooms = search_tag(dest_key, category="territory")
        arena_rooms = [r for r in dest_rooms
                       if hasattr(r.db, 'room_type')
                       and r.db.room_type in ("arena", "backstage", "training")]
        if not arena_rooms:
            return

        dest_room = arena_rooms[0]

        # Move the NPC
        guest_npc.move_to(dest_room, quiet=True)
        guest_npc.db.is_guest = True
        guest_npc.db.guest_territory = dest_key

        # Record the guest slot (expires in 6 hours)
        guests[dest_key] = {
            "npc_id": guest_npc.db.npc_id,
            "expires_at": now + 6 * 3600,
        }

        # Announce
        dest_room.msg_contents(
            f"\n|Y*** GUEST APPEARANCE ***\n"
            f"{guest_npc.key} has arrived for a guest spot!\n"
            f"The crowd buzz is electric!|n\n"
        )

        # Announce to all players in the territory
        from typeclasses.characters import Wrestler
        for obj in Wrestler.objects.filter(db_typeclass_path="typeclasses.characters.Wrestler"):
            if (obj.sessions.count() and obj.db.chargen_complete
                    and (obj.db.territory or "").lower() == dest_key
                    and obj.location != dest_room):
                obj.msg(
                    f"\n|y*** GUEST APPEARANCE: {guest_npc.key} has arrived at "
                    f"{dest_key.upper()}! ***|n"
                )


class StableRegistryScript(DefaultScript):
    """
    Global registry for stables/factions.
    Stores stable data: members, leader, territory, alignment, invites.
    """

    def at_script_creation(self):
        self.key = "stable_registry"
        self.desc = "Stable/faction registry"
        self.persistent = True
        self.interval = 0  # No repeating; data store only

        self.db.stables = {}  # {name: {leader, members, territory, alignment, invites}}


class ChampionshipRegistryScript(DefaultScript):
    """
    Global registry for championship title holders.
    """

    def at_script_creation(self):
        self.key = "championship_registry"
        self.desc = "Championship title registry"
        self.persistent = True
        self.interval = 0

        self.db.title_holders = {}  # {territory: {holder, defenses, won_at}}
        self.db.womens_title_holders = {}


class ShowSchedulerScript(DefaultScript):
    """
    Global script that generates show cards every 4 economy ticks (1 game month).
    Announces upcoming shows 2 ticks before they happen.
    """

    def at_script_creation(self):
        self.key = "show_scheduler"
        self.desc = "Show card generator"
        self.persistent = True
        self.interval = 1800  # Same as economy tick (30 min)

        self.db.tick_count = 0
        self.db.upcoming_shows = {}  # {territory: show_dict}
        self.db.show_history = []  # last 20 shows

    def at_repeat(self):
        self.db.tick_count = (self.db.tick_count or 0) + 1
        tick = self.db.tick_count

        # Every 4 ticks (1 game month), generate new cards
        if tick % 4 == 0:
            self._generate_shows()

        # 2 ticks before show, announce
        if tick % 4 == 2:
            self._announce_shows()

    def _generate_shows(self):
        """Generate show cards for all active territories."""
        from world.shows import generate_show_card
        from typeclasses.characters import Wrestler
        from typeclasses.npcs import NPCWrestler
        from evennia.utils.search import search_tag

        # Territories that run shows (tier 3+)
        show_territories = [
            "memphis", "midsouth", "midatlantic", "florida", "georgia",
            "wccw", "awa", "stampede", "pnw",
            "ovw", "fcw", "dsw", "hwa",
            "wwf", "wcw", "ecw", "uk", "japan",
        ]

        upcoming = {}
        wrestlers = Wrestler.objects.filter(
            db_typeclass_path="typeclasses.characters.Wrestler"
        )

        for terr in show_territories:
            # Find contracted players in this territory
            contracted = [
                w for w in wrestlers
                if w.db.chargen_complete
                and w.db.contract
                and w.db.contract.get("territory") == terr
            ]

            # Find NPC wrestlers for this territory
            npc_list = search_tag(terr, category="territory_home")
            npcs = [
                n for n in npc_list
                if isinstance(n, NPCWrestler)
                and getattr(n.db, 'role', 'wrestler') == 'wrestler'
            ]

            show = generate_show_card(terr, contracted, npcs)
            upcoming[terr] = show

        # Archive old shows
        history = self.db.show_history or []
        old_shows = self.db.upcoming_shows or {}
        for show in old_shows.values():
            history.append(show)
        if len(history) > 20:
            history = history[-20:]
        self.db.show_history = history

        self.db.upcoming_shows = upcoming

    def _announce_shows(self):
        """Announce upcoming shows to players in those territories."""
        from typeclasses.characters import Wrestler

        upcoming = self.db.upcoming_shows or {}
        wrestlers = Wrestler.objects.filter(
            db_typeclass_path="typeclasses.characters.Wrestler"
        )

        for terr, show in upcoming.items():
            if show.get("announced"):
                continue

            # Find online players in this territory
            for w in wrestlers:
                if (w.db.chargen_complete and w.sessions.count()
                        and (w.db.territory or "").lower() == terr):
                    w.msg(
                        f"\n|Y*** UPCOMING SHOW ***|n\n"
                        f"  |w{show['name']}|n\n"
                        f"  Check the card with |wshows|n.\n"
                    )

            show["announced"] = True

        self.db.upcoming_shows = upcoming
