
from flask import jsonify

from tic_tac_toe.repository.game_repository import GameRepository

# Informacje o graczach
players = {'player1': {'symbol': 'X', 'credits': 0},
           'player2': {'symbol': 'O', 'credits': 0}}
current_player = 'player1'

class GameService:
    def __init__(self, game_repository: GameRepository):
        self.__game_repository = game_repository

    def __get_players(self):
        self.__players = self.__game_repository.get_players()

    def new_session(self, player):
        self.__get_players()
        if player not in self.__players:
            return jsonify({'error': 'Nieprawidłowy gracz'})

        global board, current_player
        board = [['', '', ''],
                 ['', '', ''],
                 ['', '', '']]
        current_player = player

        if players[player]['credits'] == 0:
            players[player]['credits'] = 10

        return jsonify({'message': f'Nowa sesja rozpoczęta dla gracza {player}'})

    def add_credits(self, player):
        if player not in self.__players:
            return jsonify({'error': 'Nieprawidłowy gracz'})

        credits = self.__game_repository.check_credits(player)

        if credits == 0:
            credits = self.__game_repository.add_credits(player, 10)



        return jsonify({'message': f'Gracz {player} posiada teraz {credits} kredytów'})

    def make_move(self, request):
        global current_player
        row = int(request.json['row'])
        col = int(request.json['col'])
        player = current_player

        if board[row][col] != '':
            return jsonify({'error': 'To pole jest już zajęte'})

        board[row][col] = players[player]['symbol']

        if self.check_win(players[player]['symbol']):
            players[player]['credits'] += 4
            return jsonify({'message': f'Gracz {player} wygrał!'})

        players[player]['credits'] -= 3

        if players[player]['credits'] < 0:
            return jsonify({'message': f'Gracz {player} przegrał i kończy sesję'})

        current_player = 'player2' if current_player == 'player1' else 'player1'

        return jsonify({'message': 'Ruch wykonany'})

    # Sprawdzenie, czy wystąpiła wygrana
    def check_win(self, player):
        for i in range(3):
            if (board[i][0] == board[i][1] == board[i][2] == player) or \
                    (board[0][i] == board[1][i] == board[2][i] == player):
                return True
        if (board[0][0] == board[1][1] == board[2][2] == player) or \
                (board[0][2] == board[1][1] == board[2][0] == player):
            return True
        return False