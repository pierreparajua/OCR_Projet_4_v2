from colorama import Fore

from view.view import View, DICT_TEXT
from model.m_player import Player, Player_tiny_db
import utils

storage = Player_tiny_db()


class Player_controller:
    """Controls the players."""

    def __init__(self, ):
        self.view: View = View(DICT_TEXT)

    def add_player(self):
        """ Add player to database"""
        self.view.display_text("add_player")
        player = got_player.create_player()
        self.view.display_instance(player)
        self.view.display_text("confirm-add-player")
        choice = utils.util.get_choice(["o", "n"])
        if choice == "o":
            storage.save(player)
            self.view.display_text("added_player")
        else:
            self.view.display_text("no_action")

    def display_all_players(self):
        """Display the list of players save in database."""
        self.view.display_items(storage.load_all(), "joueurs")

    def update_player(self):
        """Update a player in the database."""
        players = storage.load_all()
        self.view.display_items(players, "joueurs", select=True)
        old_player = self.view.select_item(players)
        self.view.display_text("updating_player")
        new_player = got_player.update_player(old_player)
        self.view.display_instance(new_player)
        self.view.display_text("confirm_update")
        choice: str = utils.util.get_choice(["o", "n"])
        if choice == "o":
            storage.update(old_player, new_player)
            self.view.display_text("confirm_updated")
        else:
            self.view.display_text("cancel-action")

    def delete_player(self):
        """Delete a player."""
        players = storage.load_all()
        self.view.display_items(players, "joueurs", select=True)
        player = self.view.select_item(players)
        self.view.display_text("confirm_delete")
        choice = utils.util.get_choice(["o", "n"])
        if choice == "o":
            storage.delete(player)
            self.view.display_text("confirm_deleted")
        else:
            self.view.display_text("cancel-action")




class Get_info_player:
    """Gets player's informations from the user"""

    def __init__(self, first_name: str, last_name: str, date_of_birth: str, sex: str):
        self.first_name = first_name,
        self.last_name = last_name,
        self.date_of_birth = date_of_birth,
        self.sex = sex,
        self.ranking = 1000

    def get_first_name(self, old_player, update: bool = False):
        """Gets first name or update it if 'update' is True."""
        if update:
            name = input(Fore.LIGHTBLUE_EX + f"{'  Prénom '}"
                         + Fore.LIGHTWHITE_EX + f"({old_player.first_name}): ").lower()
            value = utils.util.check_name(name) or old_player.first_name
            return value
        self.first_name = input("  Prénom: ").lower()
        while not utils.util.check_name_format(self.first_name):
            self.first_name = utils.util.wrong_entry(self.first_name)
        return self.first_name

    def get_last_name(self, old_player, update: bool = False):
        """Gets last name or update it if 'update' is True."""
        if update:
            name = input(Fore.LIGHTBLUE_EX + f"{'  Nom '}"
                         + Fore.LIGHTWHITE_EX + f"({old_player.last_name}): ").lower()
            value = utils.util.check_name(name) or old_player.last_name
            return value
        self.last_name = input("  Nom: ").lower()
        while not utils.util.check_name_format(self.last_name):
            self.last_name = utils.util.wrong_entry(self.last_name).lower()
        return self.last_name

    def get_player_date_of_birth(self, old_player, update: bool = False):
        """Gets date of birth or update it if 'update' is True."""
        if update:
            date = input(Fore.LIGHTBLUE_EX + f"{'  Date de naissance: '}"
                         + Fore.LIGHTWHITE_EX + f"({old_player.date_of_birth}): ").lower()
            value = utils.util.check_date(date) or old_player.date_of_birth
            return value
        self.date_of_birth = utils.util.replace_for_date(input("  Date de naissance(DD/MM/YYYY): "))
        while not utils.util.check_date_format(self.date_of_birth):
            self.date_of_birth = utils.util.replace_for_date(utils.util.wrong_entry(self.date_of_birth).lower())
        return self.date_of_birth

    def get_player_sex(self, old_player, update: bool = False):
        """Gets sex or update it if 'update' is True."""
        if update:
            sex = input(Fore.LIGHTBLUE_EX + "  Sexe "
                        + Fore.LIGHTWHITE_EX + f"({old_player.sex}) (tapez : 'f'  ou 'h'): ").lower()
            if sex == "f":
                sex = "femme"
            elif sex == "h":
                sex = "homme"
            value = utils.util.check_name(sex) or old_player.sex
            return value
        self.sex = input("  Sexe (tapez : 'f' pour femme ou 'h' pour homme): ").lower()
        while self.sex not in ["h", "f"]:
            self.sex = utils.util.wrong_entry(self.sex).lower()
        if self.sex == "f":
            self.sex = "femme"
        elif self.sex == "h":
            self.sex = "homme"
        return self.sex

    def get_player_ranking(self, old_player, update: bool = False):
        """Gets ranking or update it if 'update' is True."""
        if update:
            ranking = input(Fore.LIGHTBLUE_EX + "  Classement " + Fore.LIGHTWHITE_EX + f"({old_player.ranking}): ")
            value = utils.util.check_ranking(ranking) or old_player.ranking
            return int(value)
        self.ranking = input("  Classement: ")
        while not utils.util.check_ranking_format(self.ranking):
            self.ranking = utils.util.wrong_entry(self.ranking)
        return int(self.ranking)

    def create_player(self):
        """Create an instance of Player from previous items filling by the user."""
        player = Player(self.get_first_name(old_player=""),
                        self.get_last_name(old_player=""),
                        self.get_player_date_of_birth(old_player=""),
                        self.get_player_sex(old_player=""),
                        self.get_player_ranking(old_player=""))
        return player

    def update_player(self, old_player):
        """Create an instance of Player from previous items updating by the user."""
        player = Player(self.get_first_name(old_player, update=True),
                        self.get_last_name(old_player, update=True),
                        self.get_player_date_of_birth(old_player, update=True),
                        self.get_player_sex(old_player, update=True),
                        self.get_player_ranking(old_player, update=True))
        return player


got_player = Get_info_player("", "", "", "")
if __name__ == "__main__":
    pass
