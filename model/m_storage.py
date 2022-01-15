from typing import Protocol

from tinydb import TinyDB, where
from pathlib import Path


SOURCE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = SOURCE_DIR / "database.json"

db = TinyDB(DB_DIR, indent=4)


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


class TinyDatabase(Storage):
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


storage_p = TinyDatabase(db.table("Database_players"))
storage_t = TinyDatabase(db.table("Database_tournaments"))
