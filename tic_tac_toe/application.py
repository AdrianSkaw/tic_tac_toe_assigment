"""Application module."""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate

from tic_tac_toe import views
from tic_tac_toe.containers import Container
from tic_tac_toe.models.player import Player
from tic_tac_toe.models.game import Game
from tic_tac_toe.models.symbol import Symbol
from tic_tac_toe.models import db


def create_app() -> Flask:
    container = Container()
    container.config.github.auth_token.from_env("GITHUB_TOKEN")

    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:password@localhost:5442/db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:password@db_pgsql:5432/db'
    db.init_app(app)
    Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.container = container
    app.add_url_rule('/api/new_session/<player>', 'new_session', views.new_session, methods=['POST'])
    app.add_url_rule('/api/new_game/', 'new_game', views.new_game, methods=['POST'])
    app.add_url_rule('/api/add_credits/<player>', 'add_credits', views.add_credits, methods=['POST'])
    app.add_url_rule('/api/move', 'move', views.make_move, methods=['POST'])
    app.add_url_rule('/api/board', 'board', views.get_board, methods=['GET'])
    app.add_url_rule('/api/credits/<player>', 'credits', views.get_credits, methods=['GET'])
    app.add_url_rule('/api/end_session/<player>', 'end_session', views.end_session, methods=['POST'])
    bootstrap = Bootstrap()
    bootstrap.init_app(app)

    return app
