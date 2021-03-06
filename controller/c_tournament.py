from colorama import Fore

from model.m_player import Player
from utils.util import Menu, Validator
from controller.c_player import PlayerController
from model.m_storage import storage_t, storage_p
from model.m_tournament import Round, Tournament
from view.v_tournament import ViewTournament
from view.view import View

NB_PLAYER_MAX = 20
NB_player = list(map(str, list(range(1, (NB_PLAYER_MAX + 1)))))[1::2]


class TournamentController:
    """Control all options available for the tournaments"""
    def __init__(self):
        self.menu = self._create_menu("tournament_menu")
        self.storage_p = storage_p
        self.storage_t = storage_t
        self.view: View = View()
        self.v_tournament = ViewTournament()
        self.player_controller = PlayerController()
        self.validator = Validator()

    def control_menu(self):
        """Manage the tournament's menu according with the user choice"""
        while True:
            self.menu = self._create_menu("tournament_menu")
            self.menu.display_menu()
            self.menu.choice = self.menu.get_choice()

            if self.menu.choice == "1":  # New tournament
                self.add_new_tournament()

            elif self.menu.choice == "2":  # Resume tournament
                self.resume_tournament()

            elif self.menu.choice == "3":  # Delete a tournament
                self.delete_tournament()

            elif self.menu.choice == "4":  # Display the reports
                tournament = self.select_tournament(self.storage_t.load_all(), report=True)
                if tournament:
                    tournament.add_score_and_opponents()
                    self.report(tournament)

            elif self.menu.choice == "5":  # Return to main menu
                break

    def add_new_tournament(self):
        """Permit to create and save a new tournament"""
        tournament = self.prepare_tournament(self.storage_p.load_all())
        self.menu = self._create_menu("save_or_cancel")
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()
        if self.menu.choice == "1":  # Start tournament
            tournament.id_db = storage_t.save(tournament)
            storage_t.update(tournament)
            self.execute_rounds(tournament)
        elif self.menu.choice == "2":  # Save and quit
            tournament.id_db = storage_t.save(tournament)
            storage_t.update(tournament)
        elif self.menu.choice == "3":  # cancel
            pass

    def resume_tournament(self):
        """Permit to resume a tournament"""
        tournament = self.select_tournament(self.storage_t.load_all(), display_all=False)
        if tournament:
            self.menu = self._create_menu("continue_or_cancel")
            self.menu.display_menu()
            self.menu.choice = self.menu.get_choice()
            if self.menu.choice == "1":  # Continue tournament
                self.execute_rounds(tournament)
            elif self.menu.choice == "2":  # Cancel
                pass

    def delete_tournament(self):
        """Permit to delete a tournament"""
        tournament = self.select_tournament(self.storage_t.load_all())
        if tournament:
            self.menu = self._create_menu("delete_or_cancel")
            self.menu.display_menu()
            self.menu.choice = self.menu.get_choice()
            if self.menu.choice == "1":  # Delete
                self.storage_t.delete(tournament)
                self.view.display_text("confirm_deleted_tournament")
            elif self.menu.choice == "2":  # Cancel
                pass

    def prepare_tournament(self, dict_player) -> Tournament or []:
        """
        Get all informations needed to start a tournament.
        Args:
            dict_player: Dict from the database containing all players.
        Returns:
            tournament: An instance of Tournament
        """
        self.view.item = Fore.LIGHTMAGENTA_EX + "\n     -----Cr??ation d 'un nouveau tournois-----\n"
        self.view.display_item()
        self.view.display_text("ask_for_player")
        choice: str = self.validator.get_choice(["o", "n"])
        if choice == "o":
            self.player_controller.control_menu()
        self.view.display_text("new_tournament", center=True)
        self.view.display_text("fill_items")
        tournament = self.v_tournament.create_tournament()
        tournament.players = self.select_players(tournament.nbr_of_rounds, dict_player)
        self.view.display_text("resume_tournament", center=True)
        self.view.item = tournament
        self.view.display_item()
        self.view.item = tournament.players
        self.view.display_items("joueurs s??lectionn??s")
        tournament.players = [player.id_db for player in tournament.players]
        return tournament

    def select_players(self, nb_round: int, dict_player) -> list:
        """
        Select players for the tournament.
        Args:
            nb_round: Nombre of round in the tournament.
            dict_player: Dict from the database containing all players.
        Returns:
            players_selected: A list with all Players selected for the tournament
        """
        players_selected = []
        self.view.display_text("nb_player")
        nb_players = int(self.validator.get_choice(NB_player))  # Check if the number of players is even
        while nb_players / 2 < nb_round:
            self.view.display_text("error_nb_player")
            nb_players = int(self.validator.get_choice(NB_player))
        players = self.player_controller.display_all_players(dict_player)
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

    def round(self, tournament: Tournament) -> Tournament:
        """
        Manage the execution of a round
        Args:
            tournament: An instance of tournament
        Returns:
            tournament: An instance of tournament
        """
        tournament.add_score_and_opponents()
        round_nb = len(tournament.rondes)
        ronde = Round(round_nb, "", "", [])
        ronde.number = round_nb
        self.view.item = f"\n         ----------Ronde N?? {round_nb + 1}----------"
        self.view.display_item()
        if round_nb == 0:
            players_split1, players_split2 = tournament.split_players()
            ronde.matches = [[players_split1[i], players_split2[i]] for i in range(int(len(tournament.players) / 2))]
        else:
            ronde.matches = tournament.compute_matches()
        self.v_tournament.item = ronde.matches
        self.v_tournament.display_matches()
        ronde.date_start, ronde.date_end = self.start_end_ronde()
        ronde.matches = self.v_tournament.get_scores(ronde.matches)
        tournament.rondes.append(ronde)
        ronde.number = len(tournament.rondes)
        tournament.add_score_and_opponents()
        self.v_tournament.item = tournament
        self.v_tournament.display_score()
        tournament.players = [player.id_db for player in tournament.players]
        return tournament

    def execute_rounds(self, tournament):
        """
        Manage the sequence of rounds
        Args:
            tournament: An instance of tournament
        """
        while len(tournament.rondes) < tournament.nbr_of_rounds:
            tournament = self.round(tournament)
            if len(tournament.rondes) < tournament.nbr_of_rounds:
                self.menu = self._create_menu("save_or_cancel")
                self.menu.display_menu()
                self.menu.choice = self.menu.get_choice()
                if self.menu.choice == "3":  # cancel
                    break
                elif self.menu.choice == "2":  # Save and quit
                    storage_t.update(tournament)
                    break
                elif self.menu.choice == "1":  # Continue
                    storage_t.update(tournament)
            else:  # End of tournament
                date_end = Validator.get_date_now().split(" ")[0]
                if date_end != tournament.date:
                    tournament.date = tournament.date + " au " + date_end
                self.storage_t.update(tournament)
                self.view.display_text("winner")
                self.view.item = f"{Player.player_from_id(tournament.players[0]).full_name()}\n"
                self.view.display_item()
                self.view.display_text("end_tournament", center=True)

    def start_end_ronde(self) -> tuple:
        """
        Get and display the date and the hour for the start and the end of the round.
        Returns:
            date_start, date_end: date for the start and the end of the round.
        """
        self.view.display_text("start_ronde")
        self.validator.get_choice([""])
        self.view.display_text("good_luck")
        self.view.display_text("started_ronde")
        date_start = Validator.get_date_now()
        self.view.item = date_start
        self.view.display_item(center=True)
        self.view.display_text("end_ronde")
        self.validator.get_choice([""])
        date_end = Validator.get_date_now()
        self.view.item = date_end
        self.view.display_item(center=True)
        return date_start, date_end

    def select_tournament(self, dict_tournaments: dict, display_all=True, report=False) -> Tournament:
        """
        Receive a dict from the database with all tournaments.
        Deserialize and display it depending on parameters .
        Select and return a tournament.
        Args:
            dict_tournaments: Dict from the database containing all tournaments.
            display_all: If 'display_all' is false: the list contains only the unterminated tournament.
            report: If report is True: the list containing only  the terminated tournament.
        Returns:
            tournament: the selected tournament
        """
        tournaments = [Tournament.deserialize(tournament) for tournament in dict_tournaments]
        if report:
            tournaments = [tournament for tournament in tournaments if len(tournament.rondes) == 4]
        else:
            tournaments = [tournament for tournament in tournaments if len(tournament.rondes) != 4
                           or display_all]
        if tournaments:
            self.v_tournament.item = tournaments
            self.v_tournament.display_tournaments()
            tournament = self.view.select_item(tournaments)
            return tournament
        self.view.display_text("db_empty_tournament")

    def report(self, tournament: Tournament):
        """
        Manage the display of the report.
        Args:
            tournament: An instance of tournament.
        """
        if tournament:
            self.v_tournament.item = tournament
            self.v_tournament.display_ronde()
            self.v_tournament.display_score()

    @staticmethod
    def _create_menu(menu):
        """
        Helper method to create a menu.
        Returns:
            An instance of Menu
        """
        tournament_menu = Menu(title="Menu de gestion des tournois: ",
                               add_info="(Tapez le chiffre correspondant ?? votre choix: )",
                               items=["Ajouter un tournoi",
                                      "Reprendre un tournoi",
                                      "Supprimer un tournoi",
                                      "Afficher les rapports des tournois",
                                      "Retourner au menu principal"],
                               choice="")

        save_or_cancel = Menu(title="Souhaitez-vous: ",
                              add_info="",
                              items=["Continuer",
                                     "Sauver et retourner au menu",
                                     "Annuler"],
                              choice="")
        delete_or_cancel = Menu(title="Souhaitez-vous:",
                                add_info="",
                                items=["Supprimer le tournois",
                                       "Annuler"],
                                choice="")
        continue_or_cancel = Menu(title="Souhaitez-vous:",
                                  add_info="",
                                  items=["Continuer",
                                         "Annuler"],
                                  choice="")

        dict_menu = {"tournament_menu": tournament_menu,
                     "save_or_cancel": save_or_cancel,
                     "delete_or_cancel": delete_or_cancel,
                     "continue_or_cancel": continue_or_cancel}
        return dict_menu[menu]
