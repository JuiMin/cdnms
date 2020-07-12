# Contains the datastore interface


class Datastore:
    """
    Store and obtain data from datastore
    """

    # User Functions
    def add_user(self, session_id, username):
        raise NotImplementedError

    def delete_user(self, session_id):
        raise NotImplementedError

    # Room Related
    def create_room(self, creator_id, room_name):
        raise NotImplementedError

    def delete_room(self, room_id):
        raise NotImplementedError

    # Gameplay
    def select_card(self, room_id, card_num):
        """
        Selects a card