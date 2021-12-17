import dataclasses

import utils.util
from utils.util import Menu


class Manage_menu:
    def __init__(self, main_menu, choice):
        self.main_menu: Menu = main_menu
        self.choice: str = choice

    def display_menu(self):
        self.main_menu.display()

    def get_choice_list(self):
        choices_list = map(str, list(range(len(self.main_menu.items))))
        return choices_list

    def get_choices(self):
        self.choice = utils.util.get_choice(self.get_choice_list())


main_menu = Menu(title="Menu principal: ",
                 add_info="(Tapez le chiffre correspondant à votre choix)",
                 items=["Gestion des joueurs",
                        "Gestion des tournois",
                        "Quitter"])

main_menu.display()
manage_menu = Manage_menu(main_menu, "")
print(manage_menu.get_choice_list())
manage_menu.get_choices()