from typing import Protocol
from tinydb import TinyDB, where
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = SOURCE_DIR / "database.json"

db = TinyDB(DB_DIR, indent=4)
db_players = db.table("Database_players")
db_tournaments = db.table("Database_tournaments")


class Storage(Protocol):

    def delete(self):
        ...

    def load_all(self):
        return ...

    def save(self):
        ...

    def update(self):
        ...


class Tinydb(Storage):
    """Storage player by Tinydb"""

    def __init__(self, table, item):
        self.table = table
        self.item = item

    def delete(self):
        self.table.remove(where('id_db') == self.item.id_db)

    def load_all(self):
        return self.table.all()

    def save(self):
        self.item.id_db = self.table.insert(self.item.serialize())

    def update(self):
        self.table.update(self.item.serialize(), doc_ids=[self.item.id_db])


"""
class TournamentTinydb:

    def save(self, tournament):

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
"""

if __name__ == "__main__":
    pass
