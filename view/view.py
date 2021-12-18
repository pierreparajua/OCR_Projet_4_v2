from colorama import Fore, init

import json
from pathlib import Path

from model.m_player import Player
import utils

init(autoreset=True)

SOURCE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = SOURCE_DIR / "Chess_manager_text.json"


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


class View_player:
    def __init__(self, dict_text, player=Player("", "", "", "")):
        self.dict_text: dict = dict_text
        self.player: Player = player

    def display_text(self, key):
        with open(JSON_PATH, 'r', encoding='utf8') as fp:
            self.dict_text = json.load(fp)
        print(self.dict_text[key])

    def display_players(self, players):
        for i, player in enumerate(players):
            self.player = player
            print(f"{i + 1}: {self.player}")

    def get_first_name(self):
        first_name: str = input("  Prénom: ").lower()
        while not utils.util.check_name_format(first_name):
            utils.util.wrong_entry(first_name)
            first_name = input("  Prénom: ").lower()
        self.player.first_name = first_name
        return self.player.first_name

    def get_last_name(self):
        last_name: str = input("  Nom: ").lower()
        while not utils.util.check_name_format(last_name):
            utils.util.wrong_entry(last_name)
            last_name = input("  Nom: ").lower()
        self.player.last_name = last_name
        return self.player.last_name

    def get_player_date_of_birth(self):
        """
        Gets player's date of birth and return it.
        Returns:
            date_of_birth(str): Player's date of birth.
        """
        date_of_birth: str = utils.util.replace_for_date(input("  Date de naissance(DD/MM/YYYY): "))
        while not utils.util.check_date_format(date_of_birth):
            utils.util.wrong_entry(date_of_birth)
            date_of_birth = utils.util.replace_for_date(input("  Date de naissance(DD/MM/YYYY): "))
        self.player.date_of_birth = date_of_birth
        return self.player.date_of_birth

    def get_player_sex(self):
        """
        Get player's sex and return it.
        Returns:
            sex(str): Player's sex.
        """
        sex: str = input("  Sexe (tapez : 'f' pour femme ou 'h' pour homme): ").lower()
        while sex not in ["h", "f"]:
            utils.util.wrong_entry(sex)
            sex = input("  Sexe(tapez : 'f' pour femme ou 'h' pour homme): ").lower()
        if sex == "f":
            sex = "femme"
        elif sex == "h":
            sex = "homme"
        self.player.sex = sex
        return self.player.sex

    def get_player_ranking(self):
        """
        Gets player's ranking and return it.
        Returns:
            ranking(str): Player's ranking.
        """
        ranking = input("  Classement: ")
        while not utils.util.check_ranking_format(ranking):
            utils.util.wrong_entry(ranking)
            ranking = input("  Classement: ")
        ranking = int(ranking)
        self.player.ranking = ranking
        print("\n")
        return self.player.ranking

    def update_player_first_name(self, old_player, new_player):
        """
         Update item from "old_player" if necessary, and return an updated player.
         Args:
             old_player(Player): Base for updating.
             new_player(Player): Player to update.
         Returns:
             new_player.first_name(str): First name updated.
         """
        first_name = input(
            Fore.LIGHTBLUE_EX + f"{'  Prénom '}" + Fore.LIGHTWHITE_EX + f"({old_player.first_name}): ").lower()
        if first_name:
            while not utils.util.check_name_format(first_name):
                utils.util.wrong_entry(first_name)
                first_name = input(Fore.LIGHTBLUE_EX + f"{'  Prénom '}" + Fore.LIGHTWHITE_EX
                                   + f"({old_player.first_name}): ").lower()
            new_player.first_name = first_name
        else:
            new_player.first_name = old_player.first_name
        self.player.first_name = new_player.first_name
        return self.player.first_name

    def update_player_last_name(self, old_player, new_player):
        """
        Update item from "old_player" if necessary, and return an updated player.
        Args:
            old_player(Player): Base for updating.
            new_player(Player): Player to update.
        Returns:
            new_player.last_name(str): Last name updated.
        """
        last_name = input(Fore.LIGHTBLUE_EX + "  Nom " + Fore.LIGHTWHITE_EX + f"({old_player.last_name}): ").lower()
        if last_name:
            while not utils.util.check_name_format(last_name):
                utils.util.wrong_entry(last_name)
                last_name = input(Fore.LIGHTBLUE_EX + "  Nom "
                                  + Fore.LIGHTWHITE_EX + f"({old_player.last_name}): ").lower()
            new_player.last_name = last_name
        else:
            new_player.last_name = old_player.last_name
        self.player.last_name = new_player.last_name
        return self.player.last_name

    def update_player_date_of_birth(self, old_player, new_player):
        """
        Update item from "old_player" if necessary, and return an updated player.
        Args:
            old_player(Player): Base for updating.
            new_player(Player): Player to update.
        Returns:
            new_player.date_of_birth(str): Date_of_birth updated.
        """
        date_of_birth = utils.util.replace_for_date(input(Fore.LIGHTBLUE_EX + "  Date de naissance "
                                                          + Fore.LIGHTWHITE_EX + f"({old_player.date_of_birth}) : "))
        if date_of_birth:
            while not utils.util.check_date_format(date_of_birth):
                utils.util.wrong_entry(date_of_birth)
                date_of_birth = utils.util.replace_for_date(input(Fore.LIGHTBLUE_EX + "  Date de naissance "
                                                                  + Fore.LIGHTWHITE_EX
                                                                  + f"({old_player.date_of_birth}) : "))
                if not date_of_birth:
                    break
            new_player.date_of_birth = date_of_birth
        else:
            new_player.date_of_birth = old_player.date_of_birth
        self.player.date_of_birth = new_player.date_of_birth
        return self.player.date_of_birth

    def update_player_sex(self, old_player, new_player):
        """
           Update item from "old_player" if necessary, and return an updated player.
           Args:
               old_player(Player): Base for updating.
               new_player(Player): Player to update.
           Returns:
               new_player.sex(str): Sex updated.
           """
        sex = input(Fore.LIGHTBLUE_EX + "  Sexe "
                    + Fore.LIGHTWHITE_EX + f"({old_player.sex}) (tapez : 'f' pour femme ou 'h' pour homme): ").lower()
        if sex:
            while sex not in ["h", "f"]:
                utils.util.wrong_entry(sex)
                sex = input(Fore.LIGHTBLUE_EX + "  Sexe "
                            + Fore.LIGHTWHITE_EX
                            + f"({old_player.sex}) (tapez : 'f' pour femme ou 'h' pour homme): ").lower()
                if not sex:
                    break
            if sex == "f":
                sex = "femme"
            elif sex == "h":
                sex = "homme"
            new_player.sex = sex
        else:
            new_player.sex = old_player.sex

        self.player.sex = new_player.sex
        return self.player.sex

    def update_player_ranking(self, old_player, new_player):
        """
           Update item from "old_player" if necessary, and return an updated player.
           Args:
               old_player(Player): Base for updating.
               new_player(Player): Player to update.
           Returns:
               new_player.ranking(int): Ranking updated.
           """
        ranking = input(Fore.LIGHTBLUE_EX + "  Classement " + Fore.LIGHTWHITE_EX + f"({old_player.ranking}): ")
        while not utils.util.check_ranking_format(ranking):
            utils.util.wrong_entry(ranking)
            ranking = input(Fore.LIGHTBLUE_EX + "  Classement " + Fore.LIGHTWHITE_EX + f"({old_player.ranking}): ")
        if ranking:
            ranking = int(ranking)
            new_player.ranking = ranking
        else:
            new_player.ranking = old_player.ranking
        self.player.ranking = new_player.ranking
        return self.player.ranking


if __name__ == "__main__":
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
    print(data)"""
