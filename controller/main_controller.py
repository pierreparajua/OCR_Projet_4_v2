from utils.util import Menu
from controller.c_player import PlayerController
from controller.c_tournament import TournamentManager


class MainController:
    """Manage the navigation inside the programme."""

    def __init__(self):
        self.menu = self._create_menu()
        self.choice_save = "1"
        self.player_manager = PlayerController()
        self.tournament_manager = TournamentManager()

    def main_manager(self):
        """Manage the main menu"""
        while True:
            self.menu.display_menu()
            self.menu.choice = self.menu.get_choice()
            if self.menu.choice == "1":
                self.player_manager.manage_menu()
            elif self.menu.choice == "2":
                self.tournament_manager.manage_menu()
            elif self.menu.choice == "3":
                break

    def _create_menu(self):
        """
        Helper method to create a menu.
        Args:
            menu: Name of the menu, you want to create"
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
