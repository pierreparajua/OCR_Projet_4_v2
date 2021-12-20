from view.view import View_menu
from controller.c_player import Player_controller


main_menu = View_menu(title="Menu principal: ",
                      add_info="(Tapez le chiffre correspondant à votre choix)",
                      items=["Gestion des joueurs",
                             "Gestion des tournois",
                             "Quitter"],
                      choice="")

player_menu = View_menu(title="Menu de gestion des joueurs: ",
                        add_info="(Tapez le chiffre correspondant à votre choix ou 'm' pour retourner au menu "
                                 "précédent: )",
                        items=["Ajouter un joueur",
                               "Afficher les joueurs",
                               "Modifier un joueurs",
                               "Supprimer un joueur"],
                        choice="")

tournament_menu = View_menu(title="Menu de gestion des tournois: ",
                            add_info="(Tapez le chiffre correspondant à votre choix ou 'm' pour retourner au menu "
                                     "précédent: )",
                            items=["Ajouter un tournois",
                                   "Reprendre un tournois",
                                   "Supprimer un tournois",
                                   "Afficher les rapports de tournois"],
                            choice="")

report_menu = View_menu(title="Rapport des tournois: ",
                        add_info="(Tapez le chiffre correspondant à votre choix ou 'm' pour retourner au menu "
                                 "précédent: )",
                        items=["Tournois en cours",
                               "Tournois terminés"],
                        choice="")

player_controller = Player_controller()


class Manage_menu:
    """Manage the navigation inside the programme."""
    def __init__(self, title, add_info, items, choice):
        self.menu = View_menu(title, add_info, items, choice)

    def main_manager(self):
        """Manage the main menu"""
        self.menu = main_menu
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choices()
        if self.menu.choice == "1":
            self.player_manager()
        elif self.menu.choice == "2":
            self.tournament_manager()
        elif self.menu.choice == "3":
            pass

    def player_manager(self):
        """Manage the player menu"""
        self.menu = player_menu
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choices()
        if self.menu.choice == "1":
            player_controller.add_player()
            self.player_manager()
        elif self.menu.choice == "2":
            player_controller.display_all_players()
            self.player_manager()
        elif self.menu.choice == "3":
            player_controller.update_player()
            self.player_manager()
        elif self.menu.choice == "4":
            player_controller.delete_player()
            self.player_manager()
        elif self.menu.choice == "m":
            self.main_manager()

    def tournament_manager(self):
        """Manage the tournament menu"""
        self.menu = tournament_menu
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choices()
        if self.menu.choice == "1":
            print("add tournament")
        elif self.menu.choice == "2":
            print("reprendre tournament")
        elif self.menu.choice == "3":
            print("delete tournament")
        elif self.menu.choice == "4":
            self.report_manager()
        elif self.menu.choice == "m":
            self.main_manager()

    def report_manager(self):
        """Manage the report menu"""
        self.menu = report_menu
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choices()
        if self.menu.choice == "1":
            print("Rapport tournois en cours")
        elif self.menu.choice == "2":
            print("Rapport tournois terminé")
        elif self.menu.choice == "m":
            self.tournament_manager()
