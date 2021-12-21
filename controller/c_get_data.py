from colorama import Fore

import utils
from utils.util import Menu
from model.main_model import Player, Tournament

time_control_menu = Menu(title="  Choisissez le système de contrôle du temps:",
                         add_info="",
                         items=["Bullet", "Blitz", "Coup rapide"],
                         choice="")


class GetData:
    def __init__(self, string: str):
        self.string = string

    def get_string(self, item: str, key: str, old_item=None, update: bool = False):
        """Gets first name or update it if 'update' is True."""

        if update:
            attributes = {}
            try:
                attributes = {"first_name": old_item.first_name, "last_name": old_item.last_name,
                              "name": old_item.name, "place": old_item.place}
            except AttributeError:
                print(attributes)
                name = input(Fore.LIGHTBLUE_EX + f"  {item}: "
                             + Fore.LIGHTWHITE_EX + f"({attributes[key]}): ").lower()
                self.string = utils.util.check_name(name) or attributes[key]
                return self.string

        self.string = input(f"  {item}: ").lower()
        while not utils.util.check_name_format(self.string):
            self.string = utils.util.wrong_entry(self.string)
        return self.string


class GetDataPlayer(GetData):
    """Gets player's informations from the user"""

    def __init__(self, first_name: str, last_name: str, date_of_birth: str, sex: str, string: str):
        super().__init__(string)
        self.first_name = first_name,
        self.last_name = last_name,
        self.date_of_birth = date_of_birth,
        self.sex = sex,
        self.ranking = 1000

    def get_player_date_of_birth(self, old_player, update: bool = False):
        """Gets date of birth or update it if 'update' is True."""
        if update:
            date = input(Fore.LIGHTBLUE_EX + f"{'  Date de naissance: '}"
                         + Fore.LIGHTWHITE_EX + f"({old_player.date_of_birth}): ").lower()
            value = utils.util.check_date(date) or old_player.date_of_birth
            return value
        self.date_of_birth = utils.util.replace_for_date(input("  Date de naissance(DD/MM/YYYY): "))
        while not utils.util.check_date_format(self.date_of_birth):
            self.date_of_birth = utils.util.replace_for_date(utils.util.wrong_entry(self.date_of_birth).lower())
        return self.date_of_birth

    def get_player_sex(self, old_player, update: bool = False):
        """Gets sex or update it if 'update' is True."""
        if update:
            sex = input(Fore.LIGHTBLUE_EX + "  Sexe "
                        + Fore.LIGHTWHITE_EX + f"({old_player.sex}) (tapez : 'f'  ou 'h'): ").lower()
            if sex == "f":
                sex = "femme"
            elif sex == "h":
                sex = "homme"
            value = utils.util.check_name(sex) or old_player.sex
            return value
        self.sex = input("  Sexe (tapez : 'f' pour femme ou 'h' pour homme): ").lower()
        while self.sex not in ["h", "f"]:
            self.sex = utils.util.wrong_entry(self.sex).lower()
        if self.sex == "f":
            self.sex = "femme"
        elif self.sex == "h":
            self.sex = "homme"
        return self.sex

    def get_player_ranking(self, old_player, update: bool = False):
        """Gets ranking or update it if 'update' is True."""
        if update:
            ranking = input(Fore.LIGHTBLUE_EX + "  Classement " + Fore.LIGHTWHITE_EX + f"({old_player.ranking}): ")
            value = utils.util.check_ranking(ranking) or old_player.ranking
            return int(value)
        self.ranking = input("  Classement: ")
        while not utils.util.check_ranking_format(self.ranking):
            self.ranking = utils.util.wrong_entry(self.ranking)
        return int(self.ranking)

    def create_player(self):
        """Create an instance of Player from previous items filling by the user."""
        player = Player(self.get_string("prénom", "first_name"),
                        self.get_string("nom", "last_name"),
                        self.get_player_date_of_birth(old_player=""),
                        self.get_player_sex(old_player=""),
                        0,
                        self.get_player_ranking(old_player=""))
        return player

    def update_player(self, old_player):
        """Create an instance of Player from previous items updating by the user."""
        player = Player(self.get_string("prénom", "first_name", old_player, update=True),
                        self.get_string("nom", "last_name", old_player, update=True),
                        self.get_player_date_of_birth(old_player, update=True),
                        self.get_player_sex(old_player, update=True),
                        0,
                        self.get_player_ranking(old_player, update=True))
        return player


class GetDataTournament(GetData):
    """Gets player's informations from the user"""

    def __init__(self, name, place, date, rondes, players, time, description, string: str, nbr_of_rounds=4):
        super().__init__(string)
        self.name = name
        self.place = place
        self.date = date
        self.rondes = rondes
        self.players = players
        self.time = time
        self.description = description
        self.nbr_of_rounds = nbr_of_rounds

    def get_tournament_date(self):
        """Gets tournament start date,  and end date if needed."""

        date = utils.util.get_date_now().split(" ")[0]
        date1: str = utils.util.replace_for_date(input(f"  Date de début du tournoi {date} (Tapez '"
                                                       f"Entrez' pour continuer ou modifier la date (DD/MM/YYYY))"
                                                       f": "))
        value = date1 or date
        while not utils.util.check_date_format(value):
            value = utils.util.wrong_entry(value)
            value = value or date

        date2: str = utils.util.replace_for_date(input("  Date de fin du tournoi (tapez 'Entrez' si le tournois ce "
                                                       "déroule sur une journée): "))
        if not date2:
            self.date = value
            return self.date
        while not utils.util.check_date_format(date2):
            date2 = utils.util.wrong_entry(date2)
            if not date2:
                self.date = value
                return self.date
        else:
            self.date = value + " - " + date2
            return self.date

    def get_tournament_nb_round(self):
        """Gets the number of round for the tournament, 4 is the default value."""
        value = input("Nombre de tours(si 4, appuyer sur entrez): ")
        while not utils.util.check_ranking_format(value):
            value = utils.util.wrong_entry(value)
        return int(value or self.nbr_of_rounds)

    def get_time_control_mode(self):
        """Users have to choice the time of control method for the tournament."""
        time_control_menu.display_menu()
        time = time_control_menu.get_choices()
        if time == "1":
            self.time = "bullet"
        elif time == "2":
            self.time = "blitz"
        elif time == "3":
            self.time = "coup rapide"
        return self.time

    def get_description(self):
        """Gets informations from tournament's director if needed."""
        self.description = input("Description: ")
        return self.description

    def create_tournament(self):
        """Create an instance of Tournament from previous items filling by the user."""
        tournament = Tournament(self.get_string("Nom", "name"),
                                self.get_string("Lieu", "place"),
                                self.get_tournament_date(),
                                [],
                                [],
                                self.get_time_control_mode(),
                                self.get_description(),
                                0,
                                self.get_tournament_nb_round())
        return tournament
