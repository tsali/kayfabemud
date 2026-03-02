"""
Kayfabe: Protect the Business — Command sets.
"""

from evennia import default_cmds
from evennia.contrib.grid.ingame_map_display.ingame_map_display import CmdMap

# Career
from commands.career import CmdStats, CmdRank, CmdTurn, CmdTitles, CmdShows

# Contract
from commands.contract import CmdContract, CmdSign

# Championship
from commands.championship import CmdTitleShot

# Wrestling match
from commands.wrestling import (
    CmdWrestle, CmdWork, CmdSell, CmdComeback,
    CmdFinish, CmdKickout, CmdMoves, CmdCard, CmdHope,
)

# Promo
from commands.promo import CmdPromo

# Training
from commands.training import CmdTrain

# Travel
from commands.travel import CmdTravel

# PvP
from commands.pvp import CmdChallenge, CmdAccept, CmdTeam, CmdBetray, CmdFeud

# Manager
from commands.manager import CmdHire, CmdFire, CmdManagerPromo, CmdManagerInterfere

# Economy
from commands.economy import CmdBalance, CmdBuy, CmdSideJob, CmdMerch

# Social
from commands.social import CmdWho, CmdRoster, CmdRecord, CmdRespond, CmdSkipTutorial

# Stable
from commands.stable import CmdStable

# Lodging
from commands.lodging import CmdRest, CmdBoard, CmdPost, CmdBuyHouse, CmdGoHome, CmdUpgrade

# Brawl
from commands.brawl import CmdBrawl

# Character selection / creation
from commands.charselect import CmdCharSelect, CmdCharCreate

# System overrides
from commands.command import CmdNoMatch, CmdNoInput


class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The CharacterCmdSet — commands available to in-game characters.
    """

    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        super().at_cmdset_creation()

        # Career
        self.add(CmdStats())
        self.add(CmdRank())
        self.add(CmdTurn())
        self.add(CmdTitles())
        self.add(CmdShows())

        # Contract
        self.add(CmdContract())
        self.add(CmdSign())

        # Championship
        self.add(CmdTitleShot())

        # Wrestling
        self.add(CmdWrestle())
        self.add(CmdWork())
        self.add(CmdSell())
        self.add(CmdComeback())
        self.add(CmdFinish())
        self.add(CmdKickout())
        self.add(CmdMoves())
        self.add(CmdCard())
        self.add(CmdHope())

        # Promo
        self.add(CmdPromo())

        # Training
        self.add(CmdTrain())

        # Travel
        self.add(CmdTravel())

        # PvP
        self.add(CmdChallenge())
        self.add(CmdAccept())
        self.add(CmdTeam())
        self.add(CmdBetray())
        self.add(CmdFeud())

        # Manager
        self.add(CmdHire())
        self.add(CmdFire())
        self.add(CmdManagerPromo())
        self.add(CmdManagerInterfere())

        # Economy
        self.add(CmdBalance())
        self.add(CmdBuy())
        self.add(CmdSideJob())
        self.add(CmdMerch())

        # Social
        self.add(CmdWho())
        self.add(CmdRoster())
        self.add(CmdRecord())
        self.add(CmdRespond())
        self.add(CmdSkipTutorial())

        # Stable
        self.add(CmdStable())

        # Lodging
        self.add(CmdRest())
        self.add(CmdBoard())
        self.add(CmdPost())
        self.add(CmdBuyHouse())
        self.add(CmdGoHome())
        self.add(CmdUpgrade())

        # Brawl
        self.add(CmdBrawl())

        # Character management
        self.add(CmdCharSelect())
        self.add(CmdCharCreate())

        # Map (ASCII ingame map from compass exits)
        self.add(CmdMap())

        # System overrides
        self.add(CmdNoMatch())
        self.add(CmdNoInput())


class AccountCmdSet(default_cmds.AccountCmdSet):
    """Account-level commands."""

    key = "DefaultAccount"

    def at_cmdset_creation(self):
        super().at_cmdset_creation()


class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """Commands available before login."""

    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        super().at_cmdset_creation()


class SessionCmdSet(default_cmds.SessionCmdSet):
    """Session-level commands."""

    key = "DefaultSession"

    def at_cmdset_creation(self):
        super().at_cmdset_creation()
