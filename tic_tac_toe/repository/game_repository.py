from tic_tac_toe.models.player import Player
from tic_tac_toe.models import db
from sqlalchemy import select
class GameRepository:


    def get_players(self):
        players = Player.query.all()
        output = [player.name for player in players]
        return output

    def check_credits(self, player_name):
        player = Player.query.filter(Player.id == player_name).first()
        return player.credits
    def add_credits(self, player_name, amount):
        player = Player.query.filter(Player.id == player_name).first()
        player.credits += amount
        db.session.commit()
        return player.credits