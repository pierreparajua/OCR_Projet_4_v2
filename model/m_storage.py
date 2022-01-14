from typing import Protocol

from tinydb import TinyDB, where
from pathlib import Path

from utils.util import Menu

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


save_or_quit_menu = Menu(title="Souhaitez-vous:",
                         add_info="",
                         items=["Sauvegarder et continuer",
                                "Sauvegarder et retourner au menu",
                                "Annuler"],
                         choice="")



class ManageDataBase:
    def __init__(self, item):
        self.menu = save_or_quit_menu
        self.item = item

    def save_or_quit(self, table, update=True):
        if table is "storage_p":
            table = storage_p
        elif table is "storage_m":
            table = storage_t

        self.menu.display_menu()
        self.menu.choice = self.menu.get_choice()
        if self.menu.choice == "1":
            if not update:
                self.item.id_db = table.save(self.item)
            table.update(self.item)
        elif self.menu.choice == "2":
            if not update:
                self.item.id_db = table.save(self.item)
            table.update(self.item)
            if table is storage_p:
                self.player_manager()
            else:
                self.tournament_manager()
        elif self.menu.choice == "3":
            self.tournament_manager()


if __name__ == "__main__":
    pass
