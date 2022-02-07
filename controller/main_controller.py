from utils.util import Menu
from controller.c_player import PlayerController
from controller.c_tournament import TournamentController


class MainController:
    """Manage the navigation inside the programme."""
    def __init__(self):
        self.menu = self._create_menu()
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()

    def main_manager(self):
        """Manage the main menu"""
        while True:
            self.menu.display_menu()
            self.menu.choice = self.menu.get_choice()
            if self.menu.choice == "1":
                self.player_controller.control_menu()
            elif self.menu.choice == "2":
                self.tournament_controller.control_menu()
            elif self.menu.choice == "3":
                break

    @staticmethod
    def _create_menu():
        """
        Helper method to create a menu.
        Returns:
            An instance of Menu
        """
        main_menu = Menu(title="Menu principal: ",
                         add_info="(Tapez le chiffre correspondant à votre choix)",
                         items=["Gestion des joueurs",
                                "Gestion des tournois",
                                "Quitter"],
                         choice="")
        return main_menu
