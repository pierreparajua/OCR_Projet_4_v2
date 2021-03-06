
from model.m_storage import storage_p


class Player:
    def __init__(self, first_name: str = "", last_name: str = "", date_of_birth: str = "", sex: str = "",
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
        """If score exist and the score are equal, so order by ranking"""
        try:
            if self.score == other.score:
                return self.ranking > other.ranking
            return self.score > other.score
        except AttributeError:
            return self.ranking > other.ranking

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value.lower()

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value.lower()

    @property
    def date_of_birth(self):
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value):
        self._date_of_birth = value

    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self, value):
        self._sex = value.lower()

    @property
    def ranking(self):
        return self._ranking

    @ranking.setter
    def ranking(self, value):
        self._ranking = value

    @staticmethod
    def deserialize(player_dict: dict):
        """
        This function deserialize a dict to create an instance of Player
        Args:
            player_dict: A dict containing all player's informations, coming from database
        Returns:
            player: an instance of Player.
        """
        player = Player(player_dict["_first_name"],
                        player_dict["_last_name"],
                        player_dict["_date_of_birth"],
                        player_dict["_sex"],
                        player_dict["id_db"],
                        player_dict["_ranking"]
                        )
        return player

    @staticmethod
    def player_from_id(id_db):
        return Player.deserialize(storage_p.load(id_db))

    def full_name(self):
        """Return the player's fullname"""
        return f"{self.first_name} {self.last_name}"

    def serialize(self):
        """This function serialize an instance of Player"""
        return self.__dict__
