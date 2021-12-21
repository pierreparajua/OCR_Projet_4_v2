from controller.c_get_data import GetDataPlayer
from view.view import View, DICT_TEXT
from model.m_storage import PlayerTinydb
import utils

storage = PlayerTinydb()
got_player = GetDataPlayer("", "", "", "", "")


class PlayerController:
    """Controls the players."""

    def __init__(self, ):
        self.view: View = View(DICT_TEXT)

    def add_player(self):
        """ Add player to database"""
        self.view.display_text("add_player")
        player = got_player.create_player()
        self.view.display_instance(player)
        self.view.display_text("confirm-add-player")
        choice = utils.util.get_choice(["o", "n"])
        if choice == "o":
            storage.save(player)
            self.view.display_text("added_player")
        else:
            self.view.display_text("no_action")

    def display_all_players(self):
        """Display the list of players save in database."""
        self.view.display_items(storage.load_all(), "joueurs")

    def update_player(self):
        """Update a player in the database."""
        players = storage.load_all()
        self.view.display_items(players, "joueurs", select=True)
        old_player = self.view.select_item(players)
        self.view.display_text("updating_player")
        new_player = got_player.update_player(old_player)
        self.view.display_instance(new_player)
        self.view.display_text("confirm_update")
        choice: str = utils.util.get_choice(["o", "n"])
        if choice == "o":
            storage.update(old_player, new_player)
            self.view.display_text("confirm_updated")
        else:
            self.view.display_text("cancel-action")

    def delete_player(self):
        """Delete a player."""
        players = storage.load_all()
        self.view.display_items(players, "joueurs", select=True)
        player = self.view.select_item(players)
        self.view.display_text("confirm_delete")
        choice = utils.util.get_choice(["o", "n"])
        if choice == "o":
            storage.delete(player)
            self.view.display_text("confirm_deleted")
        else:
            self.view.display_text("cancel-action")


if __name__ == "__main__":
    pass
