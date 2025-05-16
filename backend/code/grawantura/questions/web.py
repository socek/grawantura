from typing import Generator

from starlette.requests import Request
from starlette.routing import Route

from grawantura.auth.jwtsupport import validate_user_id
from grawantura.events.drivers.commands import add_event
from grawantura.games.webhelpers import validate_game_id
from grawantura.main.web import WebEndpoint
from grawantura.questions.drivers import commands
from grawantura.questions.drivers import queries


@WebEndpoint
async def question_list(request: Request) -> dict:
    user_id = validate_user_id(request)
    game_id = validate_game_id(request, user_id)
    return {
        "items": list(queries.get_questions(game_id)),
    }


@WebEndpoint
async def create_question(request):
    user_id = validate_user_id(request)
    game_id = validate_game_id(request, user_id)

    payload = await request.json()
    commands.create_question(
        question=payload["question"],
        answer=payload["answer"],
        hints=payload["hints"],
        game_id=game_id,
    )
    add_event(
        {
            "type": "refresh",
            "group": "questions",
            "game_id": game_id,
        }
    )
    return {
        "status": "success",
    }


@WebEndpoint
async def update_question(request: Request) -> dict:
    user_id = validate_user_id(request)
    game_id = validate_game_id(request, user_id)

    payload = await request.json()
    commands.update_question(
        question_id=payload["question_id"],
        question=payload["question"],
        answer=payload["answer"],
        hints=payload["hints"],
    )
    add_event(
        {
            "type": "refresh",
            "group": "questions",
            "game_id": game_id,
        }
    )
    return {
        "status": "success",
    }


@WebEndpoint
async def delete_question(request: Request) -> dict:
    user_id = validate_user_id(request)
    game_id = validate_game_id(request, user_id)

    payload = await request.json()
    commands.delete_question(
        question_id=payload["question_id"],
    )
    add_event(
        {
            "type": "refresh",
            "group": "questions",
            "game_id": game_id,
        }
    )
    return {
        "status": "success",
    }


def get_routes(prefix: str) -> Generator[Route, None, None]:
    yield Route(prefix, question_list, methods=["GET"])
    yield Route(prefix, create_question, methods=["PUT"])
    yield Route(prefix, update_question, methods=["PATCH"])
    yield Route(prefix, delete_question, methods=["DELETE"])
