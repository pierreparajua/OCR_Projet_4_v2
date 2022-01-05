
from colorama import Fore, init

import datetime
import re
import utils

init(autoreset=True)


class Menu:
    """Create a menu"""
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

    def get_choices(self):
        """Gets et returns the user's choice"""
        self.choice = utils.util.get_choice(self.get_choice_list())
        return self.choice


def check_name(name):
    """Check the format of name"""
    if name:
        x = re.findall("[0-9]", name)
        while x:
            name = wrong_entry(name)
            x = re.findall("[0-9]", name)
    return name


def check_date(date):
    """Check the format of date"""
    if date:
        x = re.findall("^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.]((19|20)\\d\\d)$", date)
        while not x:
            date = wrong_entry(date)
            x = re.findall("^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.]((19|20)\\d\\d)$", date)
    return date.replace("-", "/").replace(".", "/").replace(" ", "/")


def check_ranking(ranking):
    """Check the format of ranking"""
    if ranking:
        ranking = str(ranking)
        x = re.findall("[0-9]", ranking)
        while not x:
            ranking = wrong_entry(ranking)
            x = re.findall("[0-9]", ranking)
    return int(ranking)


def check_sex(sex):
    """Check the format of sex"""
    if sex:
        while sex not in ["h", "f", "H", "F", "homme", "femme"]:
            sex = utils.util.wrong_entry(sex)
        if sex in ["f", "F"]:
            return "femme"
        elif sex in ["h", "H"]:
            return "homme"
    return sex


def get_choice(choices: list) -> str:
    """Gets a choice and check it and return it"""
    choice = input(Fore.LIGHTBLUE_EX + "Choix: ").lower()
    while choice not in choices:
        choice = wrong_entry(choice)
    return choice


def get_date_now():
    """ Gets the date and hour and return """
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    return date


def wrong_entry(choice: str):
    """ Display error message"""
    value = input(Fore.LIGHTGREEN_EX + f"{choice}"
                  + Fore.LIGHTRED_EX + " : n' est pas un choix valide.\n Veuillez ressaisir votre choix: \n")
    return value

if __name__ == "__main__":
    print(check_ranking("1"))
    print(type(check_ranking(1)))