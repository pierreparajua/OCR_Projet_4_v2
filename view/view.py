from colorama import init, Fore

import json
from pathlib import Path

import utils
from model.m_player import Player, storage_p
from model.m_tournament import ChessPlayer

init(autoreset=True)

SOURCE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = SOURCE_DIR / "Chess_manager_text.json"
DICT_TEXT = json.load(open(JSON_PATH, 'r', encoding='utf8'))


class View:
    def __init__(self, dict_text):
        self.dict_text = dict_text

    @staticmethod
    def display_instance(instance):
        """Display the requested instance"""
        print(instance)
        print("\n")

    @staticmethod
    def display_items(items, name_items, select=False):
        """Display a list of items in order depending on class"""
        items.sort()
        print(f"Liste des {name_items}: ")
        if select:
            print(f"Sélectionnez un {name_items[:-1]}: ")
        for i, item in enumerate(items):
            print(f"{i + 1}: {item}")

    @staticmethod
    def display_matches(matches: list):
        """ Display the matches for the next round"""
        if matches:
            for match, i in zip(matches, range(len(matches))):
                print(f"Match n°{i + 1}:\n"
                      f"    {match[0].full_name()} contre {match[1].full_name()}\n")

    @staticmethod
    def display_var(var, center=False):
        if center:
            print(f"   ----------{var}----------")
        else:
            print(var)

    def display_text(self, key, center=False):
        if center:
            print(f"   ----------{self.dict_text[key]}----------")
        else:
            print(self.dict_text[key])

    def select_item(self, items):
        """Select an item from a list and return it"""
        choice = utils.util.get_choice(list(map(str, list(range(1, len(items) + 1)))))
        self.display_text("selected_player")
        item = items[int(choice) - 1]
        self.display_instance(item)
        return item

    @staticmethod
    def get_scores(chess_players, matches):
        for match, i in zip(matches, range(len(matches))):
            player1 = Player.deserialize(storage_p.load(match[0]))
            player2 = Player.deserialize(storage_p.load(match[1]))
            print(Fore.LIGHTBLUE_EX + f"\nMatch n°{i + 1}: " + Fore.RESET +
                  f"    {player1.full_name()} - {player1.ranking}"
                  f"   contre   {player2.full_name()} - {player2.ranking}")
            print("Qui est le gagnant du match: \n"
                  f"1: pour {player1.full_name()}\n"
                  f"2: pour {player2.full_name()}\n"
                  f"3: pour égalité")
            choice = utils.util.get_choice(['1', '2', '3'])
            ChessPlayer.chess_player_from_id(chess_players, match[0]).score = 0
            ChessPlayer.chess_player_from_id(chess_players, match[1]).score = 0
            if choice == '1':
                print(f"{player1.full_name()} :" + Fore.LIGHTGREEN_EX + " 1 point")
                print(f"{player2.full_name()} :" + Fore.LIGHTRED_EX + " 0 point\n")
                x = ChessPlayer.chess_player_from_id(chess_players, match[0]).score = 1
                match[0] = (match[0], x)
                match[1] = (match[1], 0)

            elif choice == '2':
                print(f"{player1.full_name()} :" + Fore.LIGHTRED_EX + " 0 point")
                print(f"{player2.full_name()} :" + Fore.LIGHTGREEN_EX + " 1 point\n")
                y = ChessPlayer.chess_player_from_id(chess_players, match[1]).score = 1
                match[0] = (match[0], 0)
                match[1] = (match[1], y)
            elif choice == '3':
                print(f"{player1.full_name()} :" + Fore.LIGHTBLUE_EX + " 0.5 point")
                print(f"{player2.full_name()} :" + Fore.LIGHTBLUE_EX + " 0.5 point\n")
                x = ChessPlayer.chess_player_from_id(chess_players, match[0]).score = 0.5
                match[0] = (match[0], x)
                y = ChessPlayer.chess_player_from_id(chess_players, match[1]).score = 0.5
                match[1] = (match[1], y)
        return chess_players, matches
