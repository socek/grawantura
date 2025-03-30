from datetime import datetime
from typing import Generator

from starlette.requests import Request
from starlette.routing import Route

from grawantura.main.web import WebEndpoint


@WebEndpoint
async def home(request: Request):
    return {
        "status": "running",
        "time": datetime.now().isoformat(),
    }


def get_routes(prefix: str) -> Generator[Route, None, None]:
    yield Route(prefix, home, methods=["GET"])
