from typing import Generator

from starlette.requests import Request
from starlette.routing import Route

from grawantura.auth.drivers import queries
from grawantura.auth.jwtsupport import create_jwt
from grawantura.main.web import WebEndpoint


@WebEndpoint
async def authorize(request: Request) -> dict:
    payload = await request.json()
    user_id = queries.validate_user(payload["email"], payload["password"])
    if not user_id:
        return {
            "status": "fail",
            "message": "user not validated",
        }
    return {"status": "success", "token": create_jwt(user_id)}


def get_routes(prefix: str) -> Generator[Route, None, None]:
    yield Route(prefix, authorize, methods=["POST"])
