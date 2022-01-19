from colorama import init, Fore

import json
from pathlib import Path

import utils

init(autoreset=True)

SOURCE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = SOURCE_DIR / "Chess_manager_text.json"
DICT_TEXT = json.load(open(JSON_PATH, 'r', encoding='utf8'))


class View:
    """Manage the main displays."""
    def __init__(self, item):
        self.dict_text = DICT_TEXT
        self.item = item

    def display_item(self, center=False):
        """
        Display an item."
        Args:
            center: Display the item at the center
        """""
        if center:
            print(f"          ----------{self.item}----------")
        else:
            print(self.item)

    def display_items(self, name_items: str, select=False):
        """
        Display a list of items.
        Args:
            name_items: name to the items to print.
            select: If True, print an specific sentence
        """
        self.item.sort()
        print(f"\nListe des {name_items}: ")
        if select:
            print(f"Sélectionnez un {name_items[:-1]}: ")
        for i, item in enumerate(self.item):
            print(f"{i + 1}: {item}")

    def display_score(self):
        """Display the score for each player at the end of a round"""
        nbr_ronde = len(self.item.rondes)
        print(Fore.LIGHTGREEN_EX + f"Classement à l' issue de la ronde N° {nbr_ronde}: ")
        for chess_player in self.item.chess_players:
            print(f"{self.item.chess_players.index(chess_player) + 1}:"
                  f" {chess_player.player_from_chess_player().full_name(): <15}"
                  f" {chess_player.score_tot: >5} pts")
        print("\n")

    def display_text(self, key: str, center=False):
        """
        Display the text matching with the key from the dict 'chess_manager_text.json.
        Args:
            key: Key from the dict 'chess_manager_text.json.
            center: IF True, display the item at the center
        """
        if center:
            print(f"   ----------{self.dict_text[key]}----------")
        else:
            print(self.dict_text[key])

    def display_tournaments(self):
        """Display all tournament."""
        for i, tournament in enumerate(self.item):
            print(f"{i + 1}:  Tournoi: {tournament.name} - le {tournament.date}")

    def select_item(self):
        """Select an item and return it"""
        choice = input(Fore.LIGHTBLUE_EX + "Choix: ").lower()
        while choice not in list(map(str, list(range(1, len(self.item) + 1)))):
            choice = utils.util.wrong_entry(choice)
        self.display_text("selected_player")
        item = self.item[int(choice) - 1]
        print(item)
        return item

    @staticmethod
    def display_matches(matches: list, chess_players):
        """ Display the matches for the next round"""
        if matches:
            for match, i in zip(matches, range(len(matches))):
                chess_player1 = next(chess for chess in chess_players if chess.id_player == match[0])
                chess_player2 = next(chess for chess in chess_players if chess.id_player == match[1])
                print(f"Match n°{i + 1}:\n"
                      f"    {chess_player1.full_name} contre {chess_player2.full_name}\n")

    def display_ronde(self):
        """Display all matches inside each rounds for report"""
        for ronde in self.item.rondes:
            print(Fore.LIGHTGREEN_EX + f"\nRONDE N° {ronde.number}  début: {ronde.date_start}  fin: {ronde.date_end} ")
            for match in ronde.matches:
                chess_player1 = next(chess for chess in self.item.chess_players if chess.id_player == match[0][0])
                chess_player2 = next(chess for chess in self.item.chess_players if chess.id_player == match[1][0])
                x = ""
                print(f"{chess_player1.full_name: <14}: {match[0][1]: >5} pt    contre   "
                      f"{chess_player2.full_name: >15}: {match[1][1]: >5}pt {x: <15}")
        print("\n")
