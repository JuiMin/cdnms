"""
Codenames model definitions
"""

from enum import Enum
import random
from typing import Dict, List

import words


class Card:
    __slots__ = ("flipped", "value", "association")

    def __init__(self, value, association):
        self.value = value
        self.association = association
        self.flipped = False

    def flip(self):
        self.flipped = True


class Codenames:
    __slots__ = ("cards", "gameover")

    def __init__(self):
        self.setup()

    def setup(self):
        self.gameover = False
        self.cards = random.choices(words.WORDBANK, k=25)


class Team(Enum):
    RED = 1
    BLUE = 0


class Room:
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
