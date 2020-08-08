"""
Codenames model definitions
"""

import random
from typing import List

import words


class Player:
    __slots__ = "name"

    def __init__(self, name: str):
        self.name = name


class Codenames:
    __slots__ = "words"

    def __init__(self):
        self.setup()

    def setup(self):
        self.words = random.choices(words.WORDBANK, k=25)


class Room:
    __slots__ = (
        "capacity",
        "game_instance",
        "name",
        "red_team",
        "blue_team",
        "spectators",
    )

    def __init__(self, name: str, capacity: int = 10):
        self.capacity = capacity
        self.name = name
        self.game_instance = Codenames()
        self.red_team = []
        self.blue_team = []
        self.spectators = []
