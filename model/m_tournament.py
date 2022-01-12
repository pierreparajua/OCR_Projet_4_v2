
from dataclasses import dataclass
from colorama import Fore
import random

import utils
from model.m_player import Player
from model.m_storage import Tinydb, db_tournaments, db_players

storage_t = Tinydb(db_tournaments)
storage_p = Tinydb(db_players)


class Tournament:
    def __init__(self, name: str, place: str, date: str, rondes: list, chess_players: list, time: str,
                 description: str, id_db: int = 1, nbr_of_rounds=4):
        self.name = name
        self.place = place
        self.date = date
        self.rondes = rondes
        self.chess_players = chess_players
        self.time = time
        self.description = description
        self.id_db = id_db
        self.nbr_of_rounds = nbr_of_rounds

    def __str__(self):
        """Display tournament's attributes."""
        return (Fore.LIGHTWHITE_EX + "Tournois: " + Fore.RESET + f"{self.name}\n"
                + Fore.LIGHTWHITE_EX + "Lieu: " + Fore.RESET + f"{self.place}\n"
                + Fore.LIGHTWHITE_EX + "Date: " + Fore.RESET + f"{self.date}\n"
                + Fore.LIGHTWHITE_EX + "Nombre de tours: " + Fore.RESET + f"{self.nbr_of_rounds}\n"
                + Fore.LIGHTWHITE_EX + "Liste des rondes: " + Fore.RESET + f"Nombre de rondes deja joués: "
                                                                           f"{len(self.rondes)}\n"
                + Fore.LIGHTWHITE_EX + "Système de contrôle du temps: " + Fore.RESET + f"{self.time}\n"
                + Fore.LIGHTWHITE_EX + "Remarque du directeur de tournois: " + Fore.RESET + f"{self.description}")

    def __lt__(self, other):
        """Sort the players by date"""
        return self.date < other.date

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = utils.util.check_name(value).lower()

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        self._place = utils.util.check_name(value).lower()

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = utils.util.check_date(value).lower()

    @property
    def nbr_of_rounds(self):
        return self._nbr_of_rounds

    @nbr_of_rounds.setter
    def nbr_of_rounds(self, value):
        if value:
            self._nbr_of_rounds = utils.util.check_ranking(value)
        else:
            self._nbr_of_rounds = 4

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = utils.util.check_name(value).lower()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value.lower()

    @staticmethod
    def deserialize(tournament_dict: dict):
        """Create an instance of Tournament."""
        tournament = Tournament(tournament_dict["name"],
                                tournament_dict["place"],
                                tournament_dict["date"],
                                [Ronde.deserialize(ronde) for ronde in tournament_dict["rondes"]],
                                [ChessPlayer.deserialize(player) for player in tournament_dict["chess_players"]],
                                tournament_dict["time"],
                                tournament_dict["description"],
                                tournament_dict["id_db"],
                                tournament_dict["nbr_of_rounds"])

        return tournament

    @staticmethod
    def create_matches(chess_players: list) -> list:
        """From a list of 'chess_player' create a list of matches for the next ronde"""
        new_matches = []
        for t in range(int(len(chess_players) / 2)):
            ind = 0
            i = 1
            while chess_players[0].id_player in chess_players[ind + i].opponents:
                i += 1
                if i == len(chess_players):
                    return []
            new_matches.append([chess_players[0], chess_players[ind + i]])
            chess_players.pop(ind + i)
            chess_players.pop(0)
        return new_matches

    def compute_matches(self) -> list:
        """If 'create_matches' is enable to work correctly, shuffle the list of chess_player and try again"""
        matches = self.create_matches(Tournament.deserialize(storage_t.load(self)).chess_players)
        while not matches:
            chess_players = Tournament.deserialize(storage_t.load(self)).chess_players
            random.shuffle(chess_players)
            matches = self.create_matches(chess_players)
        matches = [[match[0].id_player, match[1].id_player] for match in matches]
        self.chess_players = self.deserialize(storage_t.load(self.id_db)).chess_players
        return matches

    def serialize(self) -> dict:
        """Create a dict from an instance of tournament to save it in database"""
        dict_tournament = {"name": self.name,
                           "place": self.place,
                           "date": self.date,
                           "rondes": [Ronde.serialize(ronde) for ronde in self.rondes],
                           "chess_players": [ChessPlayer.serialize(player) for player in self.chess_players],
                           "time": self.time,
                           "description": self.description,
                           "id_db": self.id_db,
                           "nbr_of_rounds": self.nbr_of_rounds}
        return dict_tournament


class Ronde:
    def __init__(self, number: str, date_start: str, date_end: str, matches: list):
        self.number = number
        self.date_start = date_start
        self.date_end = date_end
        self.matches = matches

    def __str__(self):
        """Display ronde's attributes."""
        return f"number: {self.number}\n" \
               f"date de début: {self.date_start}\n" \
               f"date de fin: {self.date_end}\n" \
               f"matchs: {self.matches}"

    @staticmethod
    def deserialize(ronde_dict: dict):
        """Create an instance of Ronde."""
        ronde = Ronde(ronde_dict["number"],
                      ronde_dict["date_start"],
                      ronde_dict["date_end"],
                      ronde_dict["matches"])
        return ronde

    def serialize(self) -> dict:
        """Serialize a Ronde instance"""
        dict_ronde = {"number": self.number,
                      "date_start": self.date_start,
                      "date_end": self.date_end,
                      "matches": self.matches}
        return dict_ronde


@dataclass
class ChessPlayer:
    """A ChessPlayer in a player selected for a tournament.
    The matching between a Player and a ChessPlayer is the id"""
    id_player: int
    score: float
    score_tot: float
    opponents: list

    def __lt__(self, other):
        """Sort the chess_players by score_tot"""
        return self.score_tot > other.score_tot

    @staticmethod
    def deserialize(chess_player_dict: dict):
        """Create an instance of ChessPlayer."""
        chess_player = ChessPlayer(chess_player_dict["id_player"],
                                   chess_player_dict["score"],
                                   chess_player_dict["score_tot"],
                                   chess_player_dict["opponents"])
        return chess_player

    def create_chess_player(self, player: Player):
        """From a player create a chess_player"""
        self.id_player = player.id_db
        chess_player = ChessPlayer(self.id_player,
                                   score=0,
                                   score_tot=0,
                                   opponents=[])
        return chess_player

    def player_from_chess_player(self) -> Player:
        """From a ChessPlayer return a Player"""
        return Player.deserialize(storage_p.load(self.id_player))

    def serialize(self):
        dict_chess_player = {"id_player": self.id_player,
                             "score": self.score,
                             "score_tot": self.score_tot,
                             "opponents": self.opponents}
        return dict_chess_player
