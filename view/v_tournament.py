from colorama import Fore

from model.m_tournament import Tournament
from model.m_player import Player
from utils.util import Menu, Validator
from view.view import View


class ViewTournament(View):
    """Manage the views for the tournaments"""
    validator = Validator()
    time_control_menu = Menu(title="Choisissez le système de contrôle du temps",
                             add_info="",
                             items=["Bullet", "Blitz", "Coup rapide"],
                             choice="")

    def __init__(self):
        super().__init__()

    def get_name(self) -> str:
        """Get the name from the user"""
        self.validator.item = input("Entrez le nom du tournoi: ")
        return self.validator.check_name("Vous devez saisir un nom de tournois")

    def get_place(self) -> str:
        """Get the place from the user"""
        self.validator.item = input("Entrez le lieu du tournoi: ")
        return self.validator.check_name("Vous devez saisir un lieu de tournois")

    def get_date(self) -> str:
        """Get the date from the user"""
        self.validator.item = input("Entrez le date de début du tournois ou 'Entrée' pour la date du jour: ")
        if self.validator.item:
            return self.validator.check_date("Vous devez saisir une date: ")
        return Validator.get_date_now()

    def get_nbr_of_rounds(self):
        """Get the number of rounds from the user"""
        self.validator.item = input("Entrez le nombre de ronde: \n   Tapez sur 'Entrée' pour 4 rondes"
                                    "\n   ou entrez le nombre de ronde souhaitée: ")
        if self.validator.item:
            return int(self.validator.check_number("Vous devez saisir un nombre:"))
        return 4

    def get_time(self) -> str:
        """Get the time control method from the user"""
        self.time_control_menu.display_menu()
        self.time_control_menu.choice = self.time_control_menu.get_choice()
        if self.time_control_menu.choice == "1":
            return "Bullet"
        elif self.time_control_menu.choice == "2":
            return "Blitz"
        elif self.time_control_menu.choice == "3":
            return "Coup rapide"

    def create_tournament(self) -> Tournament:
        """
        Create an instance of tournament from user's informations
        Returns:
            tournament: An instance of Tournament
        """
        tournament = Tournament(name=self.get_name(),
                                place=self.get_place(),
                                date=self.get_date(),
                                rondes=[],
                                players=[],
                                time=self.get_time(),
                                nbr_of_rounds=self.get_nbr_of_rounds(),
                                description=input("Remarques du président de tournoi: "))
        return tournament

    def display_score(self):
        """Display the score for each player at the end of a round"""
        nbr_ronde = len(self.item.rondes)
        print(Fore.LIGHTGREEN_EX + f"Classement à l' issue de la ronde N° {nbr_ronde}: ")
        for player in self.item.players:
            print(f"{self.item.players.index(player) + 1}:"
                  f" {player.full_name(): <15}"
                  f" {player.score: >5} pts")
        print("\n")

    def display_matches(self):
        """ Display the matches for the next round"""
        if self.item:
            for match, i in zip(self.item, range(len(self.item))):
                print(f"Match n°{i + 1}:\n"
                      f"    {Player.player_from_id(match[0]).full_name()} contre "
                      f"{Player.player_from_id(match[1]).full_name()}\n")

    def display_ronde(self):
        """Display all matches inside each round for report"""
        for ronde in self.item.rondes:
            print(Fore.LIGHTGREEN_EX + f"\nRONDE N° {ronde.number}  début: {ronde.date_start}  fin: {ronde.date_end} ")
            for match in ronde.matches:
                player1 = next(player for player in self.item.players if player.id_db == match[0][0])
                player2 = next(player for player in self.item.players if player.id_db == match[1][0])
                x = ""
                print(f"{player1.full_name(): <14}: {match[0][1]: >5} pt    contre   "
                      f"{player2.full_name(): >15}: {match[1][1]: >5}pt {x: <15}")
        print("\n")

    def display_tournaments(self):
        """Display all tournaments."""
        for i, tournament in enumerate(self.item):
            print(f"{i + 1}:  Tournoi: {tournament.name} - le {tournament.date}")

    @staticmethod
    def get_scores(matches: list) -> list:
        """
        Ask for the winner and add corresponding score
        Args:
            matches: List of matches
        Returns:
            matches: List of matches with score added
        """
        validator = Validator()
        for match, i in zip(matches, range(len(matches))):
            player1 = Player.player_from_id(match[0])
            player2 = Player.player_from_id(match[1])

            print(Fore.LIGHTBLUE_EX + f"\nMatch n°{i + 1}: "
                  + Fore.RESET + f"    {player1.full_name()} - {player1.ranking}"
                                 f"   contre   {player2.full_name()} - {player2.ranking}")
            print("Qui est le gagnant du match: \n"
                  f"1: pour {player1.full_name()}\n"
                  f"2: pour {player2.full_name()}\n"
                  f"3: pour égalité")
            choice = validator.get_choice(['1', '2', '3'])
            if choice == '1':
                print(f"{player1.full_name()} :" + Fore.LIGHTGREEN_EX + " 1 point")
                print(f"{player2.full_name()} :" + Fore.LIGHTRED_EX + " 0 point\n")
                match[0] = (match[0], 1)
                match[1] = (match[1], 0)

            elif choice == '2':
                print(f"{player1.full_name()} :" + Fore.LIGHTRED_EX + " 0 point")
                print(f"{player2.full_name()} :" + Fore.LIGHTGREEN_EX + " 1 point\n")
                match[0] = (match[0], 0)
                match[1] = (match[1], 1)

            elif choice == '3':
                print(f"{player1.full_name()} :" + Fore.LIGHTBLUE_EX + " 0.5 point")
                print(f"{player2.full_name()} :" + Fore.LIGHTBLUE_EX + " 0.5 point\n")
                match[0] = (match[0], 0.5)
                match[1] = (match[1], 0.5)
        return matches
