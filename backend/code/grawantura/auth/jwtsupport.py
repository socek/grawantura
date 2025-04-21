from uuid import UUID

from jwt import decode
from jwt import encode
from jwt.exceptions import PyJWTError
from qq.injectors import SetInicjator
from qq.plugins.settings import SettingsInicjator
from starlette.exceptions import HTTPException
from starlette.requests import Request

from grawantura.auth.drivers import queries
from grawantura.main.globals import AppFun


@AppFun
@SetInicjator("settings", SettingsInicjator("auth"))
def create_jwt(user_id: UUID, settings: dict = None) -> str:
    payload = {"user_id": user_id.hex}
    return encode(payload, settings["jwt_secret"], algorithm="HS256")


def validate_user_id(request: Request) -> UUID:
    bearer_token = request.headers.get("auth_token")
    if bearer_token is None:
        raise HTTPException(status_code=401)
    return validate_user_id_from_token(bearer_token)


@AppFun
@SetInicjator("settings", SettingsInicjator("auth"))
def validate_user_id_from_token(token, settings: dict = None) -> UUID:
    try:
        payload = decode(token, settings["jwt_secret"], algorithms=["HS256"])
    except PyJWTError:
        raise HTTPException(status_code=401)
    try:
        is_validated = queries.validate_user_id(payload["user_id"])
    except KeyError:
        raise HTTPException(status_code=401)
    if not is_validated:
        raise HTTPException(status_code=401)
    return payload["user_id"]
