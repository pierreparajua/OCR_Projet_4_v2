
from utils.util import Menu
from controller.c_player import PlayerManager
from controller.c_tournament import TournamentManager


main_menu = Menu(title="Menu principal: ",
                 add_info="(Tapez le chiffre correspondant à votre choix)",
                 items=["Gestion des joueurs",
                        "Gestion des tournois",
                        "Quitter"],
                 choice="")



report_menu = Menu(title="Rapport des tournois: ",
                   add_info="(Tapez le chiffre correspondant à votre choix ou 'm' pour retourner au menu "
                            "précédent: )",
                   items=["Tournois en cours",
                          "Tournois terminés"],
                   choice="")

delete_or_quit_menu = Menu(title="Souhaitez-vous:",
                           add_info="",
                           items=["Supprimer et continuer",
                                  "Supprimer et retourner au menu",
                                  "Annuler"],
                           choice="")

class MainController:
    """Manage the navigation inside the programme."""

    def __init__(self):
        self.menu = Menu("", "", "", "")
        self.choice_save = "1"
        self.player_manager = PlayerManager()
        self.tournament_manager = TournamentManager()

    def main_manager(self):
        """Manage the main menu"""
        while True:
            self.menu = main_menu
            self.menu.display_menu()
            self.menu.choice = self.menu.get_choice()
            if self.menu.choice == "1":
                self.player_manager.player_manager()
            elif self.menu.choice == "2":
                self.tournament_manager.tournament_manager()
            elif self.menu.choice == "3":
                break


    def delete_or_quit(self, item, table):
        self.menu = delete_or_quit_menu
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()
        if self.menu.choice == "1":
            table.delete(item)
            return self.menu.choice
        elif self.menu.choice == "2":
            table.delete(item)
            if table is storage_p:
                self.player_manager()
            else:
                self.tournament_manager()
        elif self.menu.choice == "3":
            self.tournament_manager()

    def continue_tournament(self, tournament):
        status = len(tournament.rondes)
        if status == 0:
            tournament = tournament_controller.round1(tournament)
            self.save_or_quit(tournament, storage_t)
            status += 1
            self.manage_ronde(status, tournament)
        elif status > 0:
            self.manage_ronde(status, tournament)

    def manage_ronde(self, status, tournament):
        while status != tournament.nbr_of_rounds:
            tournament = tournament_controller.ronde(tournament)
            status += 1
            if status == tournament.nbr_of_rounds:
                tournament_controller.winner(tournament)
                storage_t.update(tournament)
            else:
                self.save_or_quit(tournament, storage_t)

