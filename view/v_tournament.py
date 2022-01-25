from colorama import Fore

import utils
from model.m_tournament import Tournament
from utils.util import Menu
from view.view import View

time_control_menu = Menu(title="Choisissez le système de contrôle du temps",
                         add_info="",
                         items=["Bullet", "Blitz", "Coup rapide"],
                         choice="")


class ViewTournament(Tournament, View):
    """Manage the views for the tournaments"""
    def __init__(self):
        super().__init__()

    def get_name(self) -> str:
        """Get the name from the user"""
        self.name = input("Entrez le nom du tournoi: ")
        while not self.name:
            self.name = input(Fore.LIGHTYELLOW_EX + "Vous devez saisir un nom de tournois: ")
        return self.name

    def get_place(self) -> str:
        """Get the place from the user"""
        self.place = input("Entrez le lieu du tournoi: ")
        while not self.place:
            self.place = input(Fore.LIGHTYELLOW_EX + "Vous devez saisir un lieu de tournois: ")
        return self.place

    def get_date(self) -> str:
        """Get the date from the user"""
        self.date = input(f"Date du tournoi: \n"
                          f"    Tapez sur 'Entrée' pour conserver la date du jour: {utils.util.get_date_now()[0:10]}\n"
                          f"    Ou saisir la date souhaitée:")
        if not self.date:
            self.date = str(utils.util.get_date_now()[0:10])
        return self.date

    def get_nbr_of_rounds(self):
        """Get the number of rounds from the user"""
        self.nbr_of_rounds = input("Entrez le nombre de ronde: \n   Tapez sur 'Entrée' pour 4 rondes"
                                   "\n   ou entrez le nombre de ronde souhaitée: ")
        return self.nbr_of_rounds

    def get_time(self) -> str:
        """Get the time control method from the user"""
        time_control_menu.display_menu()
        choice = time_control_menu.get_choice()
        if choice == "1":
            self.time = "Bullet"
        elif choice == "2":
            self.time = "Blitz"
        elif choice == "3":
            self.time = "Coup rapide"
        return self.time

    def get_description(self) -> str:
        """Get description from the user"""
        self.description = input("Remarques du président de tournoi: ")
        return self.description

    def create_tournament(self) -> Tournament:
        """
        Create an instance of tournament from user's informations
        Returns:
            tournament: An instance of Tournament
        """
        tournament = Tournament(self.get_name(),
                                self.get_place(),
                                self.get_date(),
                                [],
                                [],
                                self.get_time(),
                                self.get_description(),
                                1,
                                self.get_nbr_of_rounds())
        return tournament

    def display_score(self):
        """Display the score for each player at the end of a round"""
        nbr_ronde = len(self.item.rondes)
        print(Fore.LIGHTGREEN_EX + f"Classement à l' issue de la ronde N° {nbr_ronde}: ")
        for chess_player in self.item.chess_players:
            print(f"{self.item.chess_players.index(chess_player) + 1}:"
                  f" {chess_player.player_from_chess_player().full_name(): <15}"
                  f" {chess_player.score_tot: >5} pts")
        print("\n")

    def display_matches(self, matches):
        """ Display the matches for the next round"""
        if matches:
            for match, i in zip(matches, range(len(matches))):
                chess_player1 = next(chess for chess in self.item.chess_players if chess.id_player == match[0])
                chess_player2 = next(chess for chess in self.item.chess_players if chess.id_player == match[1])
                print(f"Match n°{i + 1}:\n"
                      f"    {chess_player1.full_name} contre {chess_player2.full_name}\n")

    def display_ronde(self):
        """Display all matches inside each rounds for report"""
        for ronde in self.item.rondes:
            print(Fore.LIGHTGREEN_EX + f"\nRONDE N° {ronde.number}  début: {ronde.date_start}  fin: {ronde.date_end} ")
            for match in ronde.matches:
                chess_player1 = next(chess for chess in self.item.chess_players if chess.id_player == match[0][0])
                chess_player2 = next(chess for chess in self.item.chess_players if chess.id_player == match[1][0])
                x = ""
                print(f"{chess_player1.full_name: <14}: {match[0][1]: >5} pt    contre   "
                      f"{chess_player2.full_name: >15}: {match[1][1]: >5}pt {x: <15}")
        print("\n")

    def display_tournaments(self):
        """Display all tournaments."""
        for i, tournament in enumerate(self.item):
            print(f"{i + 1}:  Tournoi: {tournament.name} - le {tournament.date}")

    @staticmethod
    def get_scores(chess_players: list, matches: list) -> tuple:
        """
        Ask for the winner, return corresponding score and add the opponent
        Args:
            chess_players: List of ChessPlayers
            matches: List of matches
        Returns:
            chess_players and matches with the score and the opponents added
        """
        for match, i in zip(matches, range(len(matches))):
            chess_player1 = next(chess for chess in chess_players if chess.id_player == match[0])
            chess_player2 = next(chess for chess in chess_players if chess.id_player == match[1])

            chess_player1.opponents.append(chess_player2.id_player)
            chess_player2.opponents.append(chess_player1.id_player)

            print(Fore.LIGHTBLUE_EX + f"\nMatch n°{i + 1}: "
                  + Fore.RESET + f"    {chess_player1.full_name} - {chess_player1.ranking}"
                  f"   contre   {chess_player2.full_name} - {chess_player2.ranking}")
            print("Qui est le gagnant du match: \n"
                  f"1: pour {chess_player1.full_name}\n"
                  f"2: pour {chess_player2.full_name}\n"
                  f"3: pour égalité")
            choice = utils.util.get_choice(['1', '2', '3'])
            if choice == '1':
                print(f"{chess_player1.full_name} :" + Fore.LIGHTGREEN_EX + " 1 point")
                print(f"{chess_player2.full_name} :" + Fore.LIGHTRED_EX + " 0 point\n")
                match[0] = (match[0], 1)
                match[1] = (match[1], 0)
                chess_player1.score_tot = chess_player1.score_tot + 1

            elif choice == '2':
                print(f"{chess_player1.full_name} :" + Fore.LIGHTRED_EX + " 0 point")
                print(f"{chess_player2.full_name} :" + Fore.LIGHTGREEN_EX + " 1 point\n")
                match[0] = (match[0], 0)
                match[1] = (match[1], 1)
                chess_player2.score_tot = chess_player2.score_tot + 1

            elif choice == '3':
                print(f"{chess_player1.full_name} :" + Fore.LIGHTBLUE_EX + " 0.5 point")
                print(f"{chess_player2.full_name} :" + Fore.LIGHTBLUE_EX + " 0.5 point\n")
                match[0] = (match[0], 0.5)
                match[1] = (match[1], 0.5)
                chess_player1.score_tot = chess_player1.score_tot + 0.5
                chess_player2.score_tot = chess_player2.score_tot + 0.5
        return chess_players, matches
