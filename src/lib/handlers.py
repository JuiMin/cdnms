from http import HTTPStatus

import tornado.web
from tornado.escape import json_encode

from lib.constants import API_BASE

class MainHandler(tornado.web.RequestHandler):
    """
    handler for the homepage
    """
    def get(self):
        """
        Serves the homepage
        """
        data = {"api_base": API_BASE}
        self.render("../templates/home.html", **data)

    def post(self):
        """
        Endpoint for creating rooms
        """
        self.set_header("Content-Type", "application/json")

        # Create Room
        success = True

        """
        TODO: 
        - Implement room creation. Creates two relations
            - Room Key -> Room Data
            - Session Key -> Room Key
        """
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

        TODO:
        - Get current game state and connect to websocket
        """
        data = {"api_base": API_BASE, "room": room_id}
        self.render("../templates/room.html", **data)

    def patch(self):
        """
        Update a room's information 

        TODO: 
        - Make this endpoint handle updating the room
        - Results should be written out to the websockets/channels
        - UI will update based on the new room state
        """
        self.write("Patch a room")

    def delete(self):
        """
        Delete a room

        TODO:
        - Deletes the Room based on the Room key
        - This should happen when the last person leaves the room
        """
        self.write("Delete a room")
