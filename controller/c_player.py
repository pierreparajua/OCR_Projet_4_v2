from model.m_player import Player
from model.m_storage import storage_p
from utils.util import Menu
from view.v_player import ViewPlayer
from view.view import View


class PlayerController:
    def __init__(self):
        self.menu = self._create_menu("player_menu")
        self.storage = storage_p
        self.view = View()
        self.view_player = ViewPlayer()
        self.choice = True

    def manage_menu(self):
        """Manage the player's menu according with the user choice"""
        self.choice = True
        self.menu = self._create_menu("player_menu")
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()

        if self.menu.choice == "1":
            while self.choice:
                player = self.create_player()
                self.choice = self.manage_storage(player)
            self.menu = self._create_menu("player_menu")
            self.manage_menu()
        elif self.menu.choice == "2":
            self.display_all_players(self.storage.load_all())
            self.manage_menu()

        elif self.menu.choice == "3":
            while self.choice:
                player = self.update_player(self.storage.load_all())
                self.choice = self.manage_storage(player, update=True)
            self.manage_menu()
        elif self.menu.choice == "4":
            while self.choice:
                player = self.select_to_delete(self.storage.load_all())
                self.choice = self.manage_storage(player, delete=True)
            self.manage_menu()
        elif self.menu.choice == "m":
            pass

    def manage_storage(self, item, update=False, delete=False) -> bool:
        """
        Manage the relation with the database,
        if parameters are false, save the item.
        Args:
            item: Item on which the method is executed.
            update: If True update the item.
            delete: If True delete item.
        Returns:
            A boolean, to methode "manage_menu" to know if it must repeat the action or not.
        """
        if delete:
            self.menu = self._create_menu("delete_or_save")
            self.menu.display_menu()
            self.menu.choice = self.menu.get_choice()
            if self.menu.choice == "1":
                self.storage.delete(item)
                return False
            elif self.menu.choice == "2":
                self.menu = self._create_menu("player_menu")
                return False
        self.menu = self._create_menu("save_or_cancel")
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()
        if self.menu.choice == "1":
            if not update:
                item.id_db = self.storage.save(item)
            self.storage.update(item)
            return True
        elif self.menu.choice == "2":
            if not update:
                item.id_db = self.storage.save(item)
            self.storage.update(item)
            self.menu = self._create_menu("player_menu")
            return False
        elif self.menu.choice == "3":
            self.menu = self._create_menu("player_menu")
            return False

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
        Display and return  a list of dict_players.
        Args:
            dict_players: Dict from the database containing all players.
        Returns:
            players: A list of Players
        """
        players = [Player.deserialize(dict_player) for dict_player in dict_players]
        self.view.item = players
        self.view.display_items("joueurs")
        return players

    def update_player(self, dict_players: dict) -> Player:
        """
        Select a player from a dict, update and return it.
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

    def select_to_delete(self, dict_players: dict) -> Player:
        """
        Select a player from a dict, and return it to be deleted.
        Args:
            dict_players: Dict from the database containing all players.
        Returns:
            player: the selected player
        """
        player = self.view.select_item(self.display_all_players(dict_players))
        self.view.display_text("confirm_delete")
        return player

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
                              items=["Sauver et continuer",
                                     "Sauver et retourner au menu",
                                     "Annuler"],
                              choice="")

        delete_or_cancel = Menu(title="Souhaitez-vous:",
                                add_info="",
                                items=["Confirmer",
                                       "Annuler"],
                                choice="")
        dict_menu = {"player_menu": player_menu,
                     "save_or_cancel": save_or_cancel,
                     "delete_or_save": delete_or_cancel}
        return dict_menu[menu]


if __name__ == "__main__":
    pass
