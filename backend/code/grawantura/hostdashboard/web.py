from random import choice
from typing import Generator

from starlette.requests import Request
from starlette.routing import Route

from grawantura.auth.jwtsupport import validate_user_id
from grawantura.events.drivers.commands import add_event
from grawantura.hostdashboard.drivers import commands
from grawantura.hostdashboard.drivers import queries
from grawantura.main.web import WebEndpoint
from grawantura.plays.webhelpers import validate_play_id


@WebEndpoint
async def question(request: Request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)

    return {
        "question": queries.current_question(play_id),
    }


@WebEndpoint
async def view(request: Request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)

    return {
        "name": queries.current_view(play_id).value,
    }


@WebEndpoint
async def draw_question(request: Request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)
    avalible_questions = queries.list_unused_questions(play_id)
    if len(avalible_questions) < 1:
        return {
            "status": "fail",
            "description": "not enough questions",
        }
    question_id = choice(avalible_questions)
    commands.draw_question(play_id, question_id)
    add_event(
        {
            "type": "host_action",
            "name": "draw_question",
            "question_id": "question_id",
            "play_id": play_id,
        }
    )
    return {
        "status": "ok",
        "question_id": question_id,
    }


@WebEndpoint
async def change_view(request: Request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)

    payload = await request.json()

    commands.change_view(play_id, queries.View(payload["name"]))
    add_event(
        {
            "type": "host_action",
            "name": "change_view",
            "view_name": payload["name"],
            "play_id": play_id,
        }
    )
    return {
        "status": "ok",
    }


def get_routes(prefix: str) -> Generator[Route]:
    yield Route(f"{prefix}/question", question, methods=["GET"])
    yield Route(f"{prefix}/view", view, methods=["GET"])

    yield Route(f"{prefix}/draw_question", draw_question, methods=["POST"])
    yield Route(f"{prefix}/change_view", change_view, methods=["POST"])
