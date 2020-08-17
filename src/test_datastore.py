import unittest
import json
import os
import logging

from datastore import GameStorage, ClientStorage
from serializer import CDNMSEncoder
import words


class TestGameStorage(unittest.TestCase):
    """
    Testing the Storage Response
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        words.WORDBANK = words.load_words()

    def test_create_room(self):
        self.game_storage = GameStorage()
        # Test No room
        response = self.game_storage.create_room(None)
        assert response is not None
        assert response.success == False

        response = self.game_storage.create_room("")
        assert response is not None
        assert response.success == False

        response = self.game_storage.create_room("test_name")
        assert response is not None
        assert response.success == True

    def test_remove_room(self):
        self.game_storage = GameStorage()
        response = self.game_storage.create_room("test_name")
        game_rooms = self.game_storage._internal_storage.keys()
        assert len(game_rooms) == 1
        assert response is not None
        assert response.success == True
        room_id = response.data["room_id"]
        assert room_id is not None
        response = self.game_storage.remove_room(room_id)
        assert response is not None
        assert response.success == True
        game_rooms = self.game_storage._internal_storage.keys()
        assert len(game_rooms) == 0

    def test_get_room(self):
        self.game_storage = GameStorage()
        test_name = "test_name"
        response = self.game_storage.create_room(test_name)
        assert response is not None
        assert response.success == True
        room_id = response.data["room_id"]
        response = self.game_storage.get_room(room_id)
        assert response is not None
        assert response.success == True
        game_room_data = response.data
        assert game_room_data.name == test_name

    def test_update_room(self):
        self.game_storage = GameStorage()
        test_name = "test_name"
        response = self.game_storage.create_room(test_name)
        assert response is not None
        assert response.success == True
        room_id = response.data["room_id"]
