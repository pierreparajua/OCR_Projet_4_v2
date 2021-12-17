import utils
from utils.util import Menu


class View_menu:
    def __init__(self, menu, choice):
        self.menu: Menu = menu
        self.choice: str = choice

    def display_menu(self):
        self.menu.display()

    def get_choice_list(self):
        choices_list = list(map(str, list(range(len(self.menu.items) + 1))))[1:]
        choices_list.append("m")
        return choices_list

    def get_choices(self):
        self.choice = utils.util.get_choice(self.get_choice_list())
        return self.choice
