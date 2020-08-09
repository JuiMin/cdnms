from http import HTTPStatus
import json
import logging

import tornado.web

from serializer import CDNMSEncoder
from models import Room, Team
import words

ROOMS = dict()


class DebugHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(HTTPStatus.OK)
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(ROOMS, cls=CDNMSEncoder))


class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(HTTPStatus.OK)
        self.write(f"Welcome to the cdnms API.")


class RoomHandler(tornado.web.RequestHandler):
    def get(self):
        # TODO MAKE THIS PROPERLY
        self.set_status(HTTPStatus.OK)
        self.write(f"Websocket attached")

    def post(self):
        # TODO: write code for creating a room
        self.set_status(HTTPStatus.OK)
        req_body = json.loads(self.request.body)
        try:
            name = req_body.get("name")
            if name in ROOMS:
                self.set_status(HTTPStatus.CONFLICT)
                self.write("Room already exists")
                return
            ROOMS[name] = Room(name)
            self.set_status(HTTPStatus.CREATED)
            self.write(f"Creating room {name}")
        except Exception as e:
            logging.info(str(e), exc_info=True)
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.write("Error creating room")


class PlayerHandler(tornado.web.RequestHandler):
    def get(self, room_name):
        self.set_status(HTTPStatus.OK)
        self.write(f"Player Handler GET to {room_name}")

    def post(self, room_name):
        class PlayerMod:
            def __init__(self, body):
                self.name = str(body.get("name"))
                team = body.get("team")
                if isinstance(team, int):
                    if team == 0:
                        team = Team.BLUE
                    elif team == 1:
                        team = Team.RED
                    else:
                        team = Team.SPECTATOR
                elif isinstance(team, str):
                    team = team.lower()
                    if team == "blue":
                        team = Team.BLUE
                    elif team == "red":
                        team = Team.RED
                    else:
                        team = Team.SPECTATOR
                else:
                    team = Team.SPECTATOR
                self.team = team

        if room_name not in ROOMS:
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.write(f"{room_name} Does not exist")
            return
        player_mod = None
        try:
            player_mod = json.loads(self.request.body, object_hook=PlayerMod)
        except KeyError as e:
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.write(f"Request body incorrect format: {str(e)}")
            return
        except Exception:
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.write(str(e))
            return
        room: Room = ROOMS[room_name]
        room.players[player_mod.name] = player_mod.team
        self.set_status(HTTPStatus.OK)
        self.write(f"Player added")

    def delete(self, room_name):
        # TODO MAKE THIS PROPERLY
        self.set_status(HTTPStatus.OK)
        self.write(f"Player Handler Delete {room_name}")


class GameHandler(tornado.web.RequestHandler):
    def get(self, room_name):
        self.set_status(HTTPStatus.OK)
        self.write(f"Game Handler get to {room_name}")

    def post(self, room_name):
        self.set_status(HTTPStatus.OK)
        self.write(f"Game Handler post to {room_name}")
