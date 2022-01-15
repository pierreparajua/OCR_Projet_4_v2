import utils

from utils.util import Menu
from controller.c_player import PlayerManager, PlayerController

from model.m_storage import storage_t, storage_p
from model.m_tournament import Ronde, ChessPlayer, Tournament
from view.v_get_data_tournament import GetDataTournament
from view.view import View

NB_PLAYER_MAX = 20
NB_player = list(map(str, list(range(1, (NB_PLAYER_MAX + 1)))))[1::2]

player_controller = PlayerController()

chess_player = ChessPlayer(0, 0, 0, [])

save_or_quit_menu = Menu(title="Souhaitez-vous: ",
                         add_info="",
                         items=["Continuer",
                                "Sauver et retourner au menu",
                                "Annuler"],
                         choice="")


class TournamentController:
    """Control the main features of the tournaments"""

    def __init__(self):
        self.view: View = View("")
        self.got_tournament = GetDataTournament("", "", "", [], [], "", "")
        self.menu = save_or_quit_menu

    def prepare_tournament(self, dict_player) -> tuple:
        """Get all informations needed to start a tournament"""
        self.view.display_text("ask_for_player")
        choice: str = utils.util.get_choice(["o", "n"])
        while choice == "o":
            player_controller.add_player()
            self.view.display_text("add_player_again")
            choice = utils.util.get_choice(["o", "n"])
        self.view.display_text("new_tournament", center=True)
        self.view.display_text("fill_items")
        tournament = self.got_tournament.create_tournament()
        players = self.select_players(tournament.nbr_of_rounds, dict_player)
        self.view.display_text("resume_tournament", center=True)
        self.view.item = tournament
        self.view.display_item()
        self.view.item = players
        self.view.display_items("joueurs sélectionnés")
        tournament.chess_players = [chess_player.create_chess_player(player) for player in players]
        self.menu.display_menu()
        choice = self.menu.get_choice()
        if choice == "1" or "2":
            return tournament, choice

    def select_players(self, nb_round: int, dict_player) -> list:
        """Select players for the tournament"""
        players_selected = []
        self.view.display_text("nb_player")
        nb_players = int(utils.util.get_choice(NB_player))  # Check if the number of players is even
        while nb_players / 2 < nb_round:
            self.view.display_text("error_nb_player")
            nb_players = int(utils.util.get_choice(NB_player))
        players = player_controller.display_all_players(dict_player)
        self.view.item = players

        i = 0
        while i < nb_players:
            player = self.view.select_item()
            if player in players_selected:
                self.view.display_text("already_selected")
            else:
                players_selected.append(player)
                i += 1
        players_selected.sort()
        return players

    def round1(self, tournament: Tournament) -> Tournament:
        """Execute the first round"""
        ronde1 = Ronde("1", "", "", [])
        self.view.display_text("ronde1", center=True)
        players_split1, players_split2 = utils.util.split_players(tournament.chess_players)
        ronde1.matches = [[players_split1[i].id_player, players_split2[i].id_player]
                          for i in range(int(len(tournament.chess_players) / 2))]
        self.view.display_matches(ronde1.matches, tournament.chess_players)
        ronde1.date_start, ronde1.date_end = self.start_end_ronde()
        tournament.chess_players, ronde1.matches = self.got_tournament.get_scores(tournament.chess_players,
                                                                                  ronde1.matches)
        tournament.rondes.append(ronde1)
        self.view.item = tournament
        self.view.display_score()
        self.menu.display_menu()
        choice = self.menu.get_choice()
        if choice == "1":
            return tournament

    def round(self, tournament: Tournament) -> Tournament:
        """Execute the others rounds"""
        nbr_ronde = len(tournament.rondes) + 1
        ronde = Ronde("", "", "", [])
        ronde.number = str(nbr_ronde)
        self.view.item = f"\n         ----------Ronde N° {nbr_ronde}----------"
        self.view.display_item()
        ronde.matches = tournament.compute_matches()
        ronde.date_start, ronde.date_end = self.start_end_ronde()
        tournament.chess_players, ronde.matches = self.got_tournament.get_scores(tournament.chess_players,
                                                                                 ronde.matches)
        tournament.rondes.append(ronde)
        self.view.item = tournament
        self.view.display_score()
        self.menu.display_menu()
        choice = self.menu.get_choice()
        if choice == "1":
            return tournament

    def start_end_ronde(self) -> tuple:
        """Get the date and the hour for the start and the end of the round"""
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
        """Delete the selected tournament from database"""
        tournament = self.select_tournament(dict_tournaments)
        if tournament:
            self.view.display_text("confirm_delete")
            self.view.display_text("confirm_deleted")
            return tournament

    def select_tournament(self, dict_tournaments: dict, display_all=True, report=False) -> Tournament:
        """Select a tournament from list.
            If 'display_all' is false: the list contains only the unterminated tournament.
            If report is True: the list containing only  the terminated tournament"""
        tournaments = [Tournament.deserialize(tournament) for tournament in dict_tournaments]
        if report:
            tournaments = [tournament for tournament in tournaments if len(tournament.rondes) == 4]
        else:
            tournaments = [tournament for tournament in tournaments if len(tournament.rondes) != 4
                           or display_all]
        if tournaments:
            self.view.item = tournaments
            self.view.display_tournaments()
            tournament = self.view.select_item()
            return tournament
        self.view.display_text("db_empty_tournament")

    def report(self, tournament: Tournament):
        """Manage the display of the report"""
        if tournament:
            self.view.item = tournament
            self.view.display_ronde()
            self.view.display_score()
            self.winner(tournament)

    def winner(self, tournament: Tournament):
        """Manage the display of the winner"""
        self.view.display_text("winner")
        self.view.item = f"{tournament.chess_players[0].player_from_chess_player().full_name()}\n"
        self.view.display_item()
        self.view.display_text("end_tournament", center=True)


tournament_menu = Menu(title="Menu de gestion des tournois: ",
                       add_info="(Tapez le chiffre correspondant à votre choix ou 'm' pour retourner au menu "
                                "précédent: )",
                       items=["Ajouter un tournois",
                              "Reprendre un tournois",
                              "Supprimer un tournois",
                              "Afficher les rapports de tournois"],
                       choice="")


class TournamentManager:
    """docstring"""

    def __init__(self):
        self.menu = tournament_menu

        self.controller = TournamentController()

    def tournament_manager(self):
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()
        if self.menu.choice == "1":
            tournament, choice = self.controller.prepare_tournament(self.storage_p.load_all())
            if choice == "2":
                tournament.id_db = self.storage_t.save(tournament)
                self.storage_t.update(tournament)
                self.tournament_manager()
            elif choice == "1":
                tournament.id_db = self.storage_t.save(tournament)
                self.storage_t.update(tournament)
                tournament = self.controller.round1(tournament)
                if tournament:
                    print("ok")
                    self.storage_t.update(tournament)
                    for _ in tournament.nbr_of_rounds:
                        tournament = self.controller.round(tournament)
            self.tournament_manager()

        elif self.menu.choice == "2":
            tournament = tournament_controller.select_tournament(storage_t.load_all(), display_all=False)
            if tournament:
                self.continue_tournament(tournament)
            self.tournament_manager()

        elif self.menu.choice == "3":
            while self.choice_save == "1":
                tournament = tournament_controller.delete_tournament(storage_t.load_all())
                if tournament:
                    self.choice_save = self.delete_or_quit(tournament, storage_t)
                else:
                    self.choice_save = "2"
            self.tournament_manager()

        elif self.menu.choice == "4":
            tournament = tournament_controller.select_tournament(storage_t.load_all(), report=True)
            tournament_controller.report(tournament)
            self.tournament_manager()

        elif self.menu.choice == "m":
            self.main_manager()
