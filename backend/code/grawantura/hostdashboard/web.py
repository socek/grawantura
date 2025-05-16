from random import choice
from typing import Generator

from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.routing import Route

from grawantura.auth.jwtsupport import validate_user_id
from grawantura.events.drivers.commands import add_event
from grawantura.hostdashboard.drivers import commands
from grawantura.hostdashboard.drivers import queries
from grawantura.hostdashboard.event import HintsCalculator
from grawantura.hostdashboard.event import MoneyCalculator
from grawantura.hostdashboard.event import answering_team_id
from grawantura.hostdashboard.event import is_started
from grawantura.hostdashboard.event import show_hint
from grawantura.main.web import WebEndpoint
from grawantura.plays.drivers.queries import get_game_id
from grawantura.plays.webhelpers import get_play_id
from grawantura.plays.webhelpers import validate_play_id


@WebEndpoint
async def question(request: Request) -> dict:
    play_id = get_play_id(request)
    game_id = get_game_id(play_id)

    if not game_id:
        raise HTTPException(status_code=404)

    events = list(queries.play_events(play_id))

    return {
        "question": queries.current_question(play_id),
        "events": events,
        "money": MoneyCalculator().calculate(events),
        "hints": HintsCalculator().calculate(events),
        "is_started": is_started(events),
        "answering_team_id":  answering_team_id(events),
        "show_hint": show_hint(events),
        "game_id": game_id,
    }


@WebEndpoint
async def view(request: Request) -> dict:
    play_id = get_play_id(request)

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


@WebEndpoint
async def start(request: Request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)

    payload = await request.json()
    commands.init_money(play_id, payload["money"])
    add_event(
        {
            "type": "host_action",
            "name": "game start",
            "play_id": play_id,
        }
    )

    return {
        "status": "ok",
    }


@WebEndpoint
async def end_auction(request: Request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)

    payload = await request.json()
    commands.end_auction(play_id, payload["money"])
    add_event(
        {
            "type": "host_action",
            "name": "end auction",
            "play_id": play_id,
        }
    )

    return {
        "status": "ok",
    }


@WebEndpoint
async def hint(request: Request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)

    payload = await request.json()
    commands.hint(play_id, payload["change"], payload["money"])
    add_event(
        {
            "type": "host_action",
            "name": "hint",
            "play_id": play_id,
        }
    )

    return {
        "status": "ok",
    }

@WebEndpoint
async def answer(request: Request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)

    payload = await request.json()
    commands.answer(play_id, payload["success"])
    add_event(
        {
            "type": "host_action",
            "name": "answer",
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
    yield Route(f"{prefix}/start", start, methods=["POST"])
    yield Route(f"{prefix}/end_auction", end_auction, methods=["POST"])
    yield Route(f"{prefix}/hint", hint, methods=["POST"])
    yield Route(f"{prefix}/answer", answer, methods=["POST"])
