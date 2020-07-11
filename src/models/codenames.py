from enum import Enum

class Team(Enum):
    RED = 0
    BLUE = 1


class Player:
    def __init__(self, name):
        self.name = name


# Room logic percolates down
# Each room should have two teams and those teams should know their players
class GameRoom:
    def __init__(self, name, creator_id, creator_team=Team.RED):
        self.name = name
        self.red_team = {}
        self.blue_team = {}
        self.creator_id = creator_id
        self.add_player(creator_team, creator_id, )
        self.blue_spymaster = None
        self.red_spymaster = None

    def add_player(self, team, cookie_id, player):
        if team == TeamName.RED and cookie_id not in self.red_team:
            if cookie_id in self.blue_team:
                del self.blue_team[cookie_id]
            self.red_team[cookie_id] = player
        elif team == TeamName.BLUE and cookie_id not in self.blue_team:
            if cookie_id in self.red_team:
                del self.red_team[cookie_id]
            self.blue_team[cookie_id] = player



