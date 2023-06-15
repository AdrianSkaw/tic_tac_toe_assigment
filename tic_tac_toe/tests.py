import unittest
from flask import jsonify
from unittest.mock import Mock, MagicMock

from application import app
from models.player import Player
from tic_tac_toe.service.game_service import GameService


class GameServiceTest(unittest.TestCase):
    def setUp(self):
        self.game_repository = Mock()
        self.game_service_validator = Mock()
        self.game_service = GameService(self.game_repository, self.game_service_validator)

    def test_new_session_returns_json_response(self):
        with app.app_context():
            self.game_repository.get_credits.return_value = 10
            expected_response = jsonify({'message': 'Nowa sesja gry dla: player1. Liczba kredytów: 10'})

            response = self.game_service.new_session('player1')

            self.assertEqual(response.data, expected_response.data)

    def test_start_game_returns_json_response(self):
        with app.app_context():
            self.game_service_validator.check_credits_to_join.return_value = True
            self.game_service_validator.player_exists.return_value = True
            player1 = Player(name='player1', credits=10, symbol='X')
            player2 = Player(name='player2', credits=10, symbol='O')
            self.game_repository.get_players.return_value = [player1, player2]
            self.game_repository.add_game.return_value = 1
            expected_response = jsonify({'message': f'Nowa gra o numerze id 1 rozpoczęta, zaczyna player1',
                                         'id': 1
                                         })

            response = self.game_service.start_game('player1')

            self.assertEqual(response.data, expected_response.data)


    def test_make_move_returns_json_response(self):
        with app.app_context():
            self.game_service_validator.game_exists.return_value = True
            self.game_service_validator.check_players_in_the_game.return_value = True
            self.game_service_validator.validate_input_data.return_value = True
            admin = Player(name='admin', credits=10, symbol='X')
            player1 = Player(name='player1', credits=10, symbol='X')
            player2 = Player(name='player2', credits=10, symbol='O')
            self.game_repository.add_game.return_value = 1
            self.game_repository.get_players.return_value = [admin, player1, player2]
            self.game_service.new_session('player1')
            self.game_service.new_session('player2')
            self.game_service.start_game('player1')
            self.game_service.start_game('player2')
            expected_response = jsonify({'message': 'Ruch wykonany'})
            request = Mock()
            request.json = {'row': 0, 'col': 0}
            response = self.game_service.make_move(1, 'player1', request)

        self.assertEqual(response.data, expected_response.data)



if __name__ == '__main__':
    unittest.main()
