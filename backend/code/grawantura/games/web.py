from typing import Generator

from starlette.routing import Route

from grawantura.auth.jwtsupport import validate_user_id
from grawantura.games.drivers import commands
from grawantura.games.drivers.queries import get_games
from grawantura.main.web import WebEndpoint


@WebEndpoint
async def games_list(request) -> dict:
    user_id = validate_user_id(request)
    ic(user_id)
    return {
        "items": get_games(user_id),
    }


@WebEndpoint
async def create_game(request):
    user_id = validate_user_id(request)
    payload = await request.json()
    commands.create_game(name=payload["name"], user_id=user_id)
    return {
        "status": "success",
    }


@WebEndpoint
async def update_game(request) -> dict:
    validate_user_id(request)
    payload = await request.json()
    commands.update_game(
        game_id=payload["game_id"],
        name=payload["name"],
    )
    return {
        "status": "success",
    }


@WebEndpoint
async def delete_game(request) -> dict:
    validate_user_id(request)
    payload = await request.json()
    commands.delete_game(
        game_id=payload["game_id"],
    )
    return {
        "status": "success",
    }


def get_routes(prefix: str) -> Generator[Route, None, None]:
    yield Route(prefix, games_list, methods=["GET"])
    yield Route(prefix, create_game, methods=["POST"])
    yield Route(prefix, update_game, methods=["PATCH"])
    yield Route(prefix, delete_game, methods=["DELETE"])
