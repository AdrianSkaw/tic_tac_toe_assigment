"""Application module."""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

from tic_tac_toe.containers import Container
from tic_tac_toe import views
from tic_tac_toe.models.player import Player
from tic_tac_toe.models.game import Game
from tic_tac_toe.models import db



def create_app() -> Flask:
    container = Container()
    container.config.github.auth_token.from_env("GITHUB_TOKEN")

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:password@localhost:5442/db'
    db.init_app(app)
    Migrate(app, db)
    app.container = container
    app.add_url_rule("/", "index", views.index, methods=['GET', 'POST'])

    bootstrap = Bootstrap()
    bootstrap.init_app(app)

    return app
