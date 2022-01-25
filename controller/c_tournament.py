from colorama import Fore

import utils
from utils.util import Menu
from controller.c_player import PlayerController
from model.m_storage import storage_t, storage_p
from model.m_tournament import Ronde, ChessPlayer, Tournament
from view.v_tournament import ViewTournament
from view.view import View

NB_PLAYER_MAX = 20
NB_player = list(map(str, list(range(1, (NB_PLAYER_MAX + 1)))))[1::2]


class TournamentManager:
    def __init__(self):
        self.menu = self._create_menu("tournament_menu")
        self.storage_p = storage_p
        self.storage_t = storage_t
        self.view: View = View()
        self.v_tournament = ViewTournament()
        self.player_controller = PlayerController()
        self.chess_player = ChessPlayer()
        self.choice = True

    def manage_menu(self):
        """Manage the tournament's menu according with the user choice"""
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()
        if self.menu.choice == "1":
            tournament = self.prepare_tournament(self.storage_p.load_all())
            while not tournament:
                tournament = self.prepare_tournament(self.storage_p.load_all())
            if self.manage_storage(tournament):
                tournament = self.round1(tournament)
                self.execute_rounds(tournament)
            self.menu = self._create_menu("tournament_menu")
            self.manage_menu()

        elif self.menu.choice == "2":
            self.choice = True
            tournament = self.select_tournament(self.storage_t.load_all(), display_all=False)
            if tournament:
                if not tournament.rondes:
                    tournament = self.round1(tournament)
                self.execute_rounds(tournament)
            self.menu = self._create_menu("tournament_menu")
            self.manage_menu()

        elif self.menu.choice == "3":
            tournament = self.delete_tournament(storage_t.load_all())
            if tournament:
                self.manage_storage(tournament, delete=True)
            self.menu = self._create_menu("tournament_menu")
            self.manage_menu()

        elif self.menu.choice == "4":
            tournament = self.select_tournament(self.storage_t.load_all(), report=True)
            self.report(tournament)
            self.manage_menu()

        elif self.menu.choice == "m":
            pass

    def manage_storage(self, item, direct_update=False, update=False, delete=False):
        """
        Manage the relation with the database,
        if parameters are false, save the item.
        Args:
            item: item on which the method is executed.
            direct_update: if True to a quick update without ask question to the user.
            update: If True update the item.
            delete: If True delete item.
        Returns:
        A boolean, to method "manage_menu" to know if it must repeat the action or not.
        """
        if delete:
            self.menu = self._create_menu("delete_or_cancel")
            self.menu.display_menu()
            self.menu.choice = self.menu.get_choice()
            if self.menu.choice == "1":
                self.storage_t.delete(item)
                return False
            elif self.menu.choice == "2":
                self.menu = self._create_menu("tournament_menu")
                return False
        if direct_update:
            self.storage_t.update(item)
            return False
        self.menu = self._create_menu("save_or_cancel")
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()
        if self.menu.choice == "1":
            if not update:
                item.id_db = self.storage_t.save(item)
            self.storage_t.update(item)
            return True
        elif self.menu.choice == "2":
            if not update:
                item.id_db = self.storage_t.save(item)
            self.storage_t.update(item)
            return False
        elif self.menu.choice == "3":
            return False

    def prepare_tournament(self, dict_player) -> Tournament or []:
        """
        Get all informations needed to start a tournament.
        Args:
            dict_player: Dict from the database containing all players.
        Returns:
            tournament: An instance of Tournament
        """
        self.view.item = Fore.LIGHTMAGENTA_EX + "\n     -----Création d 'un nouveau tournois-----\n"
        self.view.display_item()
        self.view.display_text("ask_for_player")
        choice: str = utils.util.get_choice(["o", "n"])
        if choice == "o":
            self.player_controller.manage_menu()
            return []
        self.view.display_text("new_tournament", center=True)
        self.view.display_text("fill_items")
        tournament = self.v_tournament.create_tournament()
        players = self.select_players(tournament.nbr_of_rounds, dict_player)
        self.view.display_text("resume_tournament", center=True)
        self.view.item = tournament
        self.view.display_item()
        self.view.item = players
        self.view.display_items("joueurs sélectionnés")
        tournament.chess_players = [self.chess_player.create_chess_player(player) for player in players]
        return tournament

    def select_players(self, nb_round: int, dict_player) -> list:
        """
        Select players for the tournament.
        Args:
            nb_round: Nombre of round in the tournament.
            dict_player: Dict from the database containing all players.
        Returns:
            players_selected: A list with all players selected for the tournament
        """
        players_selected = []
        self.view.display_text("nb_player")
        nb_players = int(utils.util.get_choice(NB_player))  # Check if the number of players is even
        while nb_players / 2 < nb_round:
            self.view.display_text("error_nb_player")
            nb_players = int(utils.util.get_choice(NB_player))
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

    def round1(self, tournament: Tournament) -> Tournament:
        """
        Split players to create matches, launch the round, get and display the scores.
        Args:
            tournament: An instance of tournament.
        Returns:
            tournament: An instance of tournament.
        """
        ronde1 = Ronde("1", "", "", [])
        self.view.display_text("ronde1", center=True)
        players_split1, players_split2 = utils.util.split_players(tournament.chess_players)
        ronde1.matches = [[players_split1[i].id_player, players_split2[i].id_player]
                          for i in range(int(len(tournament.chess_players) / 2))]
        self.v_tournament.item = tournament
        self.v_tournament.display_matches(ronde1.matches)
        ronde1.date_start, ronde1.date_end = self.start_end_ronde()
        tournament.chess_players, ronde1.matches = self.v_tournament.get_scores(tournament.chess_players,
                                                                                ronde1.matches)
        tournament.rondes.append(ronde1)
        tournament.chess_players.sort()
        self.v_tournament.item = tournament
        self.v_tournament.display_score()
        return tournament

    def round(self, tournament: Tournament) -> Tournament:
        """
        Split players to create matches, launch the round, get and display the scores.
        Args:
            tournament: An instance of tournament.
        Returns:
            tournament: An instance of tournament.
        """
        nbr_ronde = len(tournament.rondes) + 1
        ronde = Ronde("", "", "", [])
        ronde.number = str(nbr_ronde)
        self.view.item = f"\n         ----------Ronde N° {nbr_ronde}----------"
        self.view.display_item()
        tournament.chess_players.sort()
        ronde.matches = tournament.compute_matches()
        self.v_tournament.item = tournament
        self.v_tournament.display_matches(ronde.matches)
        ronde.date_start, ronde.date_end = self.start_end_ronde()
        tournament.chess_players, ronde.matches = self.v_tournament.get_scores(tournament.chess_players,
                                                                               ronde.matches)
        tournament.rondes.append(ronde)
        self.v_tournament.item = tournament
        tournament.chess_players.sort()
        self.v_tournament.display_score()
        return tournament

    def execute_rounds(self, tournament):
        """
        Manage main loop which execute a round depending of number_of_rounds parameter.
        Args:
            tournament: An instance of Tournament.
        """
        if self.manage_storage(tournament, update=True):
            while self.choice and len(tournament.rondes) < tournament.nbr_of_rounds:
                tournament = self.round(tournament)
                if len(tournament.rondes) < 4:
                    self.choice = self.manage_storage(tournament, update=True)
                else:
                    self.manage_storage(tournament, direct_update=True)
                    self.winner(tournament)

    def start_end_ronde(self) -> tuple:
        """
        Get and display the date and the hour for the start and the end of the round.
        Returns:
            date_start, date_end: date for the start and the end of the round.
        """
        self.view.display_text("start_ronde")
        utils.util.get_choice([""])
        self.view.display_text("good_luck")
        self.view.display_text("started_ronde")
        date_start = utils.util.get_date_now()
        self.view.item = date_start
        self.view.display_item(center=True)
        self.view.display_text("end_ronde")
        utils.util.get_choice([""])
        date_end = utils.util.get_date_now()
        self.view.item = date_end
        self.view.display_item(center=True)
        return date_start, date_end

    def delete_tournament(self, dict_tournaments: dict) -> Tournament:
        """
        Select a tournament from a dict, and return it to be deleted.
        Args:
            dict_tournaments: Dict from the database containing all tournaments.
        Returns:
            tournament: the selected tournament
        """
        tournament = self.select_tournament(dict_tournaments)
        if tournament:
            self.view.display_text("confirm_delete")
            return tournament

    def select_tournament(self, dict_tournaments: dict, display_all=True, report=False) -> Tournament:
        """
        Select a tournament from list.
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
            self.winner(tournament)

    def winner(self, tournament: Tournament):
        """
        Manage the display of the winner
        Args:
            tournament: An instance of tournament.
        """
        self.view.display_text("winner")
        self.view.item = f"{tournament.chess_players[0].player_from_chess_player().full_name()}\n"
        self.view.display_item()
        self.view.display_text("end_tournament", center=True)

    @staticmethod
    def _create_menu(menu):
        """
        Helper method to create a menu.
        Args:
            menu: Name of the menu, you want to create"
        Returns:
            An instance of Menu
        """
        tournament_menu = Menu(title="Menu de gestion des tournois: ",
                               add_info="(Tapez le chiffre correspondant à votre choix ou 'm' pour retourner au menu "
                                        "précédent: )",
                               items=["Ajouter un tournoi",
                                      "Reprendre un tournoi",
                                      "Supprimer un tournoi",
                                      "Afficher les rapports des tournois"],
                               choice="")

        save_or_cancel = Menu(title="Souhaitez-vous: ",
                              add_info="",
                              items=["Continuer",
                                     "Sauver et retourner au menu",
                                     "Annuler"],
                              choice="")
        delete_or_cancel = Menu(title="Souhaitez-vous:",
                                add_info="",
                                items=["Confirmer",
                                       "Annuler"],
                                choice="")

        dict_menu = {"tournament_menu": tournament_menu,
                     "save_or_cancel": save_or_cancel,
                     "delete_or_cancel": delete_or_cancel}
        return dict_menu[menu]
