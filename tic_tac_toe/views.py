"""Views module."""

from flask import request, render_template
from dependency_injector.wiring import inject, Provide

from tic_tac_toe.service.game_service import GameService

from .containers import Container


@inject
def index(
        game_service: GameService = Provide[Container.game_service],
):

    return game_service.start_session()