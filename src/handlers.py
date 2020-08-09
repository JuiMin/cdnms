from http import HTTPStatus

import tornado.web

import words


class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(HTTPStatus.OK)
        self.write(f"Welcome to the cdnms API. {str(words.WORDBANK)}")


class RoomHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(HTTPStatus.OK)
        self.write(f"Websocket attached")

    def post(self):
        # TODO: write code for creating a room
        pass


class PlayerHandler(tornado.web.RequestHandler):
    def post(self):
        pass

    def delete(self):
        pass


class GameHandler(tornado.web.RequestHandler):
    def post(self):
        pass
