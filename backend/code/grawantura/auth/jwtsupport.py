from jwt import encode
from qq.injectors import SetInicjator
from qq.plugins.settings import SettingsInicjator

from grawantura.auth.drivers import queries
from grawantura.main.globals import AppFun


@AppFun
@SetInicjator("settings", SettingsInicjator("auth"))
def create_jwt(email: str, settings: dict = None) -> str:
    return encode({"email": email}, settings["jwt_secret"], algorithm="HS256")
