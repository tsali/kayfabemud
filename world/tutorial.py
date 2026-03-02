"""
Kayfabe: Protect the Business — Learning the Ropes (Tutorial).

After chargen confirm (before picking a starting fed), new players
go through a guided tutorial match:
1. "Try `work`" — basic attack
2. "Try `sell`" — selling for opponent
3. "`hope`" — hope spot
4. "`comeback`" — comeback sequence
5. "`finish`" — hit your finisher

Tutorial opponent: "The Training Dummy" (can't lose).
`skip` command to bypass.
After tutorial: chargen continues with starting fed selection.
"""

import random
from evennia.scripts.scripts import DefaultScript
from evennia.utils import logger


TUTORIAL_STEPS = [
    {
        "phase": "opening",
        "command": "work",
        "prompt": (
            "\n|w=== LEARNING THE ROPES ===|n\n\n"
            "Welcome to your first match! You're in the ring with\n"
            "|cThe Training Dummy|n — a practice partner who'll help\n"
            "you learn the ropes before you head out to your first fed.\n\n"
            "In wrestling, matches have 5 phases:\n"
            "  |wOpening|n -> |rHeat|n -> |yHope|n -> |gComeback|n -> |wFinish|n\n\n"
            "We're in the |wOpening|n phase. Try attacking!\n\n"
            "Type |wwork|n to execute a wrestling move.\n"
            "|x(Type |wskip|x to skip the tutorial)|n"
        ),
    },
    {
        "phase": "opening",
        "command": "sell",
        "prompt": (
            "\n|wNice! You connected!|n\n\n"
            "But wrestling isn't just about hitting moves — it's about\n"
            "making your opponent look good too. That's called |wselling|n.\n\n"
            "When you |wsell|n, you let your opponent get offense in.\n"
            "This builds crowd heat and match quality.\n\n"
            "Type |wsell|n to sell for The Training Dummy."
        ),
    },
    {
        "phase": "heat",
        "command": "hope",
        "prompt": (
            "\n|wGood selling! The crowd is getting into it.|n\n\n"
            "Now we're in the |rHeat Segment|n. The villain is dominating.\n"
            "But the crowd wants to see a |yHope Spot|n — a brief\n"
            "flash of fight from the hero!\n\n"
            "Type |whope|n to fire back briefly."
        ),
    },
    {
        "phase": "comeback",
        "command": "comeback",
        "prompt": (
            "\n|yThe crowd stirs!|n\n\n"
            "Now it's time for |gThe Comeback|n! This is the moment\n"
            "the crowd has been waiting for. You fire up, feed off\n"
            "the energy, and turn the match around!\n\n"
            "Type |wcomeback|n to fire up!"
        ),
    },
    {
        "phase": "finish",
        "command": "finish",
        "prompt": (
            "\n|gYOU'RE FIRED UP! The crowd is going crazy!|n\n\n"
            "This is it — |wThe Finish|n. Time to hit your finisher\n"
            "and pin The Training Dummy!\n\n"
            "Type |wfinish|n to hit your finisher!"
        ),
    },
]


class TutorialMatchScript(DefaultScript):
    """
    A simplified match script for the tutorial.
    The player always wins. Steps guide them through each command.
    """

    def at_script_creation(self):
        self.key = "tutorial_match"
        self.desc = "Tutorial match"
        self.persistent = False
        self.interval = 0

        self.db.wrestler = None
        self.db.step = 0
        self.db.completed = False

    def setup_tutorial(self, wrestler):
        """Initialize the tutorial match."""
        self.db.wrestler = wrestler
        self.db.step = 0
        self.db.completed = False

        # Show first step
        step = TUTORIAL_STEPS[0]
        wrestler.msg(step["prompt"])

    def process_command(self, command_name):
        """
        Process a tutorial command. Returns True if command was handled.
        """
        wrestler = self.db.wrestler
        if not wrestler or self.db.completed:
            return False

        step_idx = self.db.step or 0
        if step_idx >= len(TUTORIAL_STEPS):
            return False

        current_step = TUTORIAL_STEPS[step_idx]

        # Check if the right command was used
        if command_name != current_step["command"]:
            wrestler.msg(
                f"|yTutorial hint: Try |w{current_step['command']}|y right now.|n\n"
                f"|x(Type |wskip|x to skip the tutorial)|n"
            )
            return True

        # Execute the step with flavor text
        self._execute_step(wrestler, step_idx, command_name)

        # Advance to next step
        self.db.step = step_idx + 1

        if self.db.step >= len(TUTORIAL_STEPS):
            # Tutorial complete
            self._complete_tutorial(wrestler)
        else:
            # Show next step prompt
            next_step = TUTORIAL_STEPS[self.db.step]
            wrestler.msg(next_step["prompt"])

        return True

    def _execute_step(self, wrestler, step_idx, command):
        """Execute a tutorial step with appropriate feedback."""
        name = wrestler.key
        dummy = "The Training Dummy"

        if command == "work":
            finisher_name = wrestler.db.finisher_name or "a move"
            wrestler.msg(
                f"|c{name} hits {dummy} with a solid move!|n\n"
                f"The crowd nods appreciatively."
            )
        elif command == "sell":
            wrestler.msg(
                f"|c{dummy} lands a clothesline on {name}!|n\n"
                f"{name} sells it like they got hit by a truck.\n"
                f"|yThe crowd heat rises!|n"
            )
        elif command == "hope":
            wrestler.msg(
                f"|y{name} fires back with a quick punch!|n\n"
                f"But {dummy} cuts them off! Not yet...\n"
                f"The crowd groans but they're hooked."
            )
        elif command == "comeback":
            wrestler.msg(
                f"|g{name} is FIRING UP! The crowd is on their feet!|n\n"
                f"{name} hits move after move! {dummy} is reeling!"
            )
        elif command == "finish":
            finisher = wrestler.db.finisher_name or "Finisher"
            wrestler.msg(
                f"\n|Y{name} hits the {finisher}!!!\n"
                f"COVER! ONE! TWO! THREE!!!\n\n"
                f"*** {name} WINS! ***|n"
            )

    def _complete_tutorial(self, wrestler):
        """End the tutorial and continue chargen (starting fed selection)."""
        self.db.completed = True

        # Award small XP bonus
        wrestler.db.xp = (wrestler.db.xp or 0) + 10

        wrestler.msg(
            f"\n|w{'=' * 44}|n\n"
            f"|w  YOU LEARNED THE ROPES!|n\n"
            f"|w{'=' * 44}|n\n"
            f"  You've learned the basics of working a match:\n"
            f"  |wwork|n     — Execute a move\n"
            f"  |wsell|n     — Let your opponent shine\n"
            f"  |whope|n     — Brief fight back during heat\n"
            f"  |wcomeback|n — Mount your comeback\n"
            f"  |wfinish|n   — Hit your finisher to win\n\n"
            f"  Bonus: |c+10 XP|n for completing the tutorial.\n\n"
            f"  Now let's pick where you're going to start your career.\n"
            f"|w{'=' * 44}|n\n"
        )

        # Clean up
        wrestler.ndb.in_tutorial = False
        self.stop()

        # Continue chargen — launch starting fed selection
        _resume_chargen_after_tutorial(wrestler)

    def skip_tutorial(self):
        """Skip the tutorial entirely."""
        wrestler = self.db.wrestler
        if wrestler:
            wrestler.msg("|yTutorial skipped. You're on your own, kid.|n")
            wrestler.ndb.in_tutorial = False
            # Continue chargen — launch starting fed selection
            _resume_chargen_after_tutorial(wrestler)
        self.db.completed = True
        self.stop()


def _resume_chargen_after_tutorial(wrestler):
    """After tutorial completes or is skipped, launch the starting fed EvMenu."""
    from evennia.utils.evmenu import EvMenu
    EvMenu(
        wrestler,
        "commands.chargen",
        startnode="node_starting_fed",
        cmd_on_exit=None,
    )
