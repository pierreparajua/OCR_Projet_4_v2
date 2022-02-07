
from utils.util import Menu, Validator
from model.m_player import Player


class ViewPlayer:
    """Manage the specific views for the players"""
    update_player_menu = Menu(title="Quel attribut souhaitez vous modifier: ",
                              add_info="",
                              items=["Prénom", "Nom", "date de naissance", "sexe", "classement",
                                     "Fin des modifications"],
                              choice="")
    validator = Validator()

    def get_first_name(self) -> str:
        """Get the first_name from the user"""
        self.validator.item = input("Entrez le prénom: ")
        return self.validator.check_name("Vous devez saisir un prénom: ")

    def get_last_name(self) -> str:
        """Get the last_name from the user"""
        self.validator.item = input("Entrez le nom: ")
        return self.validator.check_name("Vous devez saisir un nom: ")

    def get_date_of_birth(self) -> str:
        """Get the date_of_birth from the user"""
        self.validator.item = input("Entrez le date de naissance: ")
        return self.validator.check_date("Vous devez saisir une date de naissance: ")

    def get_sex(self) -> str:
        """Get the sex from the user"""
        self.validator.item = input("Entrez le sexe du joueur('f' ou 'h'): ")
        return self.validator.check_sex("Vous devez saisir un sexe: ")

    def get_ranking(self) -> int:
        """Get the ranking from the user"""
        self.validator.item = input("Entrez le classement: ")
        return int(self.validator.check_number("Vous devez saisir un classement: "))

    def create_player(self) -> Player:
        """
        Create an instance of player from user's informations
        Returns:
            player: A Player
        """
        player = Player(first_name=self.get_first_name(),
                        last_name=self.get_last_name(),
                        date_of_birth=self.get_date_of_birth(),
                        sex=self.get_sex(),
                        ranking=self.get_ranking())
        return player

    def get_updating(self, updating_player: Player) -> Player:
        """
        Ask if the user wants update a player's item and return the updated player
        Args:
            updating_player: Player to update
        Returns:
            updating_player: Player updated
        """
        dict_player = updating_player.__dict__
        choices = {"1": [self.get_first_name, "_first_name"],
                   "2": [self.get_last_name, "_last_name"],
                   "3": [self.get_date_of_birth, "_date_of_birth"],
                   "4": [self.get_sex, "_sex"],
                   "5": [self.get_ranking, "_ranking"],
                   "6": "Fin des modifications"}
        while True:
            self.update_player_menu.display_menu()
            choice = self.update_player_menu.get_choice()
            if choices.get(choice) == "Fin des modifications":
                break
            dict_player[choices.get(choice)[1]] = choices.get(choice)[0]()
            print(updating_player)
        return updating_player
