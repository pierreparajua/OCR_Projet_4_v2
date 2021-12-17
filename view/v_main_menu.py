from dataclasses import dataclass

import utils


@dataclass
class get_choices:
    choices: list

    def ask_choice(self):
        choice = input(Fore.LIGHTBLUE_EX + "Choix: ").lower()
