"""
datastore.py implements that in memory data storage components

"""
from collections import defaultdict
import json
import logging
from typing import Any, Dict, List
import uuid

from models import Room


class StorageResponse(object):
    __slots__ = ("success", "data", "message")

    def __init__(
        self, success: bool = True, data: Any = None, message: str = None
    ):
        self.success = success
        self.data = data
        self.message = message


class GameStorage:
    """
    GameStorage stores all rooms and games within
    """

    def __init__(self):
        self._internal_storage: Dict[str, Room] = dict()

    def create_room(self, room_name: str) -> StorageResponse:
        if not room_name:
            return StorageResponse(False)
        room_id = uuid.uuid4().hex
        while room_id in self._internal_storage:
            room_id = uuid.uuid4().hex
        try:
            room = Room(room_name)
            self._internal_storage[room_id] = room
            return StorageResponse(data={"room_id": str(room_id)})
        except Exception as e:
            logging.error(str(e), exc_info=True)
            return StorageResponse(False, message=str(e))

    def remove_room(self, room_id: str) -> StorageResponse:
        if room_id not in self._internal_storage:
            return StorageResponse(False, message="Room does not exist.")
        try:
            del self._internal_storage[room_id]
            return StorageResponse()
        except Exception as e:
            logging.error(str(e), exc_info=True)
            return StorageResponse(False, message=str(e))

    def get_room(self, room_id: str) -> StorageResponse:
        if room_id not in self._internal_storage:
            return StorageResponse(False, message="Room does not exist.")
        try:
            room_instance = self._internal_storage[room_id]
            return StorageResponse(data=room_instance)
        except Exception as e:
            logging.error(str(e), exc_info=True)
            return StorageResponse(False, message=str(e))

    def update_room(self, room_id: str, new_room: Room) -> StorageResponse:
        if room_id not in self._internal_storage:
            return StorageResponse(False, message="Room does not exist.")
        try:
            self._internal_storage[room_id] = new_room
            return StorageResponse(data=new_room)
        except Exception as e:
            return StorageResponse(False, message=str(e))


class ClientStorage:
    def __init__(self):
        self._internal_storage: Dict[uuid.UUID, List[Any]] = defaultdict(dict)

    def add_subscriber(self, room_id: str, client):
        try:
            client_id = uuid.uuid4().hex
            while client_id in self._internal_storage[room_id]:
                client_id = uuid.uuid4().hex
            self._internal_storage[room_id][client_id] = client
            return StorageResponse(True, data={"client_id": client_id})
        except Exception as e:
            return StorageResponse(False, message=str(e))

    def remove_subscriber(self, room_id: str, client_id: str):
        try:
            del self._internal_storage[room_id][client_id]
            return StorageResponse()
        except Exception as e:
            return StorageResponse(False, message=str(e))

    def get_subscribers_for_room(self, room_id: str):
        try:
            subs = self._internal_storage[room_id]
            # prune any dead conns
            for client_id, handler in subs.items():
                if handler.ws_connection == None:
                    del self._internal_storage[room_id][client_id]
            return subs
        except Exception as e:
            return StorageResponse(False, message=str(e))

    def get_client_handler(self, room_id, client_id):
        try:
            client = self._internal_storage[room_id][client_id]
            return client
        except Exception as e:
            return StorageResponse(False, message=str(e))
