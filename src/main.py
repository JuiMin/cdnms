#!/usr/bin/env python3.8
import asyncio
import logging
import os
import pathlib


# external libs
import tornado.ioloop
import tornado.web

# cdnms imports
import words
from handlers import (
    DebugHandler,
    GameHandler,
    RootHandler,
    RoomHandler,
    PlayerHandler,
)


def generate_tornado_settings():
    p = pathlib.Path(__file__).resolve().parents[1]
    return {
        "template_path": os.path.join(p, "templates"),
        "static_path": os.path.join(p, "static"),
    }


def make_app():
    routes = [
        (r"/", RootHandler),
        (r"/debug", DebugHandler),
        (r"/rooms", RoomHandler),
        (r"/rooms/(\w+)", GameHandler),
        (r"/rooms/(\w+)/players", PlayerHandler),
    ]
    settings = generate_tornado_settings()
    return tornado.web.Application(routes, **settings)


if __name__ == "__main__":
    if os.name == "nt":
        # on Windows, Tornado requires the WindowsSelectorEventLoop - Python 3.8 defaults to a different one
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # Setup logging
    logging.basicConfig(level=logging.DEBUG)
    # Load env variables
    # First load ENV Variables
    HOSTSERVER = os.getenv("HOSTSERVER", "localhost")
    PORT = os.getenv("PORT", 443)
    # Load wordbank
    words.WORDBANK = words.load_words()
    logging.info(f"Loaded {len(words.WORDBANK)} words into memory.")
    # Constructed constants
    _transfer_protocol = "http" if HOSTSERVER == "localhost" else "https"
    API_BASE = f"{_transfer_protocol}://{HOSTSERVER}:{PORT}/"

    # App start
    app = make_app()
    logging.info(f"Starting cdnms on port: {PORT}")
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()

