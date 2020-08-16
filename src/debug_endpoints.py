"""
endpoints.py holds all the endpoint calling code to be used by handlers

"""
from http import HTTPStatus
from typing import Dict

from handler_util import CDNMSResponse
from datastore import GameStorage

import endpoints

DEBUG_STORE = endpoints.GAMESTORE


def get_debug() -> CDNMSResponse:
    return CDNMSResponse(HTTPStatus.OK, DEBUG_STORE._internal_storage)


def post_debug(body: Dict) -> CDNMSResponse:
    return CDNMSResponse(HTTPStatus.OK, {"a": "b"})


def get_rooms_test(room_id: str) -> CDNMSResponse:
    return CDNMSResponse(HTTPStatus.OK, {"room_id": room_id})


def post_rooms_test(room_id: str, body: Dict) -> CDNMSResponse:
    return CDNMSResponse(HTTPStatus.OK, {"room_id": room_id, "body": body})


DEBUG_ENDPOINT_MAPPING = {
    "response": {
        r"/debug": {"GET": get_debug, "POST": post_debug},
        r"/debug/rooms/(\w+)": {"GET": get_rooms_test, "POST": post_rooms_test},
    },
}
