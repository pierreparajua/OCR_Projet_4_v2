from model.m_player import Player
from model.m_storage import storage_p
from utils.util import Menu
from view.v_get_data_player import GetDataPlayer
from view.view import View


class PlayerController:
    """Control the features for a player"""
    def __init__(self):
        self.view = View("")
        self.got_player = GetDataPlayer("", "", "", "")

    def create_player(self) -> Player:
        """
        Create a new player.
        Returns:
             player: an instance of Player.
        """
        self.view.display_text("add_player")
        player = self.got_player.create_player()
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
        self.view.item = self.display_all_players(dict_players)
        old_player = self.view.select_item()
        new_player = self.got_player.get_updating(old_player)
        self.view.item = new_player
        self.view.display_text("confirm_update")
        self.view.display_item()
        return new_player

    def delete_player(self, dict_players: dict) -> Player:
        """
        Select a player from a dict, and return it to be deleted.
        Args:
            dict_players: Dict from the database containing all players.
        Returns:
            player: the selected player
        """
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


class PlayerManager(PlayerController):
    """Manage the interface with the users and the relation with the database"""
    def __init__(self):
        super().__init__()
        self.menu = player_menu
        self.storage = storage_p
        self.choice = True

    def menu_manager(self):
        """Manage the player's menu according with the user choice"""
        self.choice = True
        self.menu = player_menu
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()

        if self.menu.choice == "1":
            while self.choice:
                player = self.create_player()
                self.choice = self.storage_manager(player)
            self.menu = player_menu
            self.menu_manager()
        elif self.menu.choice == "2":
            self.display_all_players(self.storage.load_all())
            self.menu_manager()

        elif self.menu.choice == "3":
            while self.choice:
                player = self.update_player(self.storage.load_all())
                self.choice = self.storage_manager(player, update=True)
            self.menu_manager()
        elif self.menu.choice == "4":
            while self.choice:
                player = self.delete_player(self.storage.load_all())
                self.choice = self.storage_manager(player, delete=True)
            self.menu_manager()
        elif self.menu.choice == "m":
            pass

    def storage_manager(self, item, update=False, delete=False) -> bool:
        """
        Manage the relation with the database,
        if parameters are false, save the item.
        Args:
            item: Item on which the method is executed.
            update: If True update the item.
            delete: If True delete item.
        Returns:
            A boolean, to know for menu_manager if it must repeat the action or not.
        """
        if delete:
            self.menu = delete_or_cancel
            self.menu.display_menu()
            self.menu.choice = self.menu.get_choice()
            if self.menu.choice == "1":
                self.storage.delete(item)
                return False
            elif self.menu.choice == "2":
                self.menu = player_menu
                return False
        self.menu = save_or_cancel
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
            self.menu = player_menu
            return False
        elif self.menu.choice == "3":
            self.menu = player_menu
            return False


if __name__ == "__main__":
    pierre = Player("pierre", "parajua", "20/06/1986", "homme", 0, 1106)
    test = PlayerManager()
    test.menu_manager()
