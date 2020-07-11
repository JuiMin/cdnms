#!/usr/bin/env python3
import os

# external libs
import tornado.ioloop
import tornado.web

# cdnms imports
from lib.constants import PORT
from lib.handlers import MainHandler, RoomHandler


def generate_tornado_settings():
    return {
        "static_path": os.path.join(os.path.dirname(__file__), "js"),
        "static_url_prefix": "/resources/"
    }

def make_app():
    routes = [(r"/", MainHandler), (r"/room/([0-9]+)", RoomHandler)]
    settings = generate_tornado_settings()
    print(settings)
    return tornado.web.Application(routes,**settings)


if __name__ == "__main__":
    app = make_app()
    print(f"Starting app on port: {PORT}")
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
