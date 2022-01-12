from controller.c_tournament import TournamentController, chess_player
from model.m_player import Player
from model.m_storage import Tinydb, db_tournaments, db_players
from model.m_tournament import ChessPlayer, Tournament
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
save_or_quit_menu = Menu(title="Souhaitez-vous:",
                         add_info="",
                         items=["Sauvegarder et continuer",
                                "Sauvegarder et retourner au menu",
                                "Annuler"],
                         choice="")
delete_or_quit_menu = Menu(title="Souhaitez-vous:",
                           add_info="",
                           items=["Supprimer et continuer",
                                  "Supprimer et retourner au menu",
                                  "Annuler"],
                           choice="")

player_controller = PlayerController()
tournament_controller = TournamentController()
storage_t = Tinydb(db_tournaments)
storage_p = Tinydb(db_players)
view = View(DICT_TEXT)


class MainController:
    """Manage the navigation inside the programme."""

    def __init__(self):
        self.menu = Menu("", "", "", "")
        self.choice_save = "1"

    def main_manager(self):
        """Manage the main menu"""
        self.menu = main_menu
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()
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
        self.menu.choice = self.menu.get_choice()
        if self.menu.choice == "1":
            while self.choice_save == "1":
                player = player_controller.add_player()
                self.choice_save = self.save_or_quit(player, storage_p, update=False)
            self.player_manager()
        elif self.menu.choice == "2":
            dict_players = storage_p.load_all()
            player_controller.display_all_players(dict_players)
            self.player_manager()
        elif self.menu.choice == "3":
            while self.choice_save == "1":
                dict_players = storage_p.load_all()
                player = player_controller.update_player(dict_players)
                self.choice_save = self.save_or_quit(player, storage_p)
            self.player_manager()
        elif self.menu.choice == "4":
            while self.choice_save == "1":
                dict_players = storage_p.load_all()
                player = player_controller.delete_player(dict_players)
                self.choice_save = self.delete_or_quit(player, storage_p)
            self.player_manager()
        elif self.menu.choice == "m":
            self.main_manager()

    def tournament_manager(self):
        self.menu = tournament_menu
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()
        if self.menu.choice == "1":
            tournament = tournament_controller.prepare_tournament()
            self.save_or_quit(tournament, storage_t, update=False)
            self.continue_tournament(tournament)
            print(f"Le gagnant est {tournament.chess_players[0]}")

        elif self.menu.choice == "2":
            tournament = tournament_controller.select_tournament(storage_t.load_all())
            self.continue_tournament(tournament)
            print(f"Le gagnant est {tournament.chess_players[0]}")

        elif self.menu.choice == "3":
            tournaments = storage_t.load_all()
            tournament = tournament_controller.delete_tournament(tournaments)
            if tournament:
                self.delete_or_quit(tournament, storage_t)
            self.tournament_manager()

        elif self.menu.choice == "4":
            self.report_manager()

        elif self.menu.choice == "m":
            self.main_manager()

    def report_manager(self):
        self.menu = report_menu
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()
        if self.menu.choice == "1":
            print("Rapport tournois en cours")
        elif self.menu.choice == "2":
            print("Rapport tournois terminé")
        elif self.menu.choice == "m":
            self.tournament_manager()

    def save_or_quit(self, item, table, update=True):
        self.menu = save_or_quit_menu
        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()
        if self.menu.choice == "1":
            if not update:
                item.id_db = table.save(item)
            table.update(item)
            return self.menu.choice
        elif self.menu.choice == "2":
            if not update:
                item.id_db = table.save(item)
            table.update(item)
            if table is storage_p:
                self.player_manager()
            else:
                self.tournament_manager()
        elif self.menu.choice == "3":
            self.main_manager()

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
            self.main_manager()

    def continue_tournament(self, tournament):
        status = len(tournament.rondes) + 1
        if status == 1:
            tournament = tournament_controller.round1(tournament)
            self.save_or_quit(tournament, storage_t)
            while status != tournament.nbr_of_rounds:
                tournament = tournament_controller.ronde(tournament)
                self.save_or_quit(tournament, storage_t)
                status += 1
        elif status > 1:
            while status != tournament.nbr_of_rounds:
                tournament = tournament_controller.ronde(tournament)
                self.save_or_quit(tournament, storage_t)
                status += 1





if __name__ == "__main__":
    main = MainController()
    main.tournament_manager()
    """
    test = TournamentController()
    tournament = Tournament.deserialize(storage_t.load(1))
    print(tournament)
    tournament = test.round1(tournament)
    print(tournament)
    print(tournament.rondes)
    print(tournament.chess_players)
    test.ronde(tournament)
    """



