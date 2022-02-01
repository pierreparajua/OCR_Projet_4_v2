from colorama import Fore

from dataclasses import dataclass

import utils
from model.m_player import Player
from model.m_storage import storage_t


class Tournament:
    def __init__(self, name: str = "", place: str = "", date: str = "", rondes: list = None,
                 players: list = None, time: str = "", description: str = "", id_db: int = 1, nbr_of_rounds=4):
        self.name = name
        self.place = place
        self.date = date
        self.rondes = rondes
        self.players = players
        self.time = time
        self.description = description
        self.id_db = id_db
        self.nbr_of_rounds = nbr_of_rounds

    def __str__(self):
        """Display tournament's attributes."""
        return (Fore.LIGHTWHITE_EX + "Tournoi: " + Fore.RESET + f"{self.name}\n"
                + Fore.LIGHTWHITE_EX + "Lieu: " + Fore.RESET + f"{self.place}\n"
                + Fore.LIGHTWHITE_EX + "Date: " + Fore.RESET + f"{self.date}\n"
                + Fore.LIGHTWHITE_EX + "Nombre de tours: " + Fore.RESET + f"{self.nbr_of_rounds}\n"
                + Fore.LIGHTWHITE_EX + "Liste des rondes: " + Fore.RESET + f"Nombre de rondes deja jouées: "
                                                                           f"{len(self.rondes)}\n"
                + Fore.LIGHTWHITE_EX + "Système de contrôle du temps: " + Fore.RESET + f"{self.time}\n"
                + Fore.LIGHTWHITE_EX + "Remarque du directeur de tournoi: " + Fore.RESET + f"{self.description}")

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
        """
        Create an instance of Tournament.
        Args:
            tournament_dict:  A dict containing all tournament's informations, coming from database
        Returns:
            tournament: an instance fo Tournament
        """
        tournament = Tournament(tournament_dict["name"],
                                tournament_dict["place"],
                                tournament_dict["date"],
                                [Round.deserialize(ronde) for ronde in tournament_dict["rondes"]],
                                tournament_dict["players"],
                                tournament_dict["time"],
                                tournament_dict["description"],
                                tournament_dict["id_db"],
                                tournament_dict["nbr_of_rounds"])

        return tournament

    def split_players(self) -> tuple:
        """Split the main list in 2, according with the tournament's rules"""
        nb = int(len(self.players) / 2)
        players_split1 = self.players[0: nb]
        players_split2 = self.players[nb: int(nb * 2)]
        return players_split1, players_split2

    @staticmethod
    def create_matches(players: list) -> list:
        """
        From a list of player, create a list of matches for the next round.
        Args:
            players: List of Player
        Returns:
            new_matches : List of matches for the next round
        """
        new_matches = []
        for _ in range(int(len(players) / 2)):
            i = 1
            while players[0].id_db in players[i].opponents:
                i += 1
                if i == len(players):
                    return []
            new_matches.append([players[0], players[i]])
            players.pop(i)
            players.pop(0)
        return new_matches

    def compute_matches(self) -> list:
        """
        If for 'create_matches' is impossible to find a solution (most of the time when the last two players have
        already playing together) 'compute_player' changes the order from the end of the list until 'create_player
         finds a solution.
        Returns:
            matches: List of matches for the round
        """
        matches = self.create_matches(self.players)
        i = 0
        while not matches:
            i += 1
            tournament = self.deserialize(storage_t.load(self.id_db))
            tournament.add_score_and_opponents()
            players = tournament.players
            players[-i], players[-i + -1] = players[-i + -1], players[-i]
            matches = self.create_matches(players)
        matches = [[match[0].id_db, match[1].id_db] for match in matches]
        tournament = self.deserialize(storage_t.load(self.id_db))
        self.players = tournament.players
        self.add_score_and_opponents()
        return matches

    def serialize(self) -> dict:
        """
        Create a dict from an instance of tournament to save it in database
        Returns:
            dict_tournament: A dict containing all tournament's informations to save in database.
        """
        dict_tournament = {"name": self.name,
                           "place": self.place,
                           "date": self.date,
                           "rondes": [Round.serialize(ronde) for ronde in self.rondes],
                           "players": self.players,
                           "time": self.time,
                           "description": self.description,
                           "id_db": self.id_db,
                           "nbr_of_rounds": self.nbr_of_rounds}
        return dict_tournament

    def create_list_of_matches(self):
        """
        From all the rounds in the tournament, create a list with all couples [id_players, score]
        Returns:
            all_matches: list with all couples [id_players, score]
        """
        all_matches = []
        for ronde in self.rondes:
            for match in ronde.matches:
                all_matches.append(match[0])
                all_matches.append(match[1])
        return all_matches

    def add_score_and_opponents(self):
        """
        Use method 'create_list_of_matches' to compute the score and opponents for each player depending on this
        previous matches.
        Then add dynamically, the attributs self.score and self.opponents to the tournament
        """
        all_matches = self.create_list_of_matches()
        if all_matches:
            players = [Player.player_from_id(player) for player in self.players]
            Player.score = 0
            for player in players:
                for t_player in all_matches:
                    if player.id_db == t_player[0]:
                        player.score += t_player[1]
            players.sort()
            self.players = players
            Player.opponents = []
            for player in players:
                opponents = []
                for i, t_player in zip(range(len(all_matches)), all_matches):
                    if player.id_db == t_player[0]:
                        if i < len(all_matches) - 1 and (i % 2) == 0:
                            opponents.append(all_matches[i + 1][0])
                        elif i == len(all_matches) - 1 or (i % 2) != 0:
                            opponents.append(all_matches[i - 1][0])
                player.opponents = opponents
            self.players = players


@dataclass
class Round:
    number: int
    date_start: str
    date_end: str
    matches: list

    def __str__(self):
        """Display ronde's attributes."""
        return f"number: {self.number}\n" \
               f"date de début: {self.date_start}\n" \
               f"date de fin: {self.date_end}\n" \
               f"matchs: {self.matches}"

    @staticmethod
    def deserialize(ronde_dict: dict):
        """Create an instance of Ronde."""
        ronde = Round(number=ronde_dict["number"],
                      date_start=ronde_dict["date_start"],
                      date_end=ronde_dict["date_end"],
                      matches=ronde_dict["matches"])
        return ronde

    def serialize(self) -> dict:
        """Serialize a Ronde instance"""
        dict_ronde = {"number": self.number,
                      "date_start": self.date_start,
                      "date_end": self.date_end,
                      "matches": self.matches}
        return dict_ronde
