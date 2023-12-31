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
        self.__current_player: Player = Player()
        self.__previous_player: Player = Player()
        self.__players_online: dict = {
        }
        self.__game = []

    def __get_players(self):
        players = self.__game_repository.get_players()
        self.__players = players

    def new_session(self, player: str) -> jsonify:
        self.__game_service_validator.player_exists(player)
        credits = self.__game_repository.get_credits(player)
        new_player = {'name': player, 'credits': credits, 'online': True, 'new_session': True}
        self.__players_online.update({new_player['name']: new_player})
        return jsonify(
            {'message': f'Nowa sesja gry dla: {player}. Liczba kredytów: {self.__players_online[player]["credits"]}'})

    def __check_game_to_join(self, player: str) -> bool:
        for game in self.__game:
            if game['previous_player'] is None and game['current_player'].name != player:
                return True
        return False

    def __join_to_game(self, player: str, game) -> jsonify:
        game['previous_player'] = [player_ for player_ in self.__players if player_.name == player][0]
        return jsonify(
            {'message': f'Gra o numerze id {game["id"]} rozpoczęta, grasz z  {game["current_player"].name}',
             'id': game["id"]
             })

    def __create_new_game(self, player: str) -> jsonify:
        game = Game()
        self.__start_game_time = datetime.now()
        game.wins = 'admin'

        current_player = [player_ for player_ in self.__players if player_.name == player][0]
        game_id = self.__game_repository.add_game(game)

        board = [['', '', ''],
                 ['', '', ''],
                 ['', '', '']]
        self.__game.append({'game': game,
                            'board': board,
                            'id': game_id,
                            'current_player': current_player,
                            'previous_player': None
                            })

        return jsonify({'message': f'Nowa gra o numerze id {game_id} rozpoczęta, zaczyna {current_player.name}',
                        'id': game_id
                        })

    def start_game(self, player: str) -> jsonify:
        self.__game_service_validator.player_exists(player)
        self.__get_players()
        self.__game_service_validator.check_credits_to_join(player, self.__players_online)

        if self.__check_game_to_join(player):
            for game in self.__game:
                if game['previous_player'] is None:
                    self.__join_to_game(player, game)
        return self.__create_new_game(player)

    def add_credits(self, player: str) -> jsonify:

        self.__game_service_validator.player_exists(player)
        credits = self.__game_repository.check_credits(player)

        if credits == 0 and self.__players_online[player]['new_session'] is True:
            credits = self.__game_repository.add_credits(player, 10)

            return jsonify({'message': f'Gracz {player} posiada teraz {credits} kredytów'})
        raise ValidationException('Nie można dodać kredytów, ponieważ sesja się nie zakończyła.')

    def __play_game(self, player: str, id_: int, request) -> jsonify:

        for game in self.__game:
            if game['previous_player'] is None:
                return jsonify({'warning': 'Nie ma jeszcze przeciwnika'})
            if player != game['current_player'].name:
                return jsonify({'warning': 'Teraz nie twoja kolej'}), 400

            row = int(request.json['row'])
            col = int(request.json['col'])

            if not game['id'] == id_:
                continue
            if game['board'][row][col] != '':
                return jsonify({'warning': 'To pole jest już zajęte'}), 400

            symbol = game['current_player'].symbol
            game['board'][row][col] = symbol

            status = self.__check_status(symbol, game['board'])
            if status == 'win':
                self.__handle_win(game)
                return jsonify({'message': f'Gracz {player} wygrał!'})
            elif status == 'tie':
                self.__handle_tie(game)
                return jsonify({'message': f'Gra zakończona remisem'})

            credits = game['current_player'].credits
            if credits <= 0:
                self.__handle_loss(player, credits)
                return jsonify({'message': f'Gracz {player} przegrał i kończy grę. Liczba kredytów: {credits}'})

            self.__swap_players(game)
            return jsonify({'message': 'Ruch wykonany'})

    def make_move(self, id_, player: str, request) -> jsonify:
        id_ = int(id_)
        self.__game_service_validator.game_exists(id_, self.__game)
        self.__game_service_validator.check_players_in_the_game(player, id_, self.__game)
        self.__game_service_validator.validate_input_data(request)
        return self.__play_game(player, id_, request)


    def __handle_win(self, game: dict):
        game['current_player'].credits += 4
        game['previous_player'].credits -= 3
        self.end_game(winner=game['current_player'], game=game, tie="no")

    def __handle_tie(self, game: dict):
        game['current_player'].credits += -3
        game['previous_player'].credits += -3
        self.end_game(game=game, tie="yes")

    def __handle_loss(self, player: str, credits):
        self.end_session(player)
        return jsonify({'message': f'Gracz {player} przegrał i kończy grę. Liczba kredytów: {credits}'})

    @staticmethod
    def __swap_players(game: dict):
        temp = game['current_player']
        game['current_player'] = game['previous_player']
        game['previous_player'] = temp

    @staticmethod
    def __check_status(player: str, board: list) -> str:
        for i in range(3):
            if (board[i][0] == board[i][1] == board[i][2] == player) or \
                    (board[0][i] == board[1][i] == board[2][i] == player):
                return 'win'
        if (board[0][0] == board[1][1] == board[2][2] == player) or \
                (board[0][2] == board[1][1] == board[2][0] == player):
            return 'win'
        if '' not in board[0] and '' not in board[1] and '' not in board[2]:
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

    def end_game(self, tie: str, game: dict, winner: Player = None, loser: Player = None) -> jsonify:
        duration = (datetime.now() - self.__start_game_time).total_seconds()
        game_obj = game['game']
        self.__game_repository.end_game(winner, tie, game_obj, loser, duration)
        for game in self.__game:
            if game['id'] == game_obj.id:
                self.__game.remove(game)
        return jsonify({'message': f'Gry zakończone'})

    def get_board(self, id_: str) -> jsonify:
        for game in self.__game:
            if game['id'] == int(id_):
                return jsonify({'board': game['board']})

    def get_stats(self):
        return jsonify({'stats': self.__game_repository.get_stats()})
