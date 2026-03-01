"""
Kayfabe: Protect the Business — PvP commands.

challenge <player> — propose a match against another player
accept             — accept a pending challenge
team <player>      — propose forming a tag team
betray <partner>   — turn on your partner (generates massive heat)
feud               — view current feuds
"""

import random
from evennia.commands.command import Command
from evennia.utils.create import create_script


class CmdChallenge(Command):
    """
    Challenge another player to a match.

    Usage:
      challenge <player>

    Both players must be in the same room. The challenged player
    must type 'accept' to start the match.
    """

    key = "challenge"
    locks = "cmd:all()"
    help_category = "PvP"

    def func(self):
        caller = self.caller
        if not caller.db.chargen_complete:
            caller.msg("Finish character creation first.")
            return

        if caller.scripts.get("match_script"):
            caller.msg("You're already in a match.")
            return

        if not self.args:
            caller.msg("Usage: challenge <player>")
            return

        target = caller.search(self.args.strip(), location=caller.location)
        if not target:
            return

        if target == caller:
            caller.msg("You can't challenge yourself.")
            return

        # Check target is a player character with chargen done
        if not hasattr(target.db, 'chargen_complete') or not target.db.chargen_complete:
            caller.msg(f"{target.key} isn't a wrestler you can challenge.")
            return

        # Store pending challenge
        caller.db.pending_challenge_to = target
        target.db.pending_challenge_from = caller

        caller.msg(f"|wYou challenge |c{target.key}|w to a match!|n")
        target.msg(
            f"\n|Y{caller.key} has challenged you to a match!|n\n"
            f"Type |waccept|n to accept, or ignore to decline."
        )

        if caller.location:
            caller.location.msg_contents(
                f"|w{caller.key} calls out {target.key} for a match!|n",
                exclude=[caller, target],
            )


class CmdAccept(Command):
    """
    Accept a pending match challenge.

    Usage:
      accept
    """

    key = "accept"
    locks = "cmd:all()"
    help_category = "PvP"

    def func(self):
        caller = self.caller
        challenger = caller.db.pending_challenge_from

        if not challenger:
            caller.msg("No one has challenged you.")
            return

        # Verify challenger is still in the room
        if challenger.location != caller.location:
            caller.msg(f"{challenger.key} is no longer here.")
            caller.db.pending_challenge_from = None
            return

        if challenger.scripts.get("match_script"):
            caller.msg(f"{challenger.key} is already in a match.")
            caller.db.pending_challenge_from = None
            return

        # Clear pending
        caller.db.pending_challenge_from = None
        if hasattr(challenger.db, 'pending_challenge_to'):
            challenger.db.pending_challenge_to = None

        # No pre-determined winner in PvP — it's based on actual play
        # But we pick a "booked" winner randomly for the narrative
        booked = random.choice(["a", "b"])

        # Create match script on the challenger (player A)
        script = create_script(
            "typeclasses.scripts.MatchScript",
            key="match_script",
            obj=challenger,
        )
        script.setup_match(challenger, caller, booked_winner=booked)
        script.db.is_pvp = True

        # Also attach a reference on the accepting player
        caller.db.pvp_match_script = script
        caller.db.pvp_opponent = challenger

        # Announce
        msg = (
            f"\n|w{'=' * 44}|n\n"
            f"|w  PVP MATCH: {challenger.key} vs {caller.key}|n\n"
            f"|w{'=' * 44}|n\n"
            f"The bell rings! This is personal!\n"
        )
        challenger.msg(msg)
        caller.msg(msg)
        if caller.location:
            caller.location.msg_contents(
                f"\n|w*** PVP: {challenger.key} vs {caller.key}! ***|n",
                exclude=[caller, challenger],
            )

        script.announce_phase()


class CmdTeam(Command):
    """
    Propose forming a tag team with another player.

    Usage:
      team <player>

    Both players must agree. Tag teams share reputation bonuses.
    """

    key = "team"
    aliases = ["tagteam"]
    locks = "cmd:all()"
    help_category = "PvP"

    def func(self):
        caller = self.caller
        if not self.args:
            # Show current team
            partner = caller.db.tag_partner
            if partner:
                team_name = caller.db.tag_team_name or "Unnamed Team"
                caller.msg(f"|wTag Team:|n |c{team_name}|n — {caller.key} & {partner.key}")
            else:
                caller.msg("You don't have a tag team partner. Usage: team <player>")
            return

        target = caller.search(self.args.strip(), location=caller.location)
        if not target:
            return

        if target == caller:
            caller.msg("You can't team with yourself.")
            return

        if not hasattr(target.db, 'chargen_complete') or not target.db.chargen_complete:
            caller.msg(f"{target.key} isn't available for teaming.")
            return

        # Store proposal
        caller.db.team_proposal_to = target
        target.db.team_proposal_from = caller

        caller.msg(f"|wYou propose a tag team with |c{target.key}|w!|n")
        target.msg(
            f"\n|Y{caller.key} wants to form a tag team with you!|n\n"
            f"Type |wteam {caller.key}|n to accept."
        )

        # Check if mutual (both proposed to each other)
        if hasattr(target.db, 'team_proposal_to') and target.db.team_proposal_to == caller:
            # Both agreed!
            caller.db.tag_partner = target
            target.db.tag_partner = caller
            team_name = f"{caller.key} & {target.key}"
            caller.db.tag_team_name = team_name
            target.db.tag_team_name = team_name
            caller.db.team_proposal_to = None
            target.db.team_proposal_from = None
            target.db.team_proposal_to = None
            caller.db.team_proposal_from = None

            msg = f"|Y*** TAG TEAM FORMED: {team_name} ***|n"
            caller.msg(msg)
            target.msg(msg)
            if caller.location:
                caller.location.msg_contents(msg, exclude=[caller, target])


class CmdBetray(Command):
    """
    Turn on your tag team partner or stable member.

    Usage:
      betray <partner>

    Betrayals generate MASSIVE crowd heat if timed well.
    The betrayed partner gets a sympathy pop.
    Poorly timed betrayals tank both wrestlers' reputations.
    """

    key = "betray"
    aliases = ["turnon"]
    locks = "cmd:all()"
    help_category = "PvP"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("Betray who? Usage: betray <partner>")
            return

        target = caller.search(self.args.strip(), location=caller.location)
        if not target:
            return

        partner = caller.db.tag_partner
        if not partner or partner != target:
            caller.msg(f"{target.key} isn't your partner. You can only betray a partner.")
            return

        from world.rules import kayfabe_change, stat_check

        # Check if betrayal is well-timed (CHA + PSY check)
        cha = caller.get_stat("cha")
        psy = caller.get_stat("psy")
        avg = (cha + psy) // 2
        success, roll, total, margin = stat_check(avg, 12)

        # Break up the team
        caller.db.tag_partner = None
        target.db.tag_partner = None
        caller.db.tag_team_name = ""
        target.db.tag_team_name = ""

        if success:
            # Well-executed turn
            kayfabe_change(caller, 8, "brilliant betrayal")
            kayfabe_change(target, 5, "sympathetic victim")

            caller.db.xp = (caller.db.xp or 0) + 30
            target.db.xp = (target.db.xp or 0) + 20

            msg = (
                f"\n|R*** BETRAYAL! ***\n"
                f"{caller.key} TURNS on {target.key}!\n"
                f"The crowd is in SHOCK! This changes EVERYTHING!|n"
            )
        else:
            # Poorly timed
            kayfabe_change(caller, -5, "botched betrayal")
            kayfabe_change(target, -2, "victim of bad turn")

            msg = (
                f"\n|r{caller.key} turns on {target.key}...\n"
                f"but the crowd barely reacts. Bad timing. This needed more build.|n"
            )

        caller.msg(msg)
        target.msg(msg)
        if caller.location:
            caller.location.msg_contents(msg, exclude=[caller, target])

        # Start a feud
        _start_feud(caller, target)


class CmdFeud(Command):
    """
    View your current feuds with other players.

    Usage:
      feud
    """

    key = "feud"
    aliases = ["feuds", "rivalries"]
    locks = "cmd:all()"
    help_category = "PvP"

    def func(self):
        caller = self.caller
        feuds = caller.db.feuds or {}

        if not feuds:
            caller.msg("You have no active feuds.")
            return

        caller.msg("|w--- FEUDS ---|n")
        for rival_name, heat in feuds.items():
            if heat >= 80:
                heat_str = "|RWHITE HOT|n"
            elif heat >= 50:
                heat_str = "|yHot|n"
            elif heat >= 25:
                heat_str = "|ySimmering|n"
            else:
                heat_str = "|xCold|n"
            caller.msg(f"  |c{rival_name}|n — Heat: {heat}/100 ({heat_str})")


def _start_feud(char_a, char_b):
    """Start or escalate a feud between two characters."""
    if not hasattr(char_a.db, 'feuds') or char_a.db.feuds is None:
        char_a.db.feuds = {}
    if not hasattr(char_b.db, 'feuds') or char_b.db.feuds is None:
        char_b.db.feuds = {}

    # Start or increase feud heat
    a_feuds = char_a.db.feuds
    b_feuds = char_b.db.feuds

    a_feuds[char_b.key] = min(100, a_feuds.get(char_b.key, 0) + 25)
    b_feuds[char_a.key] = min(100, b_feuds.get(char_a.key, 0) + 25)

    char_a.db.feuds = a_feuds
    char_b.db.feuds = b_feuds
