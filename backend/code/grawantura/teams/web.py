from typing import Generator

from starlette.requests import Request
from starlette.routing import Route

from grawantura.auth.jwtsupport import validate_user_id
from grawantura.events.drivers.commands import add_event
from grawantura.main.web import WebEndpoint
from grawantura.play.webhelpers import validate_play_id
from grawantura.teams.drivers import commands
from grawantura.teams.drivers import queries


@WebEndpoint
async def team_list(request: Request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)
    return {
        "items": queries.get_teams(play_id),
    }


@WebEndpoint
async def create_team(request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)

    payload = await request.json()
    commands.create_team(
        name=payload["name"],
        play_id=play_id,
    )
    add_event(
        {
            "type": "refresh",
            "group": "teams",
            "play_id": play_id,
        }
    )
    return {
        "status": "success",
    }


@WebEndpoint
async def update_team(request: Request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)

    payload = await request.json()
    commands.update_team(
        team_id=payload["team_id"],
        name=payload["name"],
    )
    add_event(
        {
            "type": "refresh",
            "group": "teams",
            "play_id": play_id,
        }
    )
    return {
        "status": "success",
    }


@WebEndpoint
async def delete_team(request: Request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)

    payload = await request.json()
    commands.delete_team(
        team_id=payload["team_id"],
    )
    add_event(
        {
            "type": "refresh",
            "group": "teams",
            "play_id": play_id,
        }
    )
    return {
        "status": "success",
    }


def get_routes(prefix: str) -> Generator[Route]:
    yield Route(prefix, team_list, methods=["GET"])
    yield Route(prefix, create_team, methods=["PUT"])
    yield Route(prefix, update_team, methods=["PATCH"])
    yield Route(prefix, delete_team, methods=["DELETE"])
