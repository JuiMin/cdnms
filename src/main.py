#!/usr/bin/env python3.8

"""
main.py is the entry point and starting script for the CDNMS server.

This file should start the tornado process and do whatever configuration is
required
"""

import asyncio
import logging
import os

import tornado.ioloop
import tornado.web
import tornado.autoreload

from handlers import cdnms_routes
import words

DIRECTORY_PATH = os.path.dirname(__file__)


def perform_setup():
    # ENABLE WINDOWS COMPATABILITY
    if os.name == "nt":
        # On Windows, Tornado requires the WindowsSelectorEventLoop
        # Python 3.8 defaults to a different one
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Load Initial Word Listing
    words.WORDBANK = words.load_words()

    # SETUP LOG LEVEL
    logging.basicConfig(level=logging.DEBUG)


def generate_tornado_settings():
    settings = {
        "debug": True,
        "template_path": os.path.join(DIRECTORY_PATH, "templates"),
        "static_path": os.path.join(DIRECTORY_PATH, "static"),
    }
    HOSTSERVER = os.getenv("HOSTSERVER", "localhost")
    if HOSTSERVER == "localhost":
        settings["autoreload"] = True
    return settings


def make_app():
    routes = cdnms_routes
    settings = generate_tornado_settings()
    return tornado.web.Application(routes, **settings)


if __name__ == "__main__":
    # Perform any configuration steps before main logic
    perform_setup()

    # LOAD ENVIRONMENT VARIABLES
    HOSTSERVER = os.getenv("HOSTSERVER", "localhost")
    PORT = os.getenv("PORT", 8283)

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
    app.listen(PORT)
    logging.info(f"Starting cdnms on port: {PORT}")
    tornado.ioloop.IOLoop.current().start()

