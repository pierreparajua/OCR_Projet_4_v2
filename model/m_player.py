from abc import ABC, abstractmethod
from pathlib import Path

from tinydb import TinyDB, Query

SOURCE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = SOURCE_DIR / "database.json"

db = TinyDB(DB_DIR, indent=4)
db_players = db.table("Database_players")


class Player:
    def __init__(self, first_name: str, last_name: str, date_of_birth: str, sex: str, ranking: int = 1000):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.ranking = ranking

    def __str__(self):
        """Display player's attributes."""
        return f"{self.first_name: <8} - {self.last_name: ^10} - {self.date_of_birth: ^10} - {self.sex: ^8} -" \
               f" {self.ranking: >3}"

    def __lt__(self, other):
        """Sort the Players by ranking"""
        return self.ranking > other.ranking


class Player_storage(ABC):
    @abstractmethod
    def save(self, player):
        pass

    def get_id(self, player):
        pass

    def deserialize_player(self, player_dict):
        pass


class PlayerDB(Player_storage):
    """Storage player by Tinydb"""
    def deserialize_player(self, player_dict):
        """ This function deserialize a dict to create an instance of Player"""
        player = Player(player_dict["first_name"],
                        player_dict["last_name"],
                        player_dict["date_of_birth"],
                        player_dict["sex"],
                        player_dict["ranking"])
        return player

    def get_id(self, player):
        """
        Return the id number from the database.
        Returns:
            player_id(str): id from database
        """
        q_player = Query()
        db_player = db_players.get((q_player.fragment({"first_name": player.first_name.lower(),
                                                       "last_name": player.last_name.lower()})))
        player_id = db_player.doc_id
        return player_id

    def load_players(self):
        """
        Load and deserialize  all players from database.
        Returns:
            players(list): list containing instances of all players from the database.
        """
        all_players = db_players.all()
        players = [self.deserialize_player(player_dict) for player_dict in all_players]
        return players

    def save(self, player):
        """ This function serialize and  add a player to database. """
        db_players.insert(player.__dict__)

    def update_player(self, old_player, new_player):
        """
        Update all items for a player
        Args:
            old_player(Player): player to update
            new_player(Player): player updated
        """
        player_id = [self.get_id(old_player)]
        db_players.update({"first_name": new_player.first_name,
                           "last_name": new_player.last_name,
                           "date_of_birth": new_player.date_of_birth,
                           "sex": new_player.sex,
                           "ranking": new_player.ranking}, doc_ids=player_id)

    def delete_player(self, player):
        player_id = self.get_id(player)
        db_players.remove(doc_ids=[player_id])
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