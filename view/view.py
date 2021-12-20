from colorama import Fore, init

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
        print(instance)

    @staticmethod
    def display_items(items, name_item, select=False):
        items.sort()
        print(f"Liste des {name_item} en base de donnée:")
        if select:
            print(f"Sélectionnez le {name_item[:-1]}: ")
        for i, player in enumerate(items):
            print(f"{i + 1}: {player}")

    def display_text(self, key):
        print(self.dict_text[key])

    def select_item(self, items):
        choice = utils.util.get_choice(list(map(str, list(range(1, len(items) + 1)))))
        self.display_text("selected_player")
        old_player = items[int(choice) - 1]
        self.display_instance(old_player)
        return old_player


class View_menu:
    def __init__(self, title, add_info, items, choice):
        self.title: str = title
        self.add_info: str = add_info
        self.items: list = items
        self.choice: str = choice

    def display_menu(self):
        print(Fore.LIGHTMAGENTA_EX + f"\n{self.title}:" + Fore.LIGHTWHITE_EX + f" {self.add_info}")
        for i, item in enumerate(self.items):
            print(f"{i + 1}: {item} ")

    def get_choice_list(self):
        choices_list = list(map(str, list(range(len(self.items) + 1))))[1:]
        choices_list.append("m")
        return choices_list

    def get_choices(self):
        self.choice = utils.util.get_choice(self.get_choice_list())
        return self.choice




