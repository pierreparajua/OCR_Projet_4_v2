from colorama import Fore, init

init(autoreset=True)


class Menu:
    def __init__(self, title, add_info, items):
        self.title: str = title
        self.add_info: str = add_info
        self.items: list = items

    def display(self):
        print(Fore.LIGHTMAGENTA_EX + f"\n{self.title}:" + Fore.LIGHTWHITE_EX + f" {self.add_info}")
        for i, item in enumerate(self.items):
            print(f"{i + 1}: {item} ")


def get_choice(choices: list) -> str:
    """
        Get a choice and check it and return it.
        Args:
            choices(list): possible choices for the user

        Returns:
            choice(str): user's choice
        """
    choice = input(Fore.LIGHTBLUE_EX + "Choix: ").lower()
    while choice not in choices:
        wrong_entry(choice)
        choice = input(Fore.LIGHTBLUE_EX + "Choix: ").lower()

    return choice


def wrong_entry(choice: str):
    """ Display error message"""
    print(Fore.LIGHTRED_EX + f"{choice} : n' est pas un choix valide.\n"
                             f"Veuillez ressaisir votre choix: \n")
