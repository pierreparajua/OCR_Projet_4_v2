from model.m_player import Player
from view.v_get_data_player import GetDataPlayer
from view.view import View, DICT_TEXT

got_player = GetDataPlayer("", "", "", "")


class PlayerController:
    """Controls the players."""

    def __init__(self):
        self.view: View = View(DICT_TEXT)

    def add_player(self):
        """ Add player to database"""
        self.view.display_text("add_player")
        player = got_player.create_player()
        self.view.display_text("confirm-add-player")
        self.view.display_item(player)
        return player

    def display_all_players(self, dict_players, display=True):
        """Display the list of players save in database."""
        players = [Player.deserialize(dict_player) for dict_player in dict_players]
        if display:
            self.view.display_items(players, "joueurs")
        return players

    def update_player(self, dict_players):
        """Update a player in the database."""
        players = self.display_all_players(dict_players, display=False)
        self.view.display_items(players, "joueurs", select=True)
        old_player = self.view.select_item(players)
        new_player = got_player.get_updating(old_player)
        self.view.display_instance(new_player)
        return new_player

    def delete_player(self, dict_players):
        """Delete a player."""
        players = self.display_all_players(dict_players, display=False)
        self.view.display_items(players, "joueurs", select=True)
        player = self.view.select_item(players)
        self.view.display_text("confirm_delete")
        return player
