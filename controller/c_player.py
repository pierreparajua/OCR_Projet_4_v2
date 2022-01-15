from model.m_player import Player
from model.m_storage import storage_p
from utils.util import Menu
from view.v_get_data_player import GetDataPlayer
from view.view import View


class PlayerController:
    def __init__(self):
        self.view = View("")
        self.got_player = GetDataPlayer("", "", "", "")

    def add_player(self) -> Player:
        """ Add player to database"""
        self.view.display_text("add_player")
        player = self.got_player.create_player()
        self.view.display_text("confirm-add-player")
        self.view.item = player
        self.view.display_item()
        return player

    def display_all_players(self, dict_players: dict, display=True) -> list:
        """Display a list of players saved in database"""
        self.view.item = [Player.deserialize(dict_player) for dict_player in dict_players]
        if display:
            self.view.display_items("joueurs")
        return self.view.item

    def update_player(self, dict_players: dict) -> Player:
        """Update a player in the database"""
        self.view.display_text("player_to_update")
        self.view.item = self.display_all_players(dict_players)
        old_player = self.view.select_item()
        new_player = self.got_player.get_updating(old_player)
        self.view.item = new_player
        self.view.display_text("confirm_update")
        self.view.display_item()

        return new_player

    def delete_player(self, dict_players: dict) -> Player:
        """Delete a player"""
        players = self.display_all_players(dict_players)
        self.view.item = players
        player = self.view.select_item()
        self.view.display_text("confirm_delete")
        return player


player_menu = Menu(title="Menu de gestion des joueurs: ",
                   add_info="(Tapez le chiffre correspondant à votre choix ou 'm' pour retourner au menu "
                            "précédent: )",
                   items=["Ajouter un joueur",
                          "Afficher les joueurs",
                          "Modifier un joueurs",
                          "Supprimer un joueur"],
                   choice="")

confirm_quit_menu = Menu(title="Souhaitez-vous:",
                         add_info="",
                         items=["Sauver et continuer",
                                "Sauver et retourner au menu",
                                "Annuler"],
                         choice="")


class PlayerManager:
    """Control the main features of the players"""

    def __init__(self):
        self.menu = player_menu
        self.storage = storage_p
        self.controller = PlayerController()
        self.choice = True

    def menu_manager(self):
        """Manage the player menu"""
        self.choice = True
        self.menu = player_menu
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()

        if self.menu.choice == "1":
            while self.choice:
                player = self.controller.add_player()
                self.choice = self.storage_manager(player)
            self.menu = player_menu
            self.menu_manager()
        elif self.menu.choice == "2":
            self.controller.display_all_players(self.storage.load_all())
            self.menu_manager()

        elif self.menu.choice == "3":
            while self.choice:
                player = self.controller.update_player(self.storage.load_all())
                self.choice = self.storage_manager(player, update=True)
            self.menu_manager()
        elif self.menu.choice == "4":
            while self.choice:
                player = self.controller.delete_player(self.storage.load_all())
                self.choice = self.storage_manager(player, delete=True)
            self.menu_manager()
        elif self.menu.choice == "m":
            pass

    def storage_manager(self, item, update=False, delete=False):
        self.menu = confirm_quit_menu
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()
        if self.menu.choice == "1":
            if delete:
                self.storage.delete(item)
                return True
            if not update:
                item.id_db = self.storage.save(item)
            self.storage.update(item)
            return True
        elif self.menu.choice == "2":
            if delete:
                self.storage.delete(item)
                return False
            if not update:
                item.id_db = self.storage.save(item)
            self.storage.update(item)
            self.menu = player_menu
            return False
        elif self.menu.choice == "3":
            self.menu = player_menu
            return False


if __name__ == "__main__":
    pierre = Player("pierre", "parajua", "20/06/1986", "homme", 0, 1106)
    test = PlayerManager()
    test.menu_manager()
