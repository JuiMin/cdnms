import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("<h1>Codenames Game</h1>\n" "<div>Whatever</div>")


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
