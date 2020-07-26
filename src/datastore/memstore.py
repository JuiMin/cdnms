# memstore implements an interface

from datastore.datastore import Datastore
from models.codenames import Player


class Memstore(Datastore):
    def __init__(self):
        self.users = {}
        self.games = {}

    def add_user(self, session_id, username):
        try:
            if session_id in self.users:
                return {"error_message": "User already exists"}
            else:
                p = Player(username)
                self.users[session_id] = p
                return {"status": "success", "player": p}
        except Exception as e:
            return {"error_message": str(e)}
