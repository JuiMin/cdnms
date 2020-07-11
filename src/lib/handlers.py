import tornado.web

from lib.constants import HOSTSERVER

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        data = {"hostserver": HOSTSERVER}
        self.render("../templates/home.html", **data)


class RoomHandler(tornado.web.RequestHandler):
    """
    Room handler should address creation/teardown of rooms
    """

    def get(self, room_id=None):
        """
        This should get the room state by ID
        """
        self.write(f"get from room. ID = {room_id}")

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
