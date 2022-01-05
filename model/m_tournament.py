
from colorama import Fore

import utils


class Tournament:
    def __init__(self, name: str, place: str, date: str, rondes: list, players: list, time: str, description: str,
                 id_db: int = 1, nbr_of_rounds=4):
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
        return (Fore.LIGHTWHITE_EX + "Tournois: " + Fore.RESET + f"{self.name}\n"
                + Fore.LIGHTWHITE_EX + "Lieu: " + Fore.RESET + f"{self.place}\n"
                + Fore.LIGHTWHITE_EX + "Date: " + Fore.RESET + f"{self.date}\n"
                + Fore.LIGHTWHITE_EX + "Nombre de tours: " + Fore.RESET + f"{self.nbr_of_rounds}\n"
                + Fore.LIGHTWHITE_EX + "Liste des rondes: " + Fore.RESET + f"Nombre de rondes deja joués: "
                                                                           f"{len(self.rondes)}\n"
                + Fore.LIGHTWHITE_EX + "Système de contrôle du temps: " + Fore.RESET + f"{self.time}\n"
                + Fore.LIGHTWHITE_EX + "Remarque du directeur de tournois: " + Fore.RESET + f"{self.description}\n")

    def __lt__(self, other):
        return self.date > other.date

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





class Ronde:
    def __init__(self, number, date_start, date_end, matches):
        self.number = number
        self.date_start = date_start
        self.date_end = date_end
        self.matches = matches

    def __str__(self):
        return f"number: {self.number}\n" \
               f"date de début: {self.date_start}\n" \
               f"date de fin: {self.date_end}\n" \
               f"matchs: {self.matches}"

    def add_opponent(self):
        """ Save in  the Chess_player the players already met."""
        for match in self.matches:
            match[0].opponent.append(match[1].id)
            match[1].opponent.append(match[0].id)

    def compute_score(self):
        """ Compute the total score"""
        for match in self.matches:
            match[0].add_score()
            match[1].add_score()

    def serialize_ronde(self) -> dict:
        """
        Serialize a Ronde instance.
        Returns
            dict_ronde(dict): dict from Ronde' s instance
        """
        dict_match = []
        for match in self.matches:
            dict_match.append([match[0].serialize(), match[1].serialize()])
        dict_ronde = {"number": self.number,
                      "date_start": self.date_start,
                      "date_end": self.date_end,
                      "matches": dict_match}
        return dict_ronde

    @staticmethod
    def serialize_rondes(rondes: list) -> list:
        """Return a list with all rondes to save in database."""
        dict_rondes = [ronde.serialize_ronde() for ronde in rondes]
        return dict_rondes
