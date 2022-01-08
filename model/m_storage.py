from typing import Protocol
from tinydb import TinyDB, where
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = SOURCE_DIR / "database.json"

db = TinyDB(DB_DIR, indent=4)
db_players = db.table("Database_players")
db_tournaments = db.table("Database_tournaments")


class Storage(Protocol):

    def delete(self, item):
        ...

    def load_all(self):
        return ...

    def load(self, item):
        return ...

    def save(self, item):
        ...

    def update(self, item):
        ...


class Tinydb(Storage):
    """Storage player by Tinydb"""

    def __init__(self, table):
        self.table = table

    def delete(self, item):
        self.table.remove(where('id_db') == item.id_db)

    def load_all(self):
        return self.table.all()

    def load(self, item):
        if isinstance(item, int):
            return self.table.get(doc_id=item)
        else:
            return self.table.get(doc_id=item.id_db)

    def save(self, item):
        return self.table.insert(item.serialize())

    def update(self, item):
        self.table.update(item.serialize(), doc_ids=[item.id_db])


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
    storage_t = Tinydb(db_tournaments)
    matches = [[1, 5], [2, 6], [3, 7], [4, 8]]





