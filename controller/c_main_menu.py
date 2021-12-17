from view.view import View_menu
from utils.util import Menu

main_menu = View_menu(Menu(title="Menu principal: ",
                           add_info="(Tapez le chiffre correspondant à votre choix)",
                           items=["Gestion des joueurs",
                                  "Gestion des tournois",
                                  "Quitter"]), "")

player_menu = View_menu(Menu(title="Menu de gestion des joueurs: ",
                             add_info="(Tapez le chiffre correspondant à votre choix ou 'm' pour retourner au menu "
                                      "précédent: )",
                             items=["Ajouter un joueur",
                                    "Afficher les joueurs",
                                    "Modifier un joueurs",
                                    "Supprimer un joueur"]), "")

tournament_menu = View_menu(Menu(title="Menu de gestion des tournois: ",
                                 add_info="(Tapez le chiffre correspondant à votre choix ou 'm' pour retourner au menu "
                                          "précédent: )",
                                 items=["Ajouter un tournois",
                                        "Reprendre un tournois",
                                        "Supprimer un tournois",
                                        "Afficher les rapports de tournois"]), "")

report_menu = View_menu(Menu(title="Rapport des tournois: ",
                             add_info="(Tapez le chiffre correspondant à votre choix ou 'm' pour retourner au menu "
                                      "précédent: )",
                             items=["Tournois en cours",
                                    "Tournois terminés"]), "")


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
            print("add player")
        elif self.choice == "2":
            print("display player")
        elif self.choice == "3":
            print("update player")
        elif self.choice == "4":
            print("delete player")
        elif self.choice == "m":
            self.main_manager()

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
