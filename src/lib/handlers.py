from http import HTTPStatus

import tornado.web
from tornado.escape import json_encode

from lib.constants import API_BASE

class MainHandler(tornado.web.RequestHandler):
    """
    handler for the homepage
    """
    def get(self):
        data = {"api_base": API_BASE}
        self.render("../templates/home.html", **data)

    def post(self):
        self.set_header("Content-Type", "application/json")

        # Create Room
        success = True
        # Select rsp
        if success == True:
            self.set_status(HTTPStatus.CREATED)
            x = {
                "room_id": 12312321
            }
            self.write(json_encode(x))


class RoomHandler(tornado.web.RequestHandler):
    """
    Room handler should address creation/teardown of rooms
    """

    def get(self, room_id):
        """
        This should get the room state by ID
        """
        data = {"api_base": API_BASE, "room": room_id}
        self.render("../templates/room.html", **data)

    def post(self):
        """
        Create a room
        """
        self.write("post to room")

    def patch(self):
        """
        Update a room's information 
        """
        self.write("Patch a room")

    def delete(self):
        """
        Delete a room
        """
        self.write("Delete a room")
