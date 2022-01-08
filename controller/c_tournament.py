import utils
from controller.c_player import PlayerController
from model.m_player import Player
from model.m_storage import Tinydb, db_players
from model.m_tournament import Ronde, ChessPlayer
from view.v_get_data_tournament import GetDataTournament
from view.view import View, DICT_TEXT

NB_PLAYER_MAX = 20
NB_player = list(map(str, list(range(1, (NB_PLAYER_MAX + 1)))))[1::2]

player_controller = PlayerController()
got_tournament = GetDataTournament("", "", "", [], [], "", "")
storage_p = Tinydb(db_players)
chess_player = ChessPlayer(0, 0, 0, [])


class TournamentController:
    def __init__(self, ):
        self.view: View = View(DICT_TEXT)

    def prepare_tournament(self):
        self.view.display_text("ask_for_player")
        choice: str = utils.util.get_choice(["o", "n"])
        while choice == "o":
            player_controller.add_player()
            self.view.display_text("add_player_again")
            choice = utils.util.get_choice(["o", "n"])
        self.view.display_text("new_tournament", center=True)
        self.view.display_text("fill_items")
        tournament = got_tournament.create_tournament()
        players = self.select_player(tournament.nbr_of_rounds)
        self.view.display_text("resume_tournament", center=True)
        self.view.display_instance(tournament)
        self.view.display_items(players, "joueurs sélectionnés")
        tournament.chess_players = [chess_player.create_chess_player(player) for player in players]
        return tournament

    def select_player(self, nb_round: int) -> list:
        players_selected = []
        self.view.display_text("nb_player")
        nb_players = int(utils.util.get_choice(NB_player))  # Check if the number of players is even
        while nb_players / 2 < nb_round:
            self.view.display_text("error_nb_player")
            nb_players = int(utils.util.get_choice(NB_player))
        dict_players = storage_p.load_all()
        players = [Player.deserialize(dict_player) for dict_player in dict_players]
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
        return players

    def round1(self, tournament):
        """Execute the first round"""
        ronde1 = Ronde("1", "", "", "")
        self.view.display_text("ronde1", center=True)
        players_split1, players_split2 = utils.util.split_players(tournament.chess_players)
        ronde1.matches = [[players_split1[i].id_player, players_split2[i].id_player]
                          for i in range(int(len(tournament.chess_players) / 2))]

        tournament.chess_players = Ronde.add_opponents(tournament.chess_players, ronde1.matches)
        tournament.chess_players, ronde1.matches = View.get_scores(tournament.chess_players, ronde1.matches)
        tournament.rondes.append(ronde1)
        return tournament

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
        View.display_var(date_start, center=True)
        self.view.display_text("end_ronde")
        utils.util.get_choice([""])
        date_end = utils.util.get_date_now()
        self.view.display_text("ended_ronde")
        View.display_var(date_end, center=True)
        return date_start, date_end


if __name__ == "__main__":
    """
    matches = [[1, 6], [2, 3], [4, 5], [7, 8]]

    for match in matches:
        match[0] = (match[0], 2)
        match[1] = (match[1], 3)

*
    test = TournamentController()
    storage_t = Tinydb(db_tournaments)
    players = [1, 2, 3, 4, 5, 6, 7, 8]
    tournament = Tournament("master", "lyon", "05/02/2002", [], players, "Blitz", "test", 1, 4)
    tournament.chess_players = [chess_player.create_chess_player(player) for player in players]
    test.round1(tournament)
    tournament.id_db = storage_t.save(tournament)
    storage_t.update(tournament)

    ronde1 = Ronde("1", "", "", "")
    test = TournamentController()
    players_split1, players_split2 = utils.util.split_players(tournament.chess_players)
    ronde1.matches = [[players_split1[i].id_player, players_split2[i].id_player]
                      for i in range(int(len(tournament.chess_players) / 2))]
    print(tournament.chess_players)
    tournament.chess_players = Ronde.add_opponents(tournament.chess_players, ronde1.matches)
    print(tournament.chess_players)
    tournament.chess_players = View.get_scores(tournament.chess_players, ronde1.matches)
    tournament.rondes.append(ronde1)
    print(tournament.chess_players)
    print(tournament.rondes[0].matches)
    storage_t.save(tournament)
    """
