#!/usr/bin/env python3
import os

# external libs
import tornado.ioloop
import tornado.web

# cdnms imports
from lib.handlers import MainHandler, RoomHandler


def make_app():
    routes = [(r"/", MainHandler), (r"/room/([0-9]+)", RoomHandler)]
    return tornado.web.Application(routes)


if __name__ == "__main__":
    # Get environment variables
    port = os.getenv("PORT", 443)
    app = make_app()
    print(f"Starting app on port: {port}")
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
