from colorama import init, Fore

import json
from pathlib import Path

import utils

init(autoreset=True)

SOURCE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = SOURCE_DIR / "Chess_manager_text.json"
DICT_TEXT = json.load(open(JSON_PATH, 'r', encoding='utf8'))


class View:
    """Manage the display of generic items."""
    def __init__(self, item=None):
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

    def select_item(self, items):
        """Select an item and return it"""
        choice = input(Fore.LIGHTBLUE_EX + "Choix: ").lower()
        while choice not in list(map(str, list(range(1, len(items) + 1)))):
            choice = utils.util.wrong_entry(choice)
        self.display_text("selected_item")
        item = items[int(choice) - 1]
        print(item)
        return item
