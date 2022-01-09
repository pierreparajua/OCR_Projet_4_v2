import utils
from model.m_storage import Tinydb, db_players

storage_p = Tinydb(db_players)


class Player:
    def __init__(self, first_name: str, last_name: str, date_of_birth: str, sex: str,
                 id_db: int = 1, ranking: int = 1000):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.id_db = id_db
        self.ranking = ranking

    def __str__(self):
        """Display player's attributes."""
        return f"{self.first_name: <8} - {self.last_name: ^10} - {self.date_of_birth: ^10} - {self.sex: ^8} -" \
               f" {self.ranking: >3}"

    def __lt__(self, other):
        """Sort the Players by ranking"""
        return self.ranking > other.ranking



    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = utils.util.check_name(value).lower()

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = utils.util.check_name(value).lower()

    @property
    def date_of_birth(self):
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value):
        self._date_of_birth = utils.util.check_date(value)

    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self, value):
        self._sex = utils.util.check_sex(value)

    @property
    def ranking(self):
        return self._ranking

    @ranking.setter
    def ranking(self, value):
        self._ranking = utils.util.check_ranking(value)

    @staticmethod
    def deserialize(player_dict):
        """ This function deserialize a dict to create an instance of Player"""
        player = Player(player_dict["_first_name"],
                        player_dict["_last_name"],
                        player_dict["_date_of_birth"],
                        player_dict["_sex"],
                        player_dict["id_db"],
                        player_dict["_ranking"],
                        )
        return player

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def serialize(self):
        """ This function serialize an instance of Player"""
        return self.__dict__
    """"
    def player_from_id(self, table, id_db):
        return self.deserialize(table.load(id_db))
    """