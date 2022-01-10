from model.m_player import Player
from view.v_get_data_player import GetDataPlayer
from view.view import View


class PlayerController:
    """Controls the players."""

    def __init__(self):
        self.got_player = GetDataPlayer("", "", "", "")
        self.view = View("")

    def add_player(self):
        """ Add player to database"""
        self.view.display_text("add_player")
        player = self.got_player.create_player()
        self.view.display_text("confirm-add-player")
        self.view.item = player
        self.view.display_item()
        return player

    def display_all_players(self, dict_players, display=True):
        """Display the list of players save in database."""
        players = [Player.deserialize(dict_player) for dict_player in dict_players]
        if display:
            self.view.item = players
            self.view.display_items("joueurs")
        return players

    def update_player(self, dict_players):
        """Update a player in the database."""
        players = self.display_all_players(dict_players, display=False)
        self.view.item = players
        self.view.display_items("joueurs", select=True)
        old_player = self.view.select_item()
        new_player = self.got_player.get_updating(old_player)
        self.view.item = new_player
        self.view.display_item()
        return new_player

    def delete_player(self, dict_players):
        """Delete a player."""
        players = self.display_all_players(dict_players, display=False)
        self.view.item = players
        self.view.display_items("joueurs", select=True)
        player = self.view.select_item()
        self.view.display_text("confirm_delete")
        self.view.display_text("confirm_deleted")
        return player


