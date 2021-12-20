import utils
from view.view import View, DICT_TEXT, View_menu
from controller.c_player import Player_controller
from model.m_tournament import Tournament, Tournament_tiny_db
from model.m_player import Player_tiny_db

NB_PLAYER_MAX = 20
NB_player = list(map(str, list(range(1, (NB_PLAYER_MAX + 1)))))[1::2]

player_controller = Player_controller()
storage_t = Tournament_tiny_db()
storage_p = Player_tiny_db()


class Tournament_controller:
    """Controls the tournament"""

    def __init__(self, ):
        self.view: View = View(DICT_TEXT)

    def prepare_tournament(self):
        """Gets all informations needed to start a tournament"""
        self.view.display_text("ask_for_player")
        choice: str = utils.util.get_choice(["o", "n"])
        while choice == "o":
            player_controller.add_player()
            self.view.display_text("add_player_again")
            choice: str = utils.util.get_choice(["o", "n"])
        self.view.display_text("new_tournament", center=True)
        self.view.display_text("fill_items")
        tournament = got_tournament.create_tournament()
        players = self.select_player(tournament.nbr_of_rounds)
        self.view.display_instance(tournament)
        self.view.display_items(players, "joueurs sélectionnés")
        tournament.players = [storage_p.get_id(player) for player in players]
        return tournament

    def select_player(self, nb_round: int) -> list:
        """This function manage the player's selection for a new tournament."""
        players_selected = []
        players_id = []
        self.view.display_text("nb_player")
        nb_players = int(utils.util.get_choice(NB_player))  # Check if the number of players is even
        while nb_players / 2 < nb_round:
            self.view.display_text("error_nb_player")
            nb_players = int(utils.util.get_choice(NB_player))
        players = storage_p.load_all()
        self.view.display_items(players, "joueurs", select=True)
        i = 0
        while i < nb_players:
            player = self.view.select_item(players)
            if player in players_selected:
                self.view.display_text("already_selected")
            else:
                players_selected.append(player)
                i += 1
        players_selected.sort()
        return players_selected


time_control_menu = View_menu(title="  Choisissez le système de contrôle du temps:",
                              add_info="",
                              items=["Bullet", "Blitz", "Coup rapide"],
                              choice="")


class Get_info_tournament:
    """Gets player's informations from the user"""

    def __init__(self, name, place, date, rondes, players, time, description, nbr_of_rounds=4):
        self.name = name
        self.place = place
        self.date = date
        self.rondes = rondes
        self.players = players
        self.time = time
        self.description = description
        self.nbr_of_rounds = nbr_of_rounds

    def get_tournament_name(self):
        """Gets name of tournament."""
        self.name: str = input("  Nom: ").lower()
        while not utils.util.check_name_format(self.name):
            self.name = utils.util.wrong_entry(self.name)
        return self.name

    def get_tournament_place(self):
        """Gets place of tournament."""
        self.place: str = input("  Lieu: ").lower()
        while not utils.util.check_name_format(self.place):
            self.place = utils.util.wrong_entry(self.place)
        return self.place

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
        tournament = Tournament(self.get_tournament_name(),
                                self.get_tournament_place(),
                                self.get_tournament_date(),
                                [],
                                [],
                                self.get_time_control_mode(),
                                self.get_description(),
                                self.get_tournament_nb_round())
        return tournament


got_tournament = Get_info_tournament("", "", "", "", "", "", "")
