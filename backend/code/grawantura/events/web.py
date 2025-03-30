from datetime import datetime
from typing import Generator

from starlette.requests import Request
from starlette.routing import Route

from grawantura.auth.jwtsupport import validate_user_id
from grawantura.events.drivers.queries import get_events
from grawantura.main.web import WebEndpoint


@WebEndpoint
async def events(request: Request):
    validate_user_id(request)
    now = datetime.now()
    if not request.query_params.get("time"):
        return {
            "elements": [],
            "time": now,
        }

    fromtime = datetime.fromisoformat(request.query_params["time"])

    return {
        "elements": get_events(fromtime),
        "time": now,
    }


def get_routes(prefix: str) -> Generator[Route, None, None]:
    yield Route(prefix, events, methods=["GET"])
