from abc import ABC, abstractmethod
from tinydb import TinyDB, Query, where

from pathlib import Path

from model.main_model import Player, Ronde

SOURCE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = SOURCE_DIR / "database.json"

db = TinyDB(DB_DIR, indent=4)
db_players = db.table("Database_players")
db_tournaments = db.table("Database_tournaments")


class Storage(ABC):
    @abstractmethod
    def delete(self, item):
        pass

    @abstractmethod
    def deserialize(self, item_dict):
        pass

    @abstractmethod
    def load_all(self):
        pass

    @abstractmethod
    def save(self, item):
        pass

    @abstractmethod
    def update(self, old_item, new_item):
        pass


class PlayerTinydb(Storage):
    """Storage player by Tinydb"""

    def delete(self, player):
        print(player)
        db_players.remove(where('id_db') == player.id_db)
        """
        not_player_in_tournament = True
        tournaments = Tournament.load_all_tournaments()
        for tournament in tournaments:
            all_players = [player for player in tournament.players]
            if player_id in all_players:
                not_player_in_tournament = False
                return not_player_in_tournament
        if not_player_in_tournament:
            database_players.remove(doc_ids=[player_id])
            return True
        """

    def deserialize(self, player_dict):
        """ This function deserialize a dict to create an instance of Player"""
        player = Player(player_dict["first_name"],
                        player_dict["last_name"],
                        player_dict["date_of_birth"],
                        player_dict["sex"],
                        player_dict["id_db"],
                        player_dict["ranking"])
        return player

    def load_all(self):
        """
        Load and deserialize  all players from database.
        Returns:
            players(list): list containing instances of all players from the database.
        """
        all_players = db_players.all()
        players = [self.deserialize(player_dict) for player_dict in all_players]
        return players

    def save(self, player):
        """ This function serialize and  add a player to database. """
        player.id_db = int(db_players.insert(player.__dict__))
        q_player = Query()
        db_players.update({"id_db": player.id_db}, q_player.fragment({"first_name": player.first_name,
                                                                      "last_name": player.last_name}))

    def update(self, old_player, new_player):
        """
        Update all items for a player
        Args:
            old_player(Player): player to update
            new_player(Player): player updated
        """
        q_player = Query()
        db_players.update({"first_name": new_player.first_name,
                           "last_name": new_player.last_name,
                           "date_of_birth": new_player.date_of_birth,
                           "sex": new_player.sex,
                           "id_db": new_player.id_db,
                           "ranking": new_player.ranking}, q_player.fragment({"first_name": old_player.first_name,
                                                                              "last_name": old_player.last_name}))


class TournamentTinydb(Storage):
    """Storage player by Tinydb"""

    def save(self, tournament):
        """ This function serialize and  add a tournament to database. """
        print("coucou")
        print(tournament.name)
        players_to_db = tournament.players
        rondes_to_db = Ronde.serialize_rondes(tournament.rondes)
        dict_t = {"name": tournament.name,
                  "place": tournament.place,
                  "date": tournament.date,
                  "nbr_of_rounds": tournament.nbr_of_rounds,
                  "rondes": rondes_to_db,
                  "players": players_to_db,
                  "time": tournament.time,
                  "description": tournament.description,
                  "id_bd": tournament.id_db}
        tournament.id_db = int(db_tournaments.insert(dict_t))
        db_tournaments.update({"id_db": tournament.id_db})

    def delete(self, player):
        pass

    def deserialize(self, item_dict):
        pass

    def load_all(self):
        pass

    def update(self, old_item, new_item):
        pass
