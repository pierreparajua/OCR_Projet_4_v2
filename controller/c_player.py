from view.view import View_player
from model.m_player import Player, storage
import utils


class Player_controller:
    def __init__(self, view_player):
        self.view: View_player = view_player

    def add_player(self):
        self.view.display_text("add_player")
        player = Player(self.view.get_first_name(),
                        self.view.get_last_name(),
                        self.view.get_player_date_of_birth(),
                        self.view.get_player_sex(),
                        self.view.get_player_ranking())
        utils.util.display_instance(player)
        self.view.display_text("confirm-add-player")
        choice = utils.util.get_choice(["o", "n"])
        if choice == "o":
            storage.save(player)
            self.view.display_text("added_player")
        else:
            self.view.display_text("no_action")

    def display_all_players(self):
        self.view.display_text("all_players")
        self.view.display_players(storage.load_players())

    def update_player(self):
        self.view.display_text("player_to_update")
        players = storage.load_players()
        self.view.display_players(players)
        choice = utils.util.get_choice(list(map(str, list(range(1, len(players) + 1)))))
        self.view.display_text("selected_player")
        old_player = players[int(choice) - 1]
        utils.util.display_instance(old_player)
        new_player = Player("", "", "", "")
        self.view.display_text("updating_player")
        new_player = Player(self.view.update_player_first_name(old_player, new_player),
                            self.view.update_player_last_name(old_player, new_player),
                            self.view.update_player_date_of_birth(old_player, new_player),
                            self.view.update_player_sex(old_player, new_player),
                            self.view.update_player_ranking(old_player, new_player))
        utils.util.display_instance(new_player)
        self.view.display_text("confirm_update")
        choice: str = utils.util.get_choice(["o", "n"])
        if choice == "o":
            storage.update_player(old_player, new_player)
            self.view.display_text("confirm_updated")
        else:
            self.view.display_text("cancel-action")

    def delete_player(self):
        pass


player_controller = Player_controller(View_player(""))

if __name__ == "__main__":
    player_controller = Player_controller(View_player(""))
    player_controller.add_player("add_player")
