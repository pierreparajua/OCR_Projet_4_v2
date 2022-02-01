import operator

from model.m_player import Player
from model.m_storage import storage_p
from utils.util import Menu
from view.v_player import ViewPlayer
from view.view import View


class PlayerController:
    """Control all options available for the players"""
    def __init__(self):
        self.menu = self._create_menu("player_menu")
        self.storage = storage_p
        self.view = View()
        self.view_player = ViewPlayer()

    def manage_menu(self):
        """Manage the player's menu according with the user choice"""
        self.menu.choice = "0"
        self.menu = self._create_menu("player_menu")
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()

        if self.menu.choice == "1":  # Create player
            player = self.create_player()
            self.menu = self._create_menu("save_or_cancel")
            self.menu.display_menu()
            self.menu.choice = self.menu.get_choice()
            while self.menu.choice == "1":  # Save and create an other player
                player.id_db = storage_p.save(player)
                storage_p.update(player)
                player = self.create_player()
                self.menu.display_menu()
                self.menu.choice = self.menu.get_choice()
            if self.menu.choice == "2":  # Save and quit
                player.id_db = storage_p.save(player)
                storage_p.update(player)
                self.manage_menu()
            elif self.menu.choice == "3":  # Cancel
                self.manage_menu()

        elif self.menu.choice == "2":  # Display all players
            self.display_all_players(self.storage.load_all())
            self.manage_menu()

        elif self.menu.choice == "3":  # Update a player
            player = self.update_player(self.storage.load_all())
            self.menu = self._create_menu("update_or_cancel")
            self.menu.display_menu()
            self.menu.choice = self.menu.get_choice()
            while self.menu.choice == "1":  # Save and update an other player
                storage_p.update(player)
                player = self.update_player(self.storage.load_all())
                self.menu.display_menu()
                self.menu.choice = self.menu.get_choice()
            if self.menu.choice == "2":  # Save and quit
                storage_p.update(player)
                self.manage_menu()
            elif self.menu.choice == "3":  # Cancel
                self.manage_menu()

        elif self.menu.choice == "4":  # Delete a player
            player = self.view.select_item(self.display_all_players(self.storage.load_all()))
            self.view.display_text("confirm_delete")
            self.menu = self._create_menu("delete_or_cancel")
            self.menu.display_menu()
            self.menu.choice = self.menu.get_choice()
            while self.menu.choice == "1":  # Delete and delete an other player
                storage_p.delete(player)
                player = self.view.select_item(self.display_all_players(self.storage.load_all()))
                self.view.display_text("confirm_delete")
                self.menu.display_menu()
                self.menu.choice = self.menu.get_choice()
            if self.menu.choice == "2":  # Delete and quit
                storage_p.delete(player)
                self.manage_menu()
            elif self.menu.choice == "3":  # Cancel
                self.manage_menu()

        elif self.menu.choice == "m":  # Retour MainMenu
            pass

    def create_player(self) -> Player:
        """
        Create a new player.
        Returns:
             player: an instance of Player.
        """
        self.view.display_text("add_player")
        player = self.view_player.create_player()
        self.view.display_text("confirm-add-player")
        self.view.item = player
        self.view.display_item()
        return player

    def display_all_players(self, dict_players: dict) -> list:
        """
        Receive a dict from the database with all players.
        Deserialize and display it by ranking or alphabetic order.
        Return a list of Players
        Args:
            dict_players: Dict from the database containing all players.
        Returns:
            players: A list of Players
        """
        players = [Player.deserialize(dict_player) for dict_player in dict_players]
        self.menu = self._create_menu("players_order")
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()
        if self.menu.choice == "1":
            players.sort()
        elif self.menu.choice == "2":
            players = sorted(players, key=operator.attrgetter('last_name'))
        self.view.item = players
        self.view.display_items("joueurs")
        return players

    def update_player(self, dict_players: dict) -> Player:
        """
        Receive a dict from the database with all players.
        Select and update parameter, as user want.
        return the updated Player
        Args:
            dict_players: Dict from the database containing all players.
        Returns:
            new_player: an instance of Player.
        """
        self.view.display_text("player_to_update")
        old_player = self.view.select_item(self.display_all_players(dict_players))
        new_player = self.view_player.get_updating(old_player)
        self.view.item = new_player
        self.view.display_text("confirm_update")
        self.view.display_item()
        return new_player

    @staticmethod
    def _create_menu(menu: str):
        """
        Helper method to create a menu.
        Args:
            menu: Name of the menu, you want to create"
        Returns:
            An instance of Menu
        """
        player_menu = Menu(title="Menu de gestion des joueurs: ",
                           add_info="(Tapez le chiffre correspondant à votre choix ou 'm' pour retourner au menu "
                                    "précédent: )",
                           items=["Ajouter un joueur",
                                  "Afficher les joueurs",
                                  "Modifier un joueur",
                                  "Supprimer un joueur"],
                           choice="")

        save_or_cancel = Menu(title="Souhaitez-vous:",
                              add_info="",
                              items=["Sauver et créer un autre joueur ",
                                     "Sauver et retourner au menu",
                                     "Annuler"],
                              choice="")

        update_or_cancel = Menu(title="Souhaitez-vous:",
                                add_info="",
                                items=["Confirmer et modifier un autre joueur",
                                       "Confirmer",
                                       "Annuler"],
                                choice="")

        delete_or_cancel = Menu(title="Souhaitez-vous:",
                                add_info="",
                                items=["Confirmer et supprimer un autre joueur",
                                       "Confirmer",
                                       "Annuler"],
                                choice="")
        players_order = Menu(title="Souhaitez-vous affichez les joueurs par",
                             add_info="",
                             items=["Ordre de classement",
                                    "Ordre alphabétique"],

                             choice="")

        dict_menu = {"player_menu": player_menu,
                     "save_or_cancel": save_or_cancel,
                     "update_or_cancel": update_or_cancel,
                     "delete_or_cancel": delete_or_cancel,
                     "players_order": players_order}
        return dict_menu[menu]
