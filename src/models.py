"""
Codenames model definitions
"""

from enum import Enum
import random
import logging
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
    __slots__ = ("cards", "gameover", "first", "second", "turn")

    def __init__(self):
        self.setup()

    def setup(self):
        self.turn = 0
        self.gameover = False
        # Set the first team randomly
        self.first = Team.BLUE
        self.second = Team.RED
        if random.sample(range(2), 1) == 1:
            self.first = Team.RED
            self.second = Team.RED

        # TODO: setup the game state for the round
        # Obtain random words from the wordbank
        card_range = set(range(25))
        t1_cards = set(random.sample(card_range, 9))
        t2_cards = set(random.sample(card_range - t1_cards, 8))
        death = set(random.sample((card_range - t1_cards) - t2_cards, 1))
        self.cards = []
        for idx, c in enumerate(random.sample(words.WORDBANK, k=25)):
            if idx in t1_cards:
                self.cards.append(Card(c, self.first))
            elif idx in t2_cards:
                self.cards.append(Card(c, self.second))
            elif idx in death:
                self.cards.append(Card(c, Team.DEATH))
            else:
                self.cards.append(Card(c, Team.NEUTRAL))

    def current_team(self):
        """
        The team whose turn it is
        """
        if self.turn % 2 == 0:
            return self.first
        return self.second

    def check_winner(self):
        first = 0
        second = 0

        for c in self.cards:
            if c.flipped:
                if c.association == self.first:
                    first += 1
                elif c.association == self.second:
                    second += 1
                elif c.association == Team.DEATH:
                    self.turn += 1
                    return self.current_team()
        if first == 9:
            return self.first
        elif second == 8:
            return self.second
        return None

    def process_turn(self, idx) -> bool:
        if idx < 0 or idx >= 25:
            return False
        c = self.cards[idx]
        c.flip()
        winner = self.check_winner()
        if not winner:
            self.turn += 1
        else:
            self.gameover = True


class Team(Enum):
    RED = 1
    BLUE = 0
    DEATH = 4
    NEUTRAL = 3
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
