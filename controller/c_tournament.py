import utils
from controller.c_player import PlayerController
from model.m_player import Player
from model.m_storage import Tinydb, db_players
from model.m_tournament import Ronde, ChessPlayer
from view.v_get_data_tournament import GetDataTournament
from view.view import View

NB_PLAYER_MAX = 20
NB_player = list(map(str, list(range(1, (NB_PLAYER_MAX + 1)))))[1::2]

player_controller = PlayerController()
storage_p = Tinydb(db_players)
chess_player = ChessPlayer(0, 0, 0, [])


class TournamentController:
    def __init__(self, ):
        self.got_tournament = GetDataTournament("", "", "", [], [], "", "")
        self.view: View = View("")

    def prepare_tournament(self):
        self.view.display_text("ask_for_player")
        choice: str = utils.util.get_choice(["o", "n"])
        while choice == "o":
            player_controller.add_player()
            self.view.display_text("add_player_again")
            choice = utils.util.get_choice(["o", "n"])
        self.view.display_text("new_tournament", center=True)
        self.view.display_text("fill_items")
        tournament = self.got_tournament.create_tournament()
        players = self.select_players(tournament.nbr_of_rounds)
        self.view.display_text("resume_tournament", center=True)
        self.view.item = tournament
        self.view.display_item()
        self.view.item = players
        self.view.display_items("joueurs sélectionnés")
        tournament.chess_players = [chess_player.create_chess_player(player) for player in players]
        return tournament

    def select_players(self, nb_round: int) -> list:
        players_selected = []
        self.view.display_text("nb_player")
        nb_players = int(utils.util.get_choice(NB_player))  # Check if the number of players is even
        while nb_players / 2 < nb_round:
            self.view.display_text("error_nb_player")
            nb_players = int(utils.util.get_choice(NB_player))
        dict_players = storage_p.load_all()
        players = [Player.deserialize(dict_player) for dict_player in dict_players]
        self.view.item = players
        self.view.display_items("joueurs", select=True)
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

    def round1(self, tournament):
        """Execute the first round"""
        ronde1 = Ronde("1", "", "", "")
        self.view.display_text("ronde1", center=True)
        players_split1, players_split2 = utils.util.split_players(tournament.chess_players)
        ronde1.matches = [[players_split1[i].id_player, players_split2[i].id_player]
                          for i in range(int(len(tournament.chess_players) / 2))]
        ronde1.date_start, ronde1.date_end = self.start_end_ronde()
        tournament.chess_players, ronde1.matches = self.got_tournament.get_scores(tournament.chess_players,
                                                                                  ronde1.matches)
        tournament.rondes.append(ronde1)
        self.view.item = tournament
        self.view.display_score()
        return tournament

    def ronde(self, tournament):
        nbr_ronde = len(tournament.rondes) + 1
        print(nbr_ronde)
        ronde = Ronde(nbr_ronde, "", "", "")

    def start_end_ronde(self):
        """
        Gets the date and the hour for the start and the end of the round.
        Returns:
            date_start, date_end(tuple): with date and hour
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
