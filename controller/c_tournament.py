import utils
from controller.c_player import PlayerController, storage_p
from model.m_player import Player
from view.v_get_data_tournament import GetDataTournament
from view.view import View, DICT_TEXT

NB_PLAYER_MAX = 20
NB_player = list(map(str, list(range(1, (NB_PLAYER_MAX + 1)))))[1::2]

player_controller = PlayerController()
got_tournament = GetDataTournament("", "", "", [], [], "", "")


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
        self.view.display_instance(tournament)
        self.view.display_items(players, "joueurs sélectionnés")
        tournament.players = players  # [storage_p.get_id(player) for player in players]
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


if __name__ == "__main__":
    test = TournamentController()
    test.prepare_tournament()
