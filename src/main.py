#!/usr/bin/env python3.8
import asyncio
import logging
import os

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

DIRECTORY_PATH = os.path.dirname(__file__)


def generate_tornado_settings():
    settingsDict = {
        "template_path": os.path.join(DIRECTORY_PATH, "templates"),
        "static_path": os.path.join(DIRECTORY_PATH, "static"),
    }
    HOSTSERVER = os.getenv("HOSTSERVER", "localhost")
    if HOSTSERVER == "localhost":
        settingsDict["autoreload"] = True
    return settingsDict


def preflight_operations():
    # ENABLE WINDOWS COMPATABILITY
    if os.name == "nt":
        # on Windows, Tornado requires the WindowsSelectorEventLoop - Python 3.8 defaults to a different one
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # SETUP LOG LEVEL
    logging.basicConfig(level=logging.DEBUG)


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
    preflight_operations()

    # LOAD ENVIRONMENT VARIABLES
    HOSTSERVER = os.getenv("HOSTSERVER", "localhost")
    PORT = os.getenv("PORT", 8283)

    # Load wordbank
    words.WORDBANK = words.load_words()
    logging.info(f"Loaded {len(words.WORDBANK)} words into memory.")

    # Add autoreload to bundle.js for client development
    if HOSTSERVER == "localhost":
        tornado.autoreload.start()
        for root, _, files in os.walk(
            os.path.join(DIRECTORY_PATH, "static/dist")
        ):
            for f in files:
                tornado.autoreload.watch(root + "/" + f)

    # App start
    app = make_app()
    logging.info(f"Starting cdnms on port: {PORT}")
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()

