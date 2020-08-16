"""
endpoints.py holds all the endpoint calling code to be used by handlers

"""
from http import HTTPStatus
from typing import Dict
import json
import logging

from tornado.websocket import WebSocketHandler

from handler_util import (
    CDNMSCommand,
    CDNMSCommandResult,
    CDNMSResponse,
    SUBSCRIBE,
    FLIP_CARD,
    ADD_PLAYER,
    REMOVE_PLAYER,
    MOVE_PLAYER,
    RESET_GAME,
)

from datastore import ClientStorage, GameStorage
from serializer import CDNMSEncoder

GAMESTORE = GameStorage()
CLIENTSTORE = ClientStorage()


def post_rooms(body: Dict) -> CDNMSResponse:
    room_name = body.get("room_name")
    if not room_name:
        return CDNMSResponse(
            HTTPStatus.BAD_REQUEST, {"error": "No room_name supplied."}
        )
    response = GAMESTORE.create_room(room_name)
    return CDNMSResponse(HTTPStatus.OK, response)


def get_specific_room(room_id: str) -> CDNMSResponse:
    response = GAMESTORE.get_room(room_id)
    logging.info(room_id)
    return CDNMSResponse(HTTPStatus.OK, response)


def _handle_subscribe(room_id, client):
    return CLIENTSTORE.add_subscriber(room_id, client)


def _handle_flip_card(room_id, card_index: int):
    response = GAMESTORE.get_room(room_id)
    if not response.success:
        return response
    room = response.data
    success = room.make_turn(card_index)
    if success:
        return GAMESTORE.update_room(room_id, room)
    return success


def _handle_reset_game(room_id):
    response = GAMESTORE.get_room(room_id)
    if not response.success:
        return response
    room = response.data
    room.reset_game()
    return GAMESTORE.update_room(room_id, room)


def _handle_add_player(room_id, player_name):
    response = GAMESTORE.get_room(room_id)
    if not response.success:
        return response
    room = response.data
    success = room.add_player(player_name)
    if success:
        return GAMESTORE.update_room(room_id, room)
    return success


def _handle_remove_player(room_id, player_name):
    response = GAMESTORE.get_room(room_id)
    if not response.success:
        return response
    room = response.data
    success = room.delete_player(player_name)
    if success:
        return GAMESTORE.update_room(room_id, room)
    return success


def _handle_move_player(room_id, player_name, team):
    response = GAMESTORE.get_room(room_id)
    if not response.success:
        return response
    room = response.data
    success = room.move_player(player_name, team)
    if success:
        return GAMESTORE.update_room(room_id, room)
    return success


def default_ws(command: CDNMSCommand, handler) -> CDNMSCommandResult:
    action = command.action
    result = None
    if action == SUBSCRIBE:
        result = _handle_subscribe(command.room_id, handler)
    elif action == FLIP_CARD:
        result = _handle_flip_card(
            command.room_id, command.params.get("card_index")
        )
    elif action == ADD_PLAYER:
        result = _handle_add_player(
            command.room_id, command.params.get("player_name")
        )
    elif action == REMOVE_PLAYER:
        result = _handle_remove_player(
            command.room_id, command.params.get("player_name")
        )
    elif action == MOVE_PLAYER:
        result = _handle_move_player(
            command.room_id,
            command.params.get("player_name"),
            command.params.get("team"),
        )
    elif action == RESET_GAME:
        result = _handle_reset_game(command.room_id)
    else:
        return CDNMSCommandResult(False, {"error": "invalid command"})

    if result is not None:
        subs = CLIENTSTORE.get_subscribers_for_room(command.room_id)
        if isinstance(subs, dict):
            for handler in subs.values():
                handler.write_message(json.dumps(result, cls=CDNMSEncoder))
            return CDNMSCommandResult(True, {})

    # Write to user
    return CDNMSCommandResult(False, {"error": "No result", "command": command})


ENDPOINT_MAPPING = {
    "response": {r"/rooms": {"GET": get_specific_room, "POST": post_rooms},},
    "websocket": {r"/ws": {"DEFAULT": default_ws,}},
}

