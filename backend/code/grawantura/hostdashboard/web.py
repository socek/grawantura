from random import choice
from typing import Generator

from starlette.requests import Request
from starlette.routing import Route

from grawantura.auth.jwtsupport import validate_user_id
from grawantura.events.drivers.commands import add_event
from grawantura.main.web import WebEndpoint
from grawantura.plays.drivers import commands
from grawantura.plays.drivers import queries
from grawantura.plays.drivers.queries import list_unused_questions
from grawantura.plays.webhelpers import validate_play_id


@WebEndpoint
async def question(request: Request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)

    return {
        "question": queries.current_question(play_id),
    }

@WebEndpoint
async def draw_question(request: Request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)
    avalible_questions = list_unused_questions(play_id)
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


def get_routes(prefix: str) -> Generator[Route]:
    yield Route(f"{prefix}/question", question, methods=["GET"])
    yield Route(f"{prefix}/draw_question", draw_question, methods=["POST"])
