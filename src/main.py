#!/usr/bin/env python3.8
import argparse
import os
import asyncio

# external libs
import tornado.ioloop
import tornado.web

# cdnms imports
import words
from handlers import RootHandler


def generate_tornado_settings():
    return {}


def make_app():
    routes = [(r"/", RootHandler)]
    settings = generate_tornado_settings()
    return tornado.web.Application(routes, **settings)


if __name__ == "__main__":
    if (os.name == 'nt'):
        # on Windows, Tornado requires the WindowsSelectorEventLoop - Python 3.8 defaults to a different one
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) 
    parser = argparse.ArgumentParser()
    parser.parse_args()
    # Load env variables
    # First load ENV Variables
    HOSTSERVER = os.getenv("HOSTSERVER", "localhost")
    PORT = os.getenv("PORT", 443)
    # Load wordbank
    words.WORDBANK = words.load_words()
    # Constructed constants
    _transfer_protocol = "http" if HOSTSERVER == "localhost" else "https"
    API_BASE = f"{_transfer_protocol}://{HOSTSERVER}:{PORT}/"

    # App start
    app = make_app()
    print(f"Starting cdnms on port: {PORT}")
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
    