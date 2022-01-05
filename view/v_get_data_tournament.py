from colorama import Fore

import utils
from model.m_tournament import Tournament
from utils.util import Menu

time_control_menu = Menu(title="Choisissez le système de contrôle du temps",
                         add_info="",
                         items=["Bullet", "Blitz", "Coup rapide"],
                         choice="")


class GetDataTournament(Tournament):
    """Gets tournament's informations from the user"""

    def get_name(self):
        """Gets the name from the user"""
        self.name = input("Entrez le nom du tournoi: ")
        while not self.name:
            self.name = input(Fore.LIGHTYELLOW_EX + "Vous devez saisir un nom de tournois: ")
        return self.name

    def get_place(self):
        """Gets the place from the user"""
        self.place = input("Entrez le lieu du tournoi: ")
        while not self.place:
            self.place = input(Fore.LIGHTYELLOW_EX + "Vous devez saisir un lieu de tournois: ")
        return self.place

    def get_date(self):
        """Gets the date from the user"""
        self.date = input(f"Date du tournois: {utils.util.get_date_now()[0:10]}\n"
                          f"Tapez la date si différente ou 'Entrez'(JJ/MM:AAAA): ")
        if not self.date:
            self.date = str(utils.util.get_date_now()[0:10])
        return self.date

    def get_nbr_of_rounds(self):
        """Gets the number of rounds from the user"""
        self.nbr_of_rounds = input("Tapez sur 'Entrez' pour 4 rondes\nou entrez le nombre de ronde souhaiter: ")
        return self.nbr_of_rounds

    def get_time(self):
        """Gets the time control method from the user"""
        time_control_menu.display_menu()
        choice = time_control_menu.get_choices()
        if choice == "1":
            self.time = "Bullet"
        elif choice == "2":
            self.time = "Blitz"
        elif choice == "3":
            self.time = "Coup rapide"
        return self.time

    def get_description(self):
        """Gets description from the user"""
        self.description = input("Remarques du président de tournois: ")
        return self.description

    def create_tournament(self):
        """Creates an instance of tournament from user's informations"""
        tournament = Tournament(self.get_name(),
                                self.get_place(),
                                self.get_date(),
                                [],
                                [],
                                self.get_time(),
                                self.get_description(),
                                1,
                                self.get_nbr_of_rounds())
        return tournament


if __name__ == "__main__":
    test = GetDataTournament("", "", "", [], [], "", "")
    print(test.create_tournament())
