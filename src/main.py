#!/usr/bin/env python3.8
import asyncio
import logging
import os
import pathlib


# external libs
import tornado.ioloop
import tornado.web
import tornado.autoreload

# cdnms imports
import words
from handlers import (
    DebugHandler,
    GameHandler,
    RootHandler,
    RoomHandler,
    PlayerHandler,
)

PARENT_DIRECTORY_PATH = pathlib.Path(__file__).resolve().parents[1]


def generate_tornado_settings():
    settingsDict = {
        "template_path": os.path.join(PARENT_DIRECTORY_PATH, "templates"),
        "static_path": os.path.join(PARENT_DIRECTORY_PATH, "static"),
    }
    HOSTSERVER = os.getenv("HOSTSERVER", "localhost")
    if HOSTSERVER == "localhost":
        settingsDict["autoreload"] = True
    return settingsDict


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

    # Add autoreload to bundle.js for client development
    if HOSTSERVER == "localhost":
        tornado.autoreload.start()
        for root, dir, files in os.walk(
            os.path.join(PARENT_DIRECTORY_PATH, "static/dist")
        ):
            for f in files:
                tornado.autoreload.watch(root + "/" + f)

    # App start
    app = make_app()
    logging.info(f"Starting cdnms on port: {PORT}")
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()

