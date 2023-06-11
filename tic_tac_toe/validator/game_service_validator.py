from dependency_injector.wiring import Provide

from tic_tac_toe.repository.game_repository import GameRepository
from tic_tac_toe.validator.validation_exception import ValidationException


class GameServiceValidator:
    def __init__(self, game_repository: GameRepository):
        self.__game_repository = game_repository

    def __get_players(self):
        return self.__game_repository.get_players()

    def player_exists(self, player):
        players = self.__get_players()
        players = self.__game_repository.get_players_names(players)
        if player not in players:
            ValidationException("Player does not exist")
