from utils.util import Menu
from controller.c_player import PlayerController
from controller.c_tournament import TournamentManager

main_menu = Menu(title="Menu principal: ",
                 add_info="(Tapez le chiffre correspondant à votre choix)",
                 items=["Gestion des joueurs",
                        "Gestion des tournois",
                        "Quitter"],
                 choice="")


class MainController:
    """Manage the navigation inside the programme."""
    def __init__(self):
        self.menu = Menu("", "", "", "")
        self.choice_save = "1"
        self.player_manager = PlayerController()
        self.tournament_manager = TournamentManager()

    def main_manager(self):
        """Manage the main menu"""
        while True:
            self.menu = main_menu
            self.menu.display_menu()
            self.menu.choice = self.menu.get_choice()
            if self.menu.choice == "1":
                self.player_manager.manage_menu()
            elif self.menu.choice == "2":
                self.tournament_manager.manage_menu()
            elif self.menu.choice == "3":
                break
