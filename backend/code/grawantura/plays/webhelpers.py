from uuid import UUID

from starlette.exceptions import HTTPException
from starlette.requests import Request

from grawantura.plays.drivers.queries import has_access


def validate_play_id(request: Request, user_id: UUID) -> UUID:
    play_id = UUID(request.path_params["play_id"])
    if not has_access(user_id, play_id):
        raise HTTPException(status_code=401)
    return play_id
