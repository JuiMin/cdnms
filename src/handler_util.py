"""
handler_util.py is for anything handlers and endpoint implementation requires

"""
from http import HTTPStatus
from typing import Callable, Dict

SUBSCRIBE = "subscribe"
FLIP_CARD = "flip_card"
ADD_PLAYER = "add_player"
REMOVE_PLAYER = "remove_player"
MOVE_PLAYER = "move_player"
RESET_GAME = "reset_game"
ALLOWED_ACTIONS = (
    FLIP_CARD,
    ADD_PLAYER,
    REMOVE_PLAYER,
    SUBSCRIBE,
    MOVE_PLAYER,
    RESET_GAME,
)


class CDNMSResponse(object):
    __slots__ = ("body", "status")

    def __init__(self, status: HTTPStatus, body: Dict):
        self.status = status
        self.body = body


class CDNMSCommand(object):
    __slots__ = ("action", "params", "room_id", "client_id")

    def __init__(self, message: Dict):
        self.action = message["action"]
        self.room_id = message["room_id"]
        self.client_id = message["client_id"]
        self.params = message["params"]
        if self.action not in ALLOWED_ACTIONS:
            raise Exception(f"{self.action} unsupported")


class CDNMSCommandResult(object):
    __slots__ = ("success", "result")

    def __init__(self, success: bool, result: Dict):
        self.success = success
        self.result = result
