#!/usr/bin/env python3
import os

# external libs
import tornado.ioloop
import tornado.web

# cdnms imports
from lib.handlers import MainHandler, RoomHandler


def make_app():
    return tornado.web.Application([(r"/", MainHandler), (r"/room/([0-9]+)", RoomHandler)])


if __name__ == "__main__":
    # Get environment variables
    port = os.getenv("PORT", 443)
    print(f"Starting app on port: {port}")
    app = make_app()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
