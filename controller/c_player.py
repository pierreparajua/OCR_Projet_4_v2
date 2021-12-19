from view.view import View, Get_info_player, DICT_TEXT
from model.m_player import Player, PlayerDB
import utils

storage = PlayerDB()
got_player = Get_info_player()


class Player_controller:
    def __init__(self, ):
        self.view = View(DICT_TEXT)

    def add_player(self):
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
        self.view.display_players(storage.load_players(), "joueurs")

    def update_player(self):
        players = storage.load_players()
        self.view.display_players(players, "joueurs", select=True)
        old_player = self.view.select_item(players)
        self.view.display_instance(old_player)
        self.view.display_text("updating_player")
        new_player = got_player.update_player(old_player)
        self.view.display_text("confirm_update")
        choice: str = utils.util.get_choice(["o", "n"])
        if choice == "o":
            storage.update_player(old_player, new_player)
            self.view.display_text("confirm_updated")
        else:
            self.view.display_text("cancel-action")

    def delete_player(self):
        players = storage.load_players()
        self.view.display_players(players, "joueurs", select=True)
        player = self.view.select_item(players)
        self.view.display_text("confirm_delete")
        choice = utils.util.get_choice(["o", "n"])
        if choice == "o":
            storage.delete_player(player)
            self.view.display_text("confirm_deleted")
        else:
            self.view.display_text("cancel-action")



if __name__ == "__main__":
    pass
