"""
Codenames model definitions
"""

from enum import Enum
import random
from typing import Dict, List

import words


class Card(object):
    __slots__ = ("flipped", "value", "association")

    def __init__(self, value, association):
        self.value = value
        self.association = association
        self.flipped = False

    def flip(self):
        self.flipped = True


class Codenames(object):
    __slots__ = ("cards", "gameover")

    def __init__(self):
        self.setup()

    def setup(self):
        self.gameover = False
        # TODO: setup the game state for the round
        # Obtain random words from the wordbank
        # cards = random.choices(words.WORDBANK, k=25)
        self.cards = ()


class Team(Enum):
    RED = 1
    BLUE = 0
    SPECTATOR = 2


class Room(object):
    __slots__ = (
        "capacity",
        "game_instance",
        "name",
        "players",
    )

    def __init__(self, name: str, capacity: int = 10):
        self.capacity = capacity
        self.name = name
        self.game_instance = Codenames()
        # TEAMS
        self.players: Dict[str, Team] = {}

    def add_player(self, name, team) -> bool:
        if name in self.players:
            return False
        self.players[name] = team
        return True

    def move_player(self, name, team) -> bool:
        if name not in self.players:
            return False
        self.players[name] = team
        return True

    def delete_player(self, name) -> bool:
        try:
            del self.players[name]
        except Exception:
            return False
        return True
