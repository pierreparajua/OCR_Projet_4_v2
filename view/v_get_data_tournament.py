from colorama import Fore

import utils
from model.m_tournament import Tournament
from utils.util import Menu

time_control_menu = Menu(title="Choisissez le système de contrôle du temps",
                         add_info="",
                         items=["Bullet", "Blitz", "Coup rapide"],
                         choice="")


class GetDataTournament(Tournament):
    """Gets tournament's informations from the user"""

    def get_name(self):
        """Gets the name from the user"""
        self.name = input("Entrez le nom du tournoi: ")
        while not self.name:
            self.name = input(Fore.LIGHTYELLOW_EX + "Vous devez saisir un nom de tournois: ")
        return self.name

    def get_place(self):
        """Gets the place from the user"""
        self.place = input("Entrez le lieu du tournoi: ")
        while not self.place:
            self.place = input(Fore.LIGHTYELLOW_EX + "Vous devez saisir un lieu de tournois: ")
        return self.place

    def get_date(self):
        """Gets the date from the user"""
        self.date = input(f"Date du tournois: {utils.util.get_date_now()[0:10]}\n"
                          f"Tapez la date si différente ou 'Entrez'(JJ/MM:AAAA): ")
        if not self.date:
            self.date = str(utils.util.get_date_now()[0:10])
        return self.date

    def get_nbr_of_rounds(self):
        """Gets the number of rounds from the user"""
        self.nbr_of_rounds = input("Tapez sur 'Entrez' pour 4 rondes\nou entrez le nombre de ronde souhaiter: ")
        return self.nbr_of_rounds

    def get_time(self):
        """Gets the time control method from the user"""
        time_control_menu.display_menu()
        choice = time_control_menu.get_choice()
        if choice == "1":
            self.time = "Bullet"
        elif choice == "2":
            self.time = "Blitz"
        elif choice == "3":
            self.time = "Coup rapide"
        return self.time

    def get_description(self):
        """Gets description from the user"""
        self.description = input("Remarques du président de tournois: ")
        return self.description

    def create_tournament(self):
        """Creates an instance of tournament from user's informations"""
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

    @staticmethod
    def get_scores(chess_players, matches):
        for match, i in zip(matches, range(len(matches))):
            chess_player1 = next(chess for chess in chess_players if chess.id_player == match[0])
            chess_player2 = next(chess for chess in chess_players if chess.id_player == match[1])
            chess_player1.opponents.append(chess_player2.id_player)
            chess_player2.opponents.append(chess_player1.id_player)

            player1 = chess_player1.player_from_chess_player()
            player2 = chess_player2.player_from_chess_player()
            print(Fore.LIGHTBLUE_EX + f"\nMatch n°{i + 1}: " + Fore.RESET +
                  f"    {player1.full_name()} - {player1.ranking}"
                  f"   contre   {player2.full_name()} - {player2.ranking}")
            print("Qui est le gagnant du match: \n"
                  f"1: pour {player1.full_name()}\n"
                  f"2: pour {player2.full_name()}\n"
                  f"3: pour égalité")
            choice = utils.util.get_choice(['1', '2', '3'])
            chess_player1.score = 0
            chess_player2.score = 0
            if choice == '1':
                print(f"{player1.full_name()} :" + Fore.LIGHTGREEN_EX + " 1 point")
                print(f"{player2.full_name()} :" + Fore.LIGHTRED_EX + " 0 point\n")
                x = chess_player1.score = 1
                match[0] = (match[0], x)
                match[1] = (match[1], 0)
                chess_player1.score_tot = chess_player1.score_tot + chess_player1.score
                chess_player2.score_tot = chess_player2.score_tot + chess_player2.score

            elif choice == '2':
                print(f"{player1.full_name()} :" + Fore.LIGHTRED_EX + " 0 point")
                print(f"{player2.full_name()} :" + Fore.LIGHTGREEN_EX + " 1 point\n")
                y = chess_player2.score = 1
                match[0] = (match[0], 0)
                match[1] = (match[1], y)
                chess_player1.score_tot = chess_player1.score_tot + chess_player1.score
                chess_player2.score_tot = chess_player2.score_tot + chess_player2.score

            elif choice == '3':
                print(f"{player1.full_name()} :" + Fore.LIGHTBLUE_EX + " 0.5 point")
                print(f"{player2.full_name()} :" + Fore.LIGHTBLUE_EX + " 0.5 point\n")
                x = chess_player1.score = 0.5
                match[0] = (match[0], x)
                y = chess_player2.score = 0.5
                match[1] = (match[1], y)

                chess_player1.score_tot = chess_player1.score_tot + chess_player1.score
                chess_player2.score_tot = chess_player2.score_tot + chess_player2.score
        return chess_players, matches


if __name__ == "__main__":
    test = GetDataTournament("", "", "", [], [], "", "")
    print(test.create_tournament())
