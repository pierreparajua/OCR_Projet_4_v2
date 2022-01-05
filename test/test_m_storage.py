from tinydb import TinyDB
from pathlib import Path

from model.m_player import Player
from model.m_storage import Tinydb

SOURCE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = SOURCE_DIR / "database_test.json"

db = TinyDB(DB_DIR, indent=4)
db_test = db.table("Database_test")

pierre = Player("caroline", "sejil", "08/02/1984", "femme", 1, 1230)
storage = Tinydb()
storage.table = db_test
storage.item = pierre

db.drop_table("Database_test")


def test_save_update():
    storage.save()
    storage.update()
    assert storage.table.get(doc_id=pierre.id_db) == pierre.serialize()


def test_load_all():
    assert storage.load_all() == [pierre.serialize()]


def test_delete():
    storage.delete()
    assert storage.load_all() == []
