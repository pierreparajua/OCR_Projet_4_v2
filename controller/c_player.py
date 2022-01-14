from model.m_player import Player
from model.m_storage import TinyDatabase, db_players
from utils.util import Menu
from view.v_get_data_player import GetDataPlayer
from view.view import View

confirm_quit_menu = Menu(title="Souhaitez-vous:",
                         add_info="",
                         items=["Confirmer",
                                "Annuler"],
                         choice="")


class PlayerController:
    def __init__(self):
        self.view = View("")
        self.got_player = GetDataPlayer("", "", "", "")
        self.menu = confirm_quit_menu

    def add_player(self) -> Player:
        """ Add player to database"""
        self.view.display_text("add_player")
        player = self.got_player.create_player()
        self.view.display_text("confirm-add-player")
        self.view.item = player
        self.view.display_item()
        self.menu = confirm_quit_menu
        self.menu.display_menu()
        choice = self.menu.get_choice()
        if choice == "1":
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
        self.view.display_item()
        self.menu.display_menu()
        choice = self.menu.get_choice()
        if choice == "1":
            return new_player

    def delete_player(self, dict_players: dict) -> Player:
        """Delete a player"""

        players = self.display_all_players(dict_players)
        self.view.item = players
        player = self.view.select_item()
        self.view.display_text("confirm_delete")
        self.menu.display_menu()
        choice = self.menu.get_choice()
        if choice == "1":
            self.view.display_text("confirm_deleted")
            return player


player_menu = Menu(title="Menu de gestion des joueurs: ",
                   add_info="(Tapez le chiffre correspondant à votre choix ou 'm' pour retourner au menu "
                            "précédent: )",
                   items=["Ajouter un joueur",
                          "Afficher les joueurs",
                          "Modifier un joueurs",
                          "Supprimer un joueur"],
                   choice="")


class PlayerManager:
    """Control the main features of the players"""
    def __init__(self):
        self.menu = player_menu
        self.storage = TinyDatabase(db_players)
        self.controller = PlayerController()

    def player_manager(self):
        """Manage the player menu"""
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()

        if self.menu.choice == "1":
            player = self.controller.add_player()
            if player:
                self.storage.save(player)
            self.player_manager()

        elif self.menu.choice == "2":
            self.controller.display_all_players(self.storage.load_all())
            self.player_manager()

        elif self.menu.choice == "3":
            player = self.controller.update_player(self.storage.load_all())
            if player:
                self.storage.update(player)
            self.player_manager()

        elif self.menu.choice == "4":
            player = self.controller.delete_player(self.storage.load_all())
            if player:
                self.storage.delete(player)
            self.player_manager()
        elif self.menu.choice == "m":
            pass
