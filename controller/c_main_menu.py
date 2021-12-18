from view.view import View_menu
from controller.c_player import player_controller

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


class Manage_menu:
    def __init__(self, menu, choice):
        self.menu: View_menu = menu
        self.choice: str = choice

    def main_manager(self):
        self.menu = main_menu
        self.menu.display_menu()
        self.choice = self.menu.get_choices()
        if self.choice == "1":
            self.player_manager()
        elif self.choice == "2":
            self.tournament_manager()
        elif self.choice == "3":
            pass

    def player_manager(self):
        self.menu = player_menu
        self.menu.display_menu()
        self.choice = self.menu.get_choices()
        if self.choice == "1":
            player_controller.add_player()
            self.player_manager()
        elif self.choice == "2":
            player_controller.display_all_players()
            self.player_manager()
        elif self.choice == "3":
            player_controller.update_player()
            self.player_manager()
        elif self.choice == "4":
            print("delete player")
        elif self.choice == "m":
            player_controller.delete_player()
            self.player_manager()

    def tournament_manager(self):
        self.menu = tournament_menu
        self.menu.display_menu()
        self.choice = self.menu.get_choices()
        if self.choice == "1":
            print("add tournament")
        elif self.choice == "2":
            print("reprendre tournament")
        elif self.choice == "3":
            print("delete tournament")
        elif self.choice == "4":
            self.report_manager()
        elif self.choice == "m":
            self.main_manager()

    def report_manager(self):
        self.menu = report_menu
        self.menu.display_menu()
        self.choice = self.menu.get_choices()
        if self.choice == "1":
            print("Rapport tournois en cours")
        elif self.choice == "2":
            print("Rapport tournois terminé")
        elif self.choice == "m":
            self.tournament_manager()


manage_menu = Manage_menu(main_menu, "")
