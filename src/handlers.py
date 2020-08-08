from http import HTTPStatus

import tornado.web

import words


class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(HTTPStatus.OK)
        self.write(f"Welcome to the cdnms API. {str(words.WORDBANK)}")

