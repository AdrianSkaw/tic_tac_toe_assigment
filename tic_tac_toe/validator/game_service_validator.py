

from tic_tac_toe.models.player import Player
from tic_tac_toe.repository.game_repository import GameRepository
from tic_tac_toe.validator.validation_exception import ValidationException


class GameServiceValidator:
    def __init__(self, game_repository: GameRepository):
        self.__game_repository = game_repository

    def __get_players(self):
        return self.__game_repository.get_players()

    def player_exists(self, player: str):
        players = self.__get_players()
        players = self.__game_repository.get_players_names(players)
        if player not in players:
           raise ValidationException("Player does not exist")

    @staticmethod
    def validate_input_data(request):
        if not request.is_json:
            raise ValidationException("Invalid request data format. JSON expected.")
        if 'row' not in request.json or 'col' not in request.json:
            raise ValidationException("Invalid request data. 'row' and 'col' fields are required.")
        if not isinstance(request.json['row'], int) or not isinstance(request.json['col'], int):
            raise ValidationException("Invalid request data. 'row' and 'col' values must be integers.")
        if request.json['row'] < 0 or request.json['row'] > 2 or request.json['col'] < 0 or request.json['col'] > 2:
            raise ValidationException("Invalid request data. 'row' and 'col' values must be in range [0, 2].")

    @staticmethod
    def game_exists(id, games: list):
        for game in games:
            if game.get('id') == id:
                return True
        raise ValidationException(message="Game does not exist")

    @staticmethod
    def check_players_in_the_game(player: str, id: int, games: list):
        for game in games:
            if game['id'] == id:
                if player == game['current_player'].name or player == game['previous_player'].name:
                    break
                else:
                    raise ValidationException('Nie możesz wykonać ruchu w tej grze')

    @staticmethod
    def check_credits_to_join(player: str, players_online: dict):
        if players_online[player]['credits'] < 4:
            raise ValidationException(message='Za mało kredytów, doładuj konto')