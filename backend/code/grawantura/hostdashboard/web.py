from random import choice
from typing import Generator

from starlette.requests import Request
from starlette.routing import Route

from grawantura.auth.jwtsupport import validate_user_id
from grawantura.events.drivers.commands import add_event
from grawantura.hostdashboard.drivers import commands
from grawantura.hostdashboard.drivers import queries
from grawantura.hostdashboard.drivers.tables import EventTypenames
from grawantura.main.web import WebEndpoint
from grawantura.plays.webhelpers import validate_play_id


def calculate_money(events):
    result = {
        "money_pool": 0,
    }
    last_auction_win = None
    for event in events:
        if event["typename"] == EventTypenames.init_money.value:
            for key, value in event["payload"].items():
                result[key] = result.get(key, 0) + value
        elif event["typename"] == EventTypenames.end_auction.value:
            last_auction_win = max(event["payload"], key=event["payload"].get)
            for key, value in event["payload"].items():
                result[key] = result.get(key, 0) - value
                result["money_pool"] += value
        elif event["typename"] == EventTypenames.hint_bought.value:
            for key, value in event["payload"].items():
                result[key] = result.get(key, 0) - value
        elif event["typename"] == EventTypenames.answer.value:
            if event["payload"]["success"]:
                result[last_auction_win] = result.get(last_auction_win, 0) + result["money_pool"]
                result["money_pool"] = 0
    return result

def is_started(events) -> bool:
    for event in events:
        if event["typename"] == EventTypenames.init_money.value:
            return True
    return False


@WebEndpoint
async def question(request: Request) -> dict:
    user_id = validate_user_id(request)
    play_id = validate_play_id(request, user_id)

    events = list(queries.play_events(play_id))

    return {
        "question": queries.current_question(play_id),
        "events": events,
        "money": calculate_money(events),
        "is_started": is_started(events),
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


def get_routes(prefix: str) -> Generator[Route]:
    yield Route(f"{prefix}/question", question, methods=["GET"])
    yield Route(f"{prefix}/view", view, methods=["GET"])

    yield Route(f"{prefix}/draw_question", draw_question, methods=["POST"])
    yield Route(f"{prefix}/change_view", change_view, methods=["POST"])
    yield Route(f"{prefix}/start", start, methods=["POST"])
