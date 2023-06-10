from flask import jsonify

from tic_tac_toe.repository.game_repository import GameRepository
from validator.game_service_validator import GameServiceValidator


class GameService:
    def __init__(self, game_repository: GameRepository,
                 game_service_validator: GameServiceValidator
                 ):
        self.__game_repository = game_repository
        self.__game_service_validator = game_service_validator
        self.__board: list = []
        self.__current_player: str = ''
        self.__players_online: dict = {
            'player1': False,
            'player2': False,
        }

    def __get_players(self):
        players = self.__game_repository.get_players()
        self.__players = players

    def new_session(self, player: str) -> jsonify:
        self.__get_players()
        self.__game_service_validator.player_exists(player)

        self.__board = [['', '', ''],
                        ['', '', ''],
                        ['', '', '']]
        self.__current_player = player

        return jsonify({'message': f'Nowa sesja rozpoczęta dla gracza {player}'})

    def new_game(self) -> jsonify:
        self.__get_players()

        self.__board = [['', '', ''],
                        ['', '', ''],
                        ['', '', '']]
        self.__current_player = self.__players[0]

        return jsonify({'message': f'Nowa gra rozpoczęta, zaczyna {self.__current_player}'})

    def add_credits(self, player: str) -> jsonify:
        self.__game_service_validator.player_exists(player)

        credits = self.__game_repository.check_credits(player)

        if credits == 0:
            credits = self.__game_repository.add_credits(player, 10)

        return jsonify({'message': f'Gracz {player} posiada teraz {credits} kredytów'})

    def make_move(self, request) -> jsonify:
        global current_player
        row = int(request.json['row'])
        col = int(request.json['col'])
        player = current_player

        if self.__board[row][col] != '':
            return jsonify({'error': 'To pole jest już zajęte'})

        symbol = self.__game_repository.get_symbol(player)
        self.__board[row][col] = symbol

        if self.check_win(symbol):
            self.__game_repository.add_credits(player, 4)
            return jsonify({'message': f'Gracz {player} wygrał!'})

        self.__game_repository.add_credits(player, -3)

        credits = self.__game_repository.get_credits(player)
        if credits <= 0:
            return jsonify({'message': f'Gracz {player} przegrał i kończy sesję'})

        current_player = 'player2' if current_player == 'player1' else 'player1'

        return jsonify({'message': 'Ruch wykonany'})

    def check_win(self, player: str) -> bool:
        for i in range(3):
            if (self.__board[i][0] == self.__board[i][1] == self.__board[i][2] == player) or \
                    (self.__board[0][i] == self.__board[1][i] == self.__board[2][i] == player):
                return True
        if (self.__board[0][0] == self.__board[1][1] == self.__board[2][2] == player) or \
                (self.__board[0][2] == self.__board[1][1] == self.__board[2][0] == player):
            return True
        return False

    def get_credits(self, player: str) -> jsonify:
        self.__game_service_validator.player_exists(player)
        return self.__game_repository.get_credits(player)

    def end_session(self, player: str) -> jsonify:
        self.__game_service_validator.player_exists(player)
        self.__game_repository.end_session(player)
        return jsonify({'message': f'Sesja gracza {player} zakończona'})
