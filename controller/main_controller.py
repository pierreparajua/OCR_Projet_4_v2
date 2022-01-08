import utils
from controller.c_tournament import TournamentController
from model.m_storage import Tinydb, db_tournaments
from utils.util import Menu
from controller.c_player import PlayerController
from view.view import View, DICT_TEXT

main_menu = Menu(title="Menu principal: ",
                 add_info="(Tapez le chiffre correspondant à votre choix)",
                 items=["Gestion des joueurs",
                        "Gestion des tournois",
                        "Quitter"],
                 choice="")

player_menu = Menu(title="Menu de gestion des joueurs: ",
                   add_info="(Tapez le chiffre correspondant à votre choix ou 'm' pour retourner au menu "
                            "précédent: )",
                   items=["Ajouter un joueur",
                          "Afficher les joueurs",
                          "Modifier un joueurs",
                          "Supprimer un joueur"],
                   choice="")

tournament_menu = Menu(title="Menu de gestion des tournois: ",
                       add_info="(Tapez le chiffre correspondant à votre choix ou 'm' pour retourner au menu "
                                "précédent: )",
                       items=["Ajouter un tournois",
                              "Reprendre un tournois",
                              "Supprimer un tournois",
                              "Afficher les rapports de tournois"],
                       choice="")

report_menu = Menu(title="Rapport des tournois: ",
                   add_info="(Tapez le chiffre correspondant à votre choix ou 'm' pour retourner au menu "
                            "précédent: )",
                   items=["Tournois en cours",
                          "Tournois terminés"],
                   choice="")

player_controller = PlayerController()
tournament_controller = TournamentController()
storage_t = Tinydb(db_tournaments)
view = View(DICT_TEXT)


class ManageMenu:
    """Manage the navigation inside the programme."""

    def __init__(self, title, add_info, items, choice):
        self.menu = Menu(title, add_info, items, choice)

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
        self.menu = tournament_menu
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choices()
        if self.menu.choice == "1":
            tournament = tournament_controller.prepare_tournament()
            self.save_or_quit(tournament, update=False)
            tournament = tournament_controller.round1(tournament)
            self.save_or_quit(tournament)

        elif self.menu.choice == "2":
            print("reprendre tournament")
        elif self.menu.choice == "3":
            print("delete tournament")
        elif self.menu.choice == "4":
            self.report_manager()
        elif self.menu.choice == "m":
            self.main_manager()

    def report_manager(self):
        self.menu = report_menu
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choices()
        if self.menu.choice == "1":
            print("Rapport tournois en cours")
        elif self.menu.choice == "2":
            print("Rapport tournois terminé")
        elif self.menu.choice == "m":
            self.tournament_manager()

    def save_or_quit(self, tournament, update=True):
        view.display_text("save_or_quit")
        choice = utils.util.get_choice(["1", "2"])
        if choice == "1":
            if not update:
                tournament.id_db = storage_t.save(tournament)
            storage_t.update(tournament)
        elif choice == "2":
            if not update:
                tournament.id_db = storage_t.save(tournament)
            storage_t.update(tournament)
            self.tournament_manager()


if __name__ == "__main__":
    """
    test = TournamentController()

    caroline = Player("caroline", "sejil", "12/02/1984", "femme", 1, 1230)
    damien = Player("damien", "parajua", "08/05/1984", "femme", 2, 1130)
    pierre = Player("pierre", "yves", "08/02/1989", "homme", 3, 1250)
    eddy = Player("eddy", "sejil", "08/02/1984", "homme", 4, 1098)
    players = [caroline, damien, pierre, eddy]

    tournament = Tournament("master", "lyon", "05/02/2002", [], players, "Blitz", "test", 1, 4)
    test.view.display_instance(tournament)
    storage_t.item = tournament
    tournament = Tournament.deserialize(storage_t.load())
    tournament = test.round1(tournament)
    storage_t.item = tournament
    storage_t.update()
    """
