from typing import Generator

from starlette.requests import Request
from starlette.routing import Route

from grawantura.auth.jwtsupport import validate_user_id
from grawantura.events.drivers.commands import add_event
from grawantura.games.webhelpers import validate_game_id
from grawantura.main.web import WebEndpoint
from grawantura.plays.drivers import commands
from grawantura.plays.drivers import queries


@WebEndpoint
async def play_list(request: Request) -> dict:
    user_id = validate_user_id(request)
    game_id = validate_game_id(request, user_id)
    return {
        "items": queries.get_plays(game_id),
    }


@WebEndpoint
async def create_play(request) -> dict:
    user_id = validate_user_id(request)
    game_id = validate_game_id(request, user_id)

    payload = await request.json()
    commands.create_play(
        name=payload["name"],
        game_id=game_id,
    )
    add_event(
        {
            "type": "refresh",
            "group": "plays",
            "game_id": game_id,
        }
    )
    return {
        "status": "success",
    }


@WebEndpoint
async def update_play(request: Request) -> dict:
    user_id = validate_user_id(request)
    game_id = validate_game_id(request, user_id)

    payload = await request.json()
    commands.update_play(
        play_id=payload["play_id"],
        name=payload["name"],
    )
    add_event(
        {
            "type": "refresh",
            "group": "plays",
            "game_id": game_id,
        }
    )
    return {
        "status": "success",
    }


@WebEndpoint
async def delete_play(request: Request) -> dict:
    user_id = validate_user_id(request)
    game_id = validate_game_id(request, user_id)

    payload = await request.json()
    commands.delete_play(
        play_id=payload["play_id"],
    )
    add_event(
        {
            "type": "refresh",
            "group": "plays",
            "game_id": game_id,
        }
    )
    return {
        "status": "success",
    }


def get_routes(prefix: str) -> Generator[Route]:
    yield Route(prefix, play_list, methods=["GET"])
    yield Route(prefix, create_play, methods=["PUT"])
    yield Route(prefix, update_play, methods=["PATCH"])
    yield Route(prefix, delete_play, methods=["DELETE"])
