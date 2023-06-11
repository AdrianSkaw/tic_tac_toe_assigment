"""Containers module."""

from dependency_injector import containers, providers

from tic_tac_toe.repository.game_repository import GameRepository
from tic_tac_toe.service.game_service import GameService
from tic_tac_toe.validator.game_service_validator import GameServiceValidator


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".views"])

    config = providers.Configuration(yaml_files=["config.yml"])

    game_repository = providers.Singleton(
        GameRepository)
    game_service_validator = providers.Singleton(
        GameServiceValidator,
        game_repository=game_repository
    )
    game_service = providers.Singleton(
        GameService,
        game_repository=game_repository,
        game_service_validator=game_service_validator,

    )

    # github_client = providers.Factory(
    #     Github,
    #     login_or_token=config.github.auth_token,
    #     timeout=config.github.request_timeout,
    # )
    #
    # search_service = providers.Factory(
    #     services.SearchService,
    #     github_client=github_client,
    # )
