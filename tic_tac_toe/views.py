"""Views module."""

from dependency_injector.wiring import Provide
from flask import request

from tic_tac_toe.service.game_service import GameService
from .containers import Container


def new_session(player: str, game_service: GameService = Provide[Container.game_service]):
    return game_service.new_session(player)


def start_game(game_service: GameService = Provide[Container.game_service]):
    return game_service.start_game()


def add_credits(player: str, game_service: GameService = Provide[Container.game_service]):
    return game_service.add_credits(player)


def make_move(player: str, game_service: GameService = Provide[Container.game_service]):
    return game_service.make_move(player, request)


def get_board(game_service: GameService = Provide[Container.game_service]):
    return game_service.get_board()


def get_credits(player: str, game_service: GameService = Provide[Container.game_service]):
    return game_service.get_credits(player)


def end_session(player: str, game_service: GameService = Provide[Container.game_service]):
    return game_service.end_session(player)


def get_stats(game_service: GameService = Provide[Container.game_service]):
    return game_service.get_stats()
