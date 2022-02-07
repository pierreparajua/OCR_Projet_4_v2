from colorama import Fore, init

import datetime
import re

init(autoreset=True)


class Menu:
    """Display menu's items and get the user choice and re return it"""

    def __init__(self, title, add_info, items, choice):
        self.title: str = title
        self.add_info: str = add_info
        self.items: list = items
        self.choice: str = choice

    def display_menu(self):
        """Display the menu's items"""
        print(Fore.LIGHTMAGENTA_EX + f"\n{self.title}:" + Fore.LIGHTWHITE_EX + f" {self.add_info}")
        for i, item in enumerate(self.items):
            print(f"{i + 1}: {item} ")

    def get_choice_list(self):
        """Create a list with all the choices"""
        choices_list = list(map(str, list(range(len(self.items) + 1))))[1:]
        choices_list.append("m")
        return choices_list

    def get_choice(self):
        """Get and return the user's choice"""
        self.choice = input(Fore.LIGHTBLUE_EX + "Choix: ").lower()
        while self.choice not in self.get_choice_list():
            self.choice = Validator.wrong_entry(self.choice)
        return self.choice


class Validator:
    """Check if the data from the user are correct"""
    def __init__(self, item: str = None):
        self.item = item

    def check_name(self, text):
        """Check the format of name"""
        while not self.item:
            self.item = input(Fore.LIGHTYELLOW_EX + text)
        x = re.findall("[0-9]", self.item)
        while x:
            self.item = self.wrong_entry(self.item)
            x = re.findall("[0-9]", self.item)
        return self.item

    def check_date(self, text):
        """Check the format of date"""
        while not self.item:
            self.item = input(Fore.LIGHTYELLOW_EX + text)
        if "au" in self.item:
            return self.item
        x = re.findall("^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.]((19|20)\\d\\d)$", self.item)
        while not x:
            self.item = self.wrong_entry(self.item)
            x = re.findall("^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.]((19|20)\\d\\d)$", self.item)
        return self.item.replace("-", "/").replace(".", "/").replace(" ", "/")

    def check_number(self, text):
        """Check the format of number"""
        while not self.item:
            self.item = input(Fore.LIGHTYELLOW_EX + text)
        x = re.findall("[0-9]", self.item)
        while not x:
            self.item = self.wrong_entry(self.item)
            x = re.findall("[0-9]", self.item)
        return self.item

    def check_sex(self, text):
        """Check the format of sex"""
        while not self.item:
            self.item = input(Fore.LIGHTYELLOW_EX + text)
        while self.item not in ["h", "f", "H", "F", "homme", "femme"]:
            self.item = self.wrong_entry(self.item)
        if self.item in ["f", "F"]:
            self.item = "femme"
        elif self.item in ["h", "H"]:
            self.item = "homme"
        return self.item

    def get_choice(self, choices: list) -> str:
        """Return a choice from a list of choices"""
        choice = input(Fore.LIGHTBLUE_EX + "Choix: ").lower()
        while choice not in choices:
            choice = self.wrong_entry(choice)
        return choice

    @staticmethod
    def get_date_now():
        """Get the live date and hour"""
        return datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    @staticmethod
    def wrong_entry(choice: str):
        """ Display error message"""
        value = input(Fore.LIGHTGREEN_EX + f"{choice}"
                      + Fore.LIGHTRED_EX + " : n' est pas un choix valide.\n Veuillez ressaisir votre choix: \n")
        return value
