from datetime import datetime

from starlette.requests import Request

from grawantura.events.drivers.queries import get_events
from grawantura.main.web import WebEndpoint


@WebEndpoint
async def events(request: Request):
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
