from uuid import UUID

from starlette.exceptions import HTTPException
from starlette.requests import Request

from grawantura.games.drivers.queries import has_access


def validate_game_id(request: Request, user_id: UUID) -> UUID:
    game_id = UUID(request.path_params["game_id"])
    if not has_access(user_id, game_id):
        raise HTTPException(status_code=401)
    return game_id
