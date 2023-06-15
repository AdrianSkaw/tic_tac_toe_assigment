"""Application module."""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate

from tic_tac_toe import controller
from tic_tac_toe.containers import Container
from tic_tac_toe.models.player import Player
from tic_tac_toe.models.game import Game
from tic_tac_toe.models.symbol import Symbol
from tic_tac_toe.models import db
from tic_tac_toe.validator.validation_exception import ValidationException


def create_app() -> Flask:
    container = Container()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:password@db_pgsql:5432/db'
    db.init_app(app)
    Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.container = container
    app.add_url_rule('/api/new_session/<player>', 'new_session', controller.new_session, methods=['POST'])
    app.add_url_rule('/api/start_game/<player>', 'start_game', controller.start_game, methods=['POST'])
    app.add_url_rule('/api/add_credits/<player>', 'add_credits', controller.add_credits, methods=['POST'])
    app.add_url_rule('/api/move/<id>/<player>', 'move', controller.make_move, methods=['POST']),
    app.add_url_rule('/api/board/<id_>', 'board', controller.get_board, methods=['GET'])
    app.add_url_rule('/api/credits/<player>', 'credits', controller.get_credits, methods=['GET'])
    app.add_url_rule('/api/end_session/<player>', 'end_session', controller.end_session, methods=['POST'])
    app.add_url_rule('/api/get_stats', 'get_stats', controller.get_stats, methods=['GET'])
    bootstrap = Bootstrap()
    bootstrap.init_app(app)

    return app


app = create_app()


@app.errorhandler(400)
def handle_bad_request(error):
    response = {
        'message': 'Bad Request',
        'status_code': 400
    }
    return response, 400


@app.errorhandler(ValidationException)
def handle_validation_exception(error):
    response = {
        'message': str(error),
        'status_code': 400
    }
    return response, 400
