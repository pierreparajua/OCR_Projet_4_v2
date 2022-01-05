import utils
from controller.c_player import PlayerController
from model.m_player import Player
from model.m_storage import Tinydb, db_players
from view.v_get_data_tournament import GetDataTournament
from view.view import View, DICT_TEXT

NB_PLAYER_MAX = 20
NB_player = list(map(str, list(range(1, (NB_PLAYER_MAX + 1)))))[1::2]

player_controller = PlayerController()
got_tournament = GetDataTournament("", "", "", [], [], "", "")
storage_p = Tinydb(db_players, Player("", "", "", ""))


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
        tournament.players = players
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
        return players_selected

    def round1(self):
        """Execute the first round"""
        ronde1 = Ronde("", "", "", "")
        ronde1.number = "1"
        view.v_tournament.display_number_ronde(ronde1)
        players_split1, players_split2 = model.m_players.split_players(tournament.players)
        nb_players = int(len(tournament.players))
        half_nb_player = int(nb_players / 2)
        matches1 = [[players_split1[i], players_split2[i]] for i in range(half_nb_player)]
        view.v_tournament.display_matches(matches1)
        ronde1.date_start, ronde1.date_end = start_end_ronde()
        view.v_tournament.display_manage_tournament("get_score")
        ronde1.matches = view.v_tournament.get_scores(matches1)
        ronde1.compute_score()
        ronde1.add_opponent()
        return ronde1


if __name__ == "__main__":
    """
    test = TournamentController()

    caroline = Player("caroline", "sejil", "12/02/1984", "femme", 1, 1230)
    damien = Player("damien", "parajua", "08/05/1984", "femme", 1, 1130)
    pierre = Player("pierre", "yves", "08/02/1989", "homme", 1, 1250)
    eddy = Player("eddy", "sejil", "08/02/1984", "homme", 1, 1098)
    players = [caroline, damien, pierre, eddy]

    tournament = Tournament("master", "lyon", "05/02/2002", [], players, "Blitz", "test", 1, 4)
    test.view.display_instance(tournament)
    storage_t.item = tournament
    storage_t.save()
    storage_t.update()
    """
