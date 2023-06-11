from datetime import datetime

from flask import jsonify

from tic_tac_toe.models.game import Game
from tic_tac_toe.models.player import Player
from tic_tac_toe.repository.game_repository import GameRepository
from tic_tac_toe.validator.game_service_validator import GameServiceValidator
from tic_tac_toe.validator.validation_exception import ValidationException


class GameService:
    def __init__(self, game_repository: GameRepository,
                 game_service_validator: GameServiceValidator
                 ):
        self.__start_game_time = None
        self.__game_repository = game_repository
        self.__game_service_validator = game_service_validator
        self.__board: list = []
        self.__current_player: Player = Player()
        self.__previous_player: Player = Player()
        self.__players_online: dict = {
            'player1': {'online': False, 'new_session': False, credits: 0}, #TODO prepare login module and registration
            'player2': {'online': False, 'new_session': False, credits: 0},
        }
        self.__game = None
        self.__validation_exception = ValidationException()

    def __get_players(self):
        players = self.__game_repository.get_players()
        self.__players = players

    def new_session(self, player: str) -> jsonify:
        self.__game_service_validator.player_exists(player)
        self.__players_online[player]['new_session'] = True
        self.__players_online[player]['online'] = True
        self.__players_online[player]['credits'] = self.__game_repository.get_credits(player)
        return jsonify(
            {'message': f'Nowa sesja gry dla: {player}. Liczba kredytów: {self.__players_online[player]["credits"]}'})

    def start_game(self) -> jsonify:
        #TODO ADD LOGIN MODULE AND CHECK TO ONLY 2 PLAYERS ONLINE
        if self.__game is None:
            self.__game = Game()
            self.__start_game_time = datetime.now()
        if self.__players_online['player1']['online'] is False and self.__players_online['player2']['online'] is False:
            return self.__validation_exception.response(message='Nie ma dwóch graczy online')
        if self.__players_online['player1']['credits'] < 4 or self.__players_online['player2']['credits'] < 4:
            return self.__validation_exception.response(message='Za mało kredytów')

        self.__get_players()

        self.__board = [['', '', ''],
                        ['', '', ''],
                        ['', '', '']]

        self.__current_player = self.__players[0]

        return jsonify({'message': f'Nowa gra rozpoczęta, zaczyna {self.__current_player.name}'})

    def add_credits(self, player: str) -> jsonify:

        self.__game_service_validator.player_exists(player)
        credits = self.__game_repository.check_credits(player)

        if credits == 0 and self.__players_online[player]['new_session'] is True:
            credits = self.__game_repository.add_credits(player, 10)

            return jsonify({'message': f'Gracz {player} posiada teraz {credits} kredytów'})
        return self.__validation_exception.response('Nie można dodać kredytów, ponieważ sesja się nie zakończyła.')

    def make_move(self, player, request) -> jsonify:
        self.__game_service_validator.validate_input_data(request)
        self.__game_service_validator.player_exists(player)
        if player != self.__current_player.name:
            return jsonify({'warning': 'Teraz nie twoja kolej'})

        row = int(request.json['row'])
        col = int(request.json['col'])

        if self.__board[row][col] != '':
            return jsonify({'warning': 'To pole jest już zajęte'})

        symbol = self.__current_player.symbol
        self.__board[row][col] = symbol

        if self.check_status(symbol) == 'win':
            self.__current_player.credits += 4
            self.__previous_player.credits -= 3
            self.end_game(winner=self.__current_player, game=self.__game, tie="no")
            return jsonify({'message': f'Gracz {player} wygrał!'})
        if self.check_status(symbol) == 'tie':
            self.__current_player.credits += -3
            self.__previous_player.credits += -3
            self.end_game(game=self.__game, tie="yes")
            return jsonify({'message': f'Gra zakończona remisem'})

        credits = self.__current_player.credits
        if credits <= 0:
            self.end_session(player)
            return jsonify({'message': f'Gracz {player} przegrał i kończy gre. Liczba kredytów: {credits}'})

        self.__set_current_player()
        return jsonify({'message': 'Ruch wykonany'})

    def __set_current_player(self):
        if self.__current_player.name == 'player1':
            self.__current_player = self.__players[1]
            self.__previous_player = self.__players[0]
        else:
            self.__current_player = self.__players[0]
            self.__previous_player = self.__players[1]

    def check_status(self, player: str) -> str:
        for i in range(3):
            if (self.__board[i][0] == self.__board[i][1] == self.__board[i][2] == player) or \
                    (self.__board[0][i] == self.__board[1][i] == self.__board[2][i] == player):
                return 'win'
        if (self.__board[0][0] == self.__board[1][1] == self.__board[2][2] == player) or \
                (self.__board[0][2] == self.__board[1][1] == self.__board[2][0] == player):
            return 'win'
        if '' not in self.__board[0] and '' not in self.__board[1] and '' not in self.__board[2]:
            return 'tie'
        return 'continue'

    def get_credits(self, player: str) -> jsonify:
        self.__game_service_validator.player_exists(player)
        return self.__game_repository.get_credits(player)

    def end_session(self, player: str) -> jsonify:
        self.__game_service_validator.player_exists(player)
        self.__game_repository.end_session(self.__current_player)
        self.__players_online[player]['online'] = False
        return jsonify({'message': f'Sesja gracza {player} zakończona'})

    def end_game(self, tie: str, game: Game, winner: Player = None, loser: Player = None) -> jsonify:
        duration = (datetime.now() - self.__start_game_time).total_seconds()
        self.__game = self.__game_repository.end_game(winner, tie, game, loser, duration)
        return jsonify({'message': f'Gry zakończone'})

    def get_board(self):
        return jsonify({'board': self.__board})

    def get_stats(self):
        return jsonify({'stats': self.__game_repository.get_stats()})
