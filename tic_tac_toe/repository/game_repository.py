from tic_tac_toe.models.game import Game
from tic_tac_toe.models import db
from tic_tac_toe.models.player import Player


class GameRepository:

    @staticmethod
    def get_players():
        players = Player.query.all()
        return players

    @staticmethod
    def get_players_names(players):
        output = [player.name for player in players]
        return output

    @staticmethod
    def check_credits(player_name):
        player = Player.query.filter(Player.name == player_name).first()
        return player.credits

    @staticmethod
    def get_credits(player):
        player = Player.query.filter(Player.name == player).first()
        return player.credits

    @staticmethod
    def end_session(player):
        db.session.commit()
        return True

    @staticmethod
    def get_symbol(player):
        player = Player.query.filter(Player.name == player).first()
        return player.symbol

    @staticmethod
    def end_game(winner: Player, tie: str, game: Game, loser: Player, duration):
        new_game = Game(wins=winner.name, ties=tie, duration=duration)
        db.session.add(new_game)
        db.session.commit()

    @staticmethod
    def add_credits(player_name: str, amount: int) -> int:
        player = Player.query.filter(Player.name == player_name).first()
        player.credits += amount
        db.session.commit()
        return player.credits

    @staticmethod
    def get_stats():
        games = Game.query.all()
        output = {}
        for game in games:
            output[game.id] = {
                'wins': game.wins,
                'ties': game.ties,
                'duration': game.duration
            }

        return output

    @staticmethod
    def add_game(game: Game) -> int:
        db.session.add(game)
        db.session.commit()
        return game.id
