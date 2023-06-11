"""Tests module."""
import json

import pytest
from flask import request
from repository.game_repository import GameRepository
from tic_tac_toe.service.game_service import GameService
from validator.game_service_validator import GameServiceValidator
from .application import create_app


@pytest.fixture
def app():
    app = create_app()
    yield app


def test_start_session(app):
    with app.test_client() as client:
        response = client.post('/api/new_session/player1')
        assert response.status_code == 200
        assert response.json == {'message': 'Nowa sesja gry dla: player1. Liczba kredytów: 10'}


def test_add_credits_except_error(app):
    with app.test_client() as client:
        client.post('/api/new_session/player1')
        response = client.post('/api/add_credits/player1')
        assert response.status_code == 400
        assert response.json == {'error': 'Nie można dodać kredytów, ponieważ sesja się nie zakończyła.'}




# def test_win_game(app):
#     game_repository = GameRepository()
#     game_validator = GameServiceValidator(game_repository=game_repository)
#     game_session = GameService(game_repository=game_repository, game_service_validator=game_validator)
#     game_session.new_session('player1')
#     game_session.new_session('player2')
#     game_session.start_game()
#     game_session.make_move('player1', {'row': 0, 'column': 0})
#     game_session.make_move('player2', {'row': 1, 'column': 0})
#     game_session.make_move('player1', {'row': 0, 'column': 1})
#     game_session.make_move('player2', {'row': 1, 'column': 1})
#     game_session.make_move('player1', {'row': 0, 'column': 2})
#     assert game_session.make_move('player2', {'row': 1, 'column': 2}) == {'message': 'Wygrał gracz player2'}

def test_start_game_except_success(app):
    with app.test_client() as client:
        client.post('/api/new_session/player1')
        client.post('/api/new_session/player2')
        response = client.post('/api/start_game/')
        assert response.status_code == 200

def test_start_game_except_error(app):
    with app.test_client() as client:
        response = client.post('/api/start_game/')
        excepted_response = {'error': 'Nie ma dwóch graczy online'}
        assert response.json == excepted_response

def test_make_move(app):
    with app.test_client() as client:
        client.post('/api/new_session/player1')
        client.post('/api/new_session/player2')
        client.post('/api/start_game/')
        response = client.post('/api/move/player1', json = {'row': 0, 'col': 0})
        response = client.post('/api/move/player2', json = {'row': 1, 'col': 0})
        response = client.post('/api/move/player1', json = {'row': 0, 'col': 1})
        response = client.post('/api/move/player2', json = {'row': 1, 'col': 1})
        response = client.post('/api/move/player1', json = {'row': 0, 'col': 2})
        assert response.status_code == 200
        assert response.json == {'message': 'Gracz player1 wygrał!'}


def test_add_credits(app):
    with app.test_client() as client:
        client.post('/api/new_session/player1')
        response = client.post('/api/add_credits/player1')
        assert response.status_code == 200
        assert response.json == {'message': 'Gracz player1 posiada teraz 10 kredytów'}

def test_get_stats(app):
    with app.test_client() as client:

        response = client.get('/api/get_stats')
        assert response.status_code == 200