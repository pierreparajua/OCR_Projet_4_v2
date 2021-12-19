from colorama import Fore, init

import json
from pathlib import Path

from model.m_player import Player
import utils

init(autoreset=True)

SOURCE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = SOURCE_DIR / "Chess_manager_text.json"
DICT_TEXT = json.load(open(JSON_PATH, 'r', encoding='utf8'))


class View:
    def __init__(self, dict_text):
        self.dict_text = dict_text

    @staticmethod
    def display_instance(instance):
        print(instance)

    @staticmethod
    def display_players(players, name_item, select=False):
        print(f"Liste des {name_item} en base de donnée:")
        if select:
            print(f"Sélectionnez le {name_item[:-1]}: ")
        for i, player in enumerate(players):
            print(f"{i + 1}: {player}")

    def display_text(self, key):
        print(self.dict_text[key])

    def select_item(self, items):
        choice = utils.util.get_choice(list(map(str, list(range(1, len(items) + 1)))))
        self.display_text("selected_player")
        old_player = items[int(choice) - 1]
        self.display_instance(old_player)
        return old_player


class View_menu:
    def __init__(self, title, add_info, items, choice):
        self.title: str = title
        self.add_info: str = add_info
        self.items: list = items
        self.choice: str = choice

    def display_menu(self):
        print(Fore.LIGHTMAGENTA_EX + f"\n{self.title}:" + Fore.LIGHTWHITE_EX + f" {self.add_info}")
        for i, item in enumerate(self.items):
            print(f"{i + 1}: {item} ")

    def get_choice_list(self):
        choices_list = list(map(str, list(range(len(self.items) + 1))))[1:]
        choices_list.append("m")
        return choices_list

    def get_choices(self):
        self.choice = utils.util.get_choice(self.get_choice_list())
        return self.choice


class Get_info_player:
    def __init__(self):
        self.first_name = "",
        self.last_name = "",
        self.date_of_birth = "",
        self.sex = "",
        self.ranking = 1000

    def get_first_name(self, old_player, update=False):
        if update:
            name = input(Fore.LIGHTBLUE_EX + f"{'  Prénom '}"
                         + Fore.LIGHTWHITE_EX + f"({old_player.first_name}): ").lower()
            value = utils.util.check_name(name) or old_player.first_name
            return value
        self.first_name = input("  Prénom: ").lower()
        while not utils.util.check_name_format(self.first_name):
            self.first_name = utils.util.wrong_entry(self.first_name)
        return self.first_name

    def get_last_name(self, old_player, update=False):
        if update:
            name = input(Fore.LIGHTBLUE_EX + f"{'  Nom '}"
                         + Fore.LIGHTWHITE_EX + f"({old_player.last_name}): ").lower()
            value = utils.util.check_name(name) or old_player.last_name
            return value
        self.last_name = input("  Nom: ").lower()
        while not utils.util.check_name_format(self.last_name):
            self.last_name = utils.util.wrong_entry(self.last_name).lower()
        return self.last_name

    def get_player_date_of_birth(self, old_player, update=False):
        if update:
            date = input(Fore.LIGHTBLUE_EX + f"{'  Date de naissance: '}"
                         + Fore.LIGHTWHITE_EX + f"({old_player.date_of_birth}): ").lower()
            value = utils.util.check_date(utils.util.replace_for_date(date)) or old_player.last_name
            return value
        self.date_of_birth = utils.util.replace_for_date(input("  Date de naissance(DD/MM/YYYY): "))
        while not utils.util.check_date_format(self.date_of_birth):
            self.date_of_birth = utils.util.replace_for_date(utils.util.wrong_entry(self.date_of_birth).lower())
        return self.date_of_birth

    def get_player_sex(self, old_player, update=False):
        """
        Get player's sex and return it.
        Returns:
            sex(str): Player's sex.
        """
        if update:
            sex = input(Fore.LIGHTBLUE_EX + "  Sexe "
                        + Fore.LIGHTWHITE_EX + f"({old_player.sex}) (tapez : 'f'  ou 'h'): ").lower()
            if sex == "f":
                sex = "femme"
            elif sex == "h":
                sex = "homme"
            value = utils.util.check_name(sex) or old_player.last_name
            return value
        self.sex = input("  Sexe (tapez : 'f' pour femme ou 'h' pour homme): ").lower()
        while self.sex not in ["h", "f"]:
            self.sex = utils.util.wrong_entry(self.sex).lower()
        if self.sex == "f":
            self.sex = "femme"
        elif self.sex == "h":
            self.sex = "homme"
        return self.sex

    def get_player_ranking(self, old_player, update=False):
        """
        Gets player's ranking and return it.
        Returns:
            ranking(str): Player's ranking.
        """
        if update:
            ranking = input(Fore.LIGHTBLUE_EX + "  Classement " + Fore.LIGHTWHITE_EX + f"({old_player.ranking}): ")
            value = utils.util.check_ranking(ranking) or old_player.ranking
            return value
        self.ranking = input("  Classement: ")
        while not utils.util.check_ranking_format(self.ranking):
            self.ranking = utils.util.wrong_entry(self.ranking)
        print("\n")
        return int(self.ranking)

    def create_player(self):
        player = Player(self.get_first_name(old_player=""),
                        self.get_last_name(old_player=""),
                        self.get_player_date_of_birth(old_player=""),
                        self.get_player_sex(old_player=""),
                        self.get_player_ranking(old_player=""))
        return player

    def update_player(self, old_player):
        player = Player(self.get_first_name(old_player, update=True),
                        self.get_last_name(old_player, update=True),
                        self.get_player_date_of_birth(old_player, update=True),
                        self.get_player_sex(old_player, update=True),
                        self.get_player_ranking(old_player, update=True))
        return player



if __name__ == "__main__":
    pass
    """
    dict_chess_manager_text: dict = {
        "add_player_again": "Souhaitez vous ajouter un autre joueur(Tapez : 'o' ou 'n')",
        "add_player": "Pour ajouter un joueur, remplissez les champs suivants:",
        "confirm-add-player": "\nConfirmez l' ajouter du joueur à la base de donnée :  \n"
                              " (Tapez : 'o' ou 'n')",
        "added_player": "Le joueur a été ajouté à la base de donnée\n",
        "action": "    Action exécutée     \n",
        "no_action": "    Action non exécutée     \n",
        "sorted_player": "Voulez vous trier les joueurs par classement ('o' ou 'n')",
        "all_players": "\nListes des joueurs enregistrés en base de donnée :",
        "player_to_update": "Quel joueur de la liste souhaitez vous modifier: ",
        "selected_player": "Vous avez sélectionné: ",
        "updating_player": "\nModifier, si vous souhaitez, l' item entre parenthèse ou tapez 'Entrez' pour passer à l' "
                           "item suivant: ",
        "confirm_update": "Confirmez la modification( 'o' ou 'n'):",
        "confirm_updated": "Le joueur à été modifié dans la base de donnée\n",
        "cancel-action": "action non exécutée - retour au menu",
        "delete_player": "Quel joueur souhaitez vous supprimé: ",
        "confirm_delete_player": "Confirmez la suppression ( 'o' ou 'n'):",
        "player_in_tournament": "Le joueur sélectionné participe à un tournoi enregistré en base de donnée, "
                                "vous ne pouvez pas le supprimer",
        "confirm_deleted": "Le joueur à été supprimé de la base de donnée\n",
        "db_empty_player": " Pas de joueurs en base de donnée",
        "new_tournament": "\nCréation d' un nouveau tournoi",
        "ask_for_player": "Attention: "
                          "Les joueurs participant au tournoi doivent "
                          "être préalablement "
                          "saisie en base de donnée\n"
                          "Souhaitez vous créer un nouveau joueur ('o' ou 'n'): ",
        "fill_items": "Remplissez les champs suivants: ",
        "nb_player": "\nCombien de joueurs participent au tournois: ",
        "error_nb_player": "Le nombre de joueurs est insuffisant par rapport aux nombres de rondes",
        "select_player": "Sélectionner les joueurs pour le tournoi: ",
        "selected_player_for_tournament": "Sélectionner pour le tournoi",
        "already_selected": "Joueur déjà sélectionné",
        "resume_tournament": "\n---------Nouveau tournoi---------  ",
        "selected_players": "Liste des joueurs sélectionner pour le tournoi: ",
        "all-tournament": "\nListe des tournois sauvegardé en base de donné: ",
        "delete_tournament": "\nSélectionner un tournois pour le supprimer: ",
        "confirm_deleted_tournament": "Le tournois à été supprimé de la base de donnée\n",
        "db_empty_tournament": " Pas de tournois en base de donnée",
        "confirm_start_tournament": "\nPour reprendre ce tournoi tapez 'o', sinon tapez 'n'",
        "start_tournament": "----------Début du tournois----------\n"
                            " Liste des matchs pour la première ronde: ",
        "start_ronde": "Appuyer sur 'Entrez' pour lancer la ronde",
        "started_ronde": "La ronde a commencé le: ",
        "good_luck": "\n----------BONNE CHANCE A TOUS----------\n",
        "end_ronde": "Appuyer sur 'Entrez' pour finir la ronde",
        "ended_ronde": "La ronde a pris fin le: ",
        "get_score": "\nVeuillez renseigner le résultat des matchs:",
        "score_error": "\nErreur dans les scores: "
                       "veuillez saisir '0', '1' ou '0.5'\n",
        "save_or_quit": "\nSouhaitez vous: "
                        "\n 1: Sauvegarder et continuer le tournoi"
                        "\n 2: Sauvegarder et quitter",
        "end_tournament": "\n\n             ------FIN DU TOURNOIS-------\n"
    }

    with open(JSON_PATH, 'w', encoding='utf8') as fp:
        json.dump(dict_chess_manager_text, fp, indent=4)
    with open(JSON_PATH, 'r', encoding='utf8') as fp:
        data = json.load(fp)
    print(data)
    

    old_name = "Yves"
    new_name = input(Fore.LIGHTBLUE_EX + f"{'  Prénom '}"
                                       + Fore.LIGHTWHITE_EX + f"({old_name}): ").lower()
    value = check_name(new_name) or old_name
    print(value)
    print(old_name)
    print(new_name)"""
