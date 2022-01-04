from model.m_player import Player
from view.v_get_data import GetDataPlayer
from view.view import View, DICT_TEXT
from model.m_storage import PlayerTinydb
import utils

storage = PlayerTinydb()
got_player = GetDataPlayer("", "", "", "")


class PlayerController:
    """Controls the players."""

    def __init__(self):
        self.view: View = View(DICT_TEXT)

    def add_player(self):
        """ Add player to database"""
        self.view.display_text("add_player")
        player = got_player.create_player()
        self.view.display_instance(player)
        self.view.display_text("confirm-add-player")
        choice = utils.util.get_choice(["o", "n"])
        if choice == "o":
            storage.item = player
            storage.save()
            storage.update()
            self.view.display_text("added_player")
        else:
            self.view.display_text("no_action")

    def display_all_players(self,  display=True):
        """Display the list of players save in database."""
        dict_players = storage.load_all()
        players = [Player.deserialize(dict_player) for dict_player in dict_players]
        if display:
            self.view.display_items(players, "joueurs")
        return players

    def update_player(self):
        """Update a player in the database."""
        players = self.display_all_players(display=False)
        self.view.display_items(players, "joueurs", select=True)
        old_player = self.view.select_item(players)
        new_player = got_player.get_updating(old_player)
        self.view.display_text("confirm_update")
        self.view.display_instance(new_player)
        choice: str = utils.util.get_choice(["o", "n"])
        if choice == "o":
            storage.item = new_player
            storage.update()
            self.view.display_text("confirm_updated")
        else:
            self.view.display_text("cancel-action")

    def delete_player(self):
        """Delete a player."""
        players = self.display_all_players(display=False)
        self.view.display_items(players, "joueurs", select=True)
        player = self.view.select_item(players)
        self.view.display_text("confirm_delete")
        choice = utils.util.get_choice(["o", "n"])
        if choice == "o":
            storage.item = player
            storage.delete()
            self.view.display_text("confirm_deleted")
        else:
            self.view.display_text("cancel-action")


if __name__ == "__main__":
    """
    pierre = Player("caroline", "sejil", "08/02/1984", "femme", 1, 1230)
    storage = PlayerTinydb()
    storage.item = pierre
    storage.save()
    storage.update()
    test = PlayerController()
    test.update_player()
    """
