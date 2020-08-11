from http import HTTPStatus
import json
import logging

import tornado.web
import tornado.websocket

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
        self.render(
            "index.html",
            static_url=self.static_url,
            full_url=self.request.full_url(),
        )


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
        if room.capacity == len(room.players.keys()):
            self.set_status(HTTPStatus.NOT_ACCEPTABLE)
            self.write("Room capacity reached")
            return
        if player_mod.name in room.players:
            success = room.move_player(player_mod.name, player_mod.team)
        else:
            success = room.add_player(player_mod.name, player_mod.team)
        if success:
            self.set_status(HTTPStatus.OK)
        else:
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)

    def delete(self, room_name):
        if room_name not in ROOMS:
            self.set_status(HTTPStatus.NOT_FOUND)
            self.write(f"{room_name} Does not exist")
            return
        room: Room = ROOMS[room_name]
        req_body = json.loads(self.request.body)
        name = req_body.get("name")
        if name and room:
            success = room.delete_player(name)
            if success:
                self.set_status(HTTPStatus.NO_CONTENT)
                return
            self.set_status(HTTPStatus.NOT_FOUND)
            self.write("Failed to delete")
        else:
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.write(f"Player Handler Delete {room_name}")


class GameHandler(tornado.web.RequestHandler):
    def get(self, room_name):
        self.set_status(HTTPStatus.OK)
        self.write(f"Game Handler get to {room_name}")

    def post(self, room_name):
        self.set_status(HTTPStatus.OK)
        if room_name not in ROOMS:
            self.set_status(HTTPStatus.NOT_FOUND)
            self.write(f"{room_name} Does not exist")
            return
        base_rsp = {"game_over": False, "reset": False}
        room: Room = ROOMS[room_name]
        req_body = json.loads(self.request.body)
        action = req_body.get("action")
        if action == "flip":
            idx = req_body.get("card_number")
            room.game_instance.process_turn(idx)
        if action == "reset":
            base_rsp["reset"] = True
        if room.game_instance.gameover:
            base_rsp["game_over"] = True
        # TODO: Trigger Websocket to send game state
        self.write(json.dumps(base_rsp))


class SocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        logging.info("socket opened")

    def on_message(self, message):
        message_body = None
        try:
            message_body = json.loads(message)
        except:
            logging.info(f"invalid action: {message}", exc_info=True)
        if not message_body:
            self.write_message(f"{message} is not an action")
            return

        
    def on_close(self):
        logging.info("socket closed")