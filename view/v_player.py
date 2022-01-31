from colorama import Fore

from utils.util import Menu
from model.m_player import Player
from view.view import View


class ViewPlayer(Player, View):
    """Manage the views for the players"""
    update_player_menu = Menu(title="Quel attribut souhaitez vous modifier: ",
                              add_info="(Tapez 'm' pour sortir)",
                              items=["Prénom", "Nom", "date de naissance", "sexe", "classement"],
                              choice="")

    def __init__(self):
        super().__init__()

    def get_first_name(self) -> str:
        """Get the first_name from the user"""
        self.first_name = input("Entrez le prénom: ")
        while not self.first_name:
            self.first_name = input(Fore.LIGHTYELLOW_EX + "Vous devez saisir un prénom: ")
        return self.first_name

    def get_last_name(self) -> str:
        """Get the last_name from the user"""
        self.last_name = input("Entrez le Nom: ")
        while not self.last_name:
            self.last_name = input(Fore.LIGHTYELLOW_EX + "Vous devez saisir un nom: ")
        return self.last_name

    def get_date_of_birth(self) -> str:
        """Get the date_of_birth from the user"""
        self.date_of_birth = input("Entrez la date de naissance (JJ/MM/AAAA): ")
        while not self.date_of_birth:
            self.date_of_birth = input(Fore.LIGHTYELLOW_EX + "Vous devez saisir une date: ")
        return self.date_of_birth

    def get_sex(self) -> str:
        """Get the sex from the user"""
        self.sex = input("Entrez le sex( 'h' ou 'f'): ")
        while not self.sex:
            self.sex = input(Fore.LIGHTYELLOW_EX + "Vous devez saisir un sex: ")
        return self.sex

    def get_ranking(self) -> int:
        """Get the ranking from the user"""
        self.ranking = input("Entrez le classement: ")
        while not self.ranking:
            self.ranking = input(Fore.LIGHTYELLOW_EX + "Vous devez saisir un classement: ")
        return self.ranking

    def create_player(self) -> Player:
        """
        Create an instance of player from user's informations
        Returns:
            player: A Player
        """
        player = Player(self.get_first_name(),
                        self.get_last_name(),
                        self.get_date_of_birth(),
                        self.get_sex(),
                        1,
                        self.get_ranking())
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
                   "m": "break"}
        while True:
            self.update_player_menu.display_menu()
            choice = self.update_player_menu.get_choice()
            if choices.get(choice) == "break":
                break
            dict_player[choices.get(choice)[1]] = choices.get(choice)[0]()
            print(updating_player)
        return updating_player
