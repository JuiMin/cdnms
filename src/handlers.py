from http import HTTPStatus
import json
import logging

import tornado.web

from serializer import CDNMSEncoder
from models import Room
import words

ROOMS = dict()


class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(HTTPStatus.OK)
        logging.info(ROOMS)
        self.write(
            f"Welcome to the cdnms API. {json.dumps(ROOMS, cls=CDNMSEncoder)}"
        )


class RoomHandler(tornado.web.RequestHandler):
    def get(self):
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
            r = Room(name)
            logging.info(r.name)
            logging.info(r.capacity)
            ROOMS[name] = r
            self.set_status(HTTPStatus.CREATED)
            self.write(f"Creating room {name}")
        except Exception as e:
            logging.info(str(e), exc_info=True)
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.write("Error creating room")


class PlayerHandler(tornado.web.RequestHandler):
    def get(self, room_name):
        self.set_status(HTTPStatus.OK)
        self.write(f"Player Handler room name get req: {room_name}")

    def post(self, room_name):
        self.set_status(HTTPStatus.OK)
        self.write(f"Player Handler Post to {room_name}")

    def delete(self, room_name):
        self.set_status(HTTPStatus.OK)
        self.write(f"Player Handler Delete {room_name}")


class GameHandler(tornado.web.RequestHandler):
    def get(self, room_name):
        self.set_status(HTTPStatus.OK)
        self.write(f"Game Handler get to {room_name}")

    def post(self, room_name):
        self.set_status(HTTPStatus.OK)
        self.write(f"Game Handler post to {room_name}")
