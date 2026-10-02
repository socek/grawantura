from grawantura.timer.models import get_now_ms
from typing import Generator

from starlette.requests import Request
from starlette.routing import Route

from grawantura.auth.jwtsupport import validate_user_id
from grawantura.main.web import WebEndpoint
from grawantura.plays.webhelpers import validate_play_id
from grawantura.timer.drivers import commands
from grawantura.timer.drivers import queries


@WebEndpoint
async def server_time(request: Request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)

    timer = queries.get_time_for_play(play_id)

    return {
        "server_time": get_now_ms(),
        "timer": {
            "status": timer["status"],
            "end_time": timer["end_time"],
        }
    }


@WebEndpoint
async def start(request: Request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)

    payload = await request.json()

    commands.start_timer(play_id, payload["microseconds"])
    return {
        "status": "ok",
    }


@WebEndpoint
async def stop(request: Request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)

    commands.stop_timer(play_id)

    return {
        "status": "ok",
    }


def get_routes(prefix: str) -> Generator[Route]:
    yield Route(f"{prefix}", server_time, methods=["GET"])
    yield Route(f"{prefix}/start", start, methods=["POST"])
    yield Route(f"{prefix}/stop", stop, methods=["POST"])
