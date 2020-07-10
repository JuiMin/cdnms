from typing import List

# Room logic percolates down
# Each room should have two teams and those teams should know their players
class Room:
    def __init__(self, name, creator, creator_team=1):
        self.name = name
        self.red_team = Team("Red Team")
        self.blue_team = Team("Blue Team")
        # A single player
        self.creator: Player = creator


class Team:
    def __init__(self, name):
        self.name = name
        self.spy_master = None
        self.members = None


class Player:
    def __init__(self, nickname, team):
        self.nickname: str = nickname
        self.team = team
