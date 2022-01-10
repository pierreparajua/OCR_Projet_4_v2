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

    @staticmethod
    def display_items(items, name_items, select=False):
        """Display a list of items in order depending on class"""
        items.sort()
        print(f"\nListe des {name_items}: ")
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
    def display_item(item, center=False):
        if center:
            print(f"   ----------{item}----------")
        else:
            print(item)

    def display_text(self, key, center=False):
        if center:
            print(f"   ----------{self.dict_text[key]}----------")
        else:
            print(self.dict_text[key])

    def select_item(self, items):
        """Select an item from a list and return it"""
        choice = input(Fore.LIGHTBLUE_EX + "Choix: ").lower()
        while choice not in list(map(str, list(range(1, len(items) + 1)))):
            choice = utils.util.wrong_entry(choice)
        self.display_text("selected_player")
        item = items[int(choice) - 1]
        self.display_instance(item)
        return item
