"""Views module."""
import json

from flask import request, render_template, jsonify
from dependency_injector.wiring import inject, Provide

from tic_tac_toe.models.player import Player
from tic_tac_toe.repository.game_repository import GameRepository
from tic_tac_toe.service.game_service import GameService

from .containers import Container



# Inicjalizacja planszy
board = [['', '', ''],
         ['', '', ''],
         ['', '', '']]

current_player = 'player1'






# Rozpoczęcie nowej sesji dla gracza
def new_session(player: str, game_service: GameService = Provide[Container.game_service]):
    return game_service.new_session(player)

def new_game(game_service: GameService = Provide[Container.game_service]):
    return game_service.new_game()

# Dodanie kredytów do konta gracza
def add_credits(player: str, game_service: GameService = Provide[Container.game_service]):
    return game_service.add_credits(player)



# Wykonanie ruchu
def make_move(game_service: GameService = Provide[Container.game_service]):
    return game_service.make_move(request)


# Pobranie aktualnego stanu planszy
def get_board():
    return jsonify(board)


def get_credits(player: str, game_service: GameService = Provide[Container.game_service]):
    return game_service.get_credits(player)



# Zakończenie sesji dla gracza
def end_session(player: str, game_service: GameService = Provide[Container.game_service]):
    return game_service.end_session(player)

