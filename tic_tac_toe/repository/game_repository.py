from models.game import Game
from tic_tac_toe.models import db
from tic_tac_toe.models.player import Player


class GameRepository:

    def get_players(self):
        players = Player.query.all()
        # output = [player.name for player in players]
        return players
    def get_players_names(self, players):
        output = [player.name for player in players]
        return output

    def check_credits(self, player_name):
        player = Player.query.filter(Player.name == player_name).first()
        return player.credits

    def add_credits(self, player_name, amount):
        player = Player.query.filter(Player.name == player_name).first()
        player.credits += amount
        db.session.commit()
        return player.credits

    def get_credits(self, player):
        player = Player.query.filter(Player.name == player).first()
        return player.credits

    def end_session(self, player):
        player = Player.query.filter(Player.name == player).first()
        credits_ = player.credits
        game = Game()
        game.player_name = player.name
        game.credits = credits_
        db.session.commit()
        return True

    def get_symbol(self, player):
        player = Player.query.filter(Player.name == player).first()
        return player.symbol

    def save_result(self, player):
        game = Game()
        game.player_name = player
