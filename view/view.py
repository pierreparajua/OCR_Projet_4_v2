from colorama import init, Fore

import json
from pathlib import Path

import utils

init(autoreset=True)

SOURCE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = SOURCE_DIR / "Chess_manager_text.json"
DICT_TEXT = json.load(open(JSON_PATH, 'r', encoding='utf8'))


class View:
    def __init__(self, item):
        self.dict_text = DICT_TEXT
        self.item = item

    def display_item(self, center=False):
        if center:
            print(f"          ----------{self.item}----------")
        else:
            print(self.item)

    def display_items(self, name_items, select=False):
        """Display a list of items in order depending on class"""
        self.item.sort()
        print(f"\nListe des {name_items}: ")
        if select:
            print(f"Sélectionnez un {name_items[:-1]}: ")
        for i, item in enumerate(self.item):
            print(f"{i + 1}: {item}")

    def display_score(self):
        nbr_ronde = len(self.item.rondes)
        self.item.chess_players.sort()
        print(Fore.LIGHTGREEN_EX + f"Classement à l' issue de la ronde N° {nbr_ronde}: ")
        for chess_player in self.item.chess_players:
            print(f"{self.item.chess_players.index(chess_player) + 1}:"
                  f" {chess_player.player_from_chess_player().full_name(): <15}"
                  f" {chess_player.score_tot: >5} pts")

    def display_text(self, key, center=False):
        if center:
            print(f"   ----------{self.dict_text[key]}----------")
        else:
            print(self.dict_text[key])

    def display_tournaments(self):
        for i,  tournament in enumerate(self.item):
            print(f"{i + 1}:  Tournoi: {tournament.name}- le {tournament.date}")

    def select_item(self):
        """Select an item from a list and return it"""
        choice = input(Fore.LIGHTBLUE_EX + "Choix: ").lower()
        while choice not in list(map(str, list(range(1, len(self.item) + 1)))):
            choice = utils.util.wrong_entry(choice)
        self.display_text("selected_player")
        item = self.item[int(choice) - 1]
        print(item)
        return item

    @staticmethod
    def display_matches(matches: list):
        """ Display the matches for the next round"""
        if matches:
            for match, i in zip(matches, range(len(matches))):
                print(f"Match n°{i + 1}:\n"
                      f"    {match[0].full_name()} contre {match[1].full_name()}\n")
