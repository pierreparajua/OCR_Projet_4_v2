from colorama import init

import json
from pathlib import Path

import utils

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
        print(f"Liste des {name_items}: ")
        if select:
            print(f"Sélectionnez un {name_items[:-1]}: ")
        for i, item in enumerate(items):
            print(f"{i + 1}: {item}")

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
