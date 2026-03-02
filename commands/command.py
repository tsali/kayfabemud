"""
Kayfabe: Protect the Business -- Base command class.

Adds a "> " prompt after each command via at_post_cmd.
Also provides custom no-match/no-input handlers and a
continue-then-look helper for paged output (board, card).
"""

from evennia.commands.default.muxcommand import MuxCommand
from evennia.commands.command import Command as BaseCommand
from evennia.utils.evmenu import get_input


class Command(MuxCommand):
    """Base command class for Kayfabe. Adds input prompt."""

    def at_post_cmd(self):
        """Send a > prompt after each command."""
        if hasattr(self.caller, "msg"):
            self.caller.msg(text="> ", options={"send_prompt": True})


def _show_room(caller):
    """Show the room appearance + prompt without execute_cmd."""
    loc = caller.location
    if loc:
        caller.msg(loc.return_appearance(caller))
    caller.msg(text="> ", options={"send_prompt": True})


def _continue_then_look(caller, prompt, result):
    """Callback for get_input: shows room directly (avoids cmdhandler)."""
    _show_room(caller)
    return False


def pause_then_look(caller):
    """Show 'Press ENTER to continue...' then re-display the room."""
    get_input(caller, "\n|w[Press ENTER to continue...]|n", _continue_then_look)


class CmdNoMatch(BaseCommand):
    """
    Called when no command match is found. Shows error, waits for
    ENTER, then re-shows the room.
    """

    key = "__nomatch_command"
    locks = "cmd:all()"

    def func(self):
        raw = self.raw_string.strip()
        self.caller.msg(f"|rCommand '{raw}' is not available. Type \"help\" for help.|n")
        pause_then_look(self.caller)


class CmdNoInput(BaseCommand):
    """
    Called when the user presses ENTER with no input.
    Re-shows room directly.
    """

    key = "__noinput_command"
    locks = "cmd:all()"

    def func(self):
        _show_room(self.caller)
