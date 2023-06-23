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
from tic_tac_toe.router import route


def create_app() -> Flask:
    container = Container()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:password@db_pgsql:5432/db'
    db.init_app(app)
    Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.container = container

    bootstrap = Bootstrap()
    bootstrap.init_app(app)
    route(app, controller)
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
