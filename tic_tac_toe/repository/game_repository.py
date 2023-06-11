from tic_tac_toe.models.game import Game
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

    def get_credits(self, player):
        player = Player.query.filter(Player.name == player).first()
        return player.credits

    def end_session(self, player):
        db.session.commit()
        return True

    def get_symbol(self, player):
        player = Player.query.filter(Player.name == player).first()
        return player.symbol

    def end_game(self, winner: Player, tie: str, game: Game, loser: Player, duration) -> None:
        new_game = Game(wins=winner.name, ties=tie, duration=duration)
        db.session.add(new_game)
        db.session.commit()
        return None

    def add_credits(self, player_name, amount):
        player = Player.query.filter(Player.name == player_name).first()
        player.credits += amount
        db.session.commit()
        return player.credits

    def get_stats(self):
        games = Game.query.all()
        output = {}
        for game in games:
            output[game.id] = {
                'wins': game.wins,
                'ties': game.ties,
                'duration': game.duration
            }

        return output
