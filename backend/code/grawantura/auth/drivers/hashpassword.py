from hashlib import blake2b

from grawantura.main.globals import AppFun
from qq.injectors import SetInicjator
from qq.plugins.settings import SettingsInicjator


@AppFun
@SetInicjator("settings", SettingsInicjator("auth"))
def hash_password(password: str, settings: dict = None) -> str:
    passwordb = password.encode("utf8")
    return blake2b(passwordb, salt=settings["salt"]).hexdigest()
