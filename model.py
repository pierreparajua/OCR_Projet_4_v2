from colorama import Fore, init

init(autoreset=True)


class Menu:
    def __init__(self, title, add_info, items):
        self.title: str = title
        self.add_info: str = add_info
        self.items: list = items

    def display_menu(self):
        """Display the menu"""
        print(Fore.LIGHTMAGENTA_EX + f"\n{self.title}:" + Fore.LIGHTWHITE_EX + f" {self.add_info}")
        for i, item in enumerate(self.items):
            print(f"{[i +1]}: {item} ")