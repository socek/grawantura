from icecream import ic
from icecream import install
from qq import Application
from qq.context import Context
from qq.plugin import Plugin
from qq.plugins import SettingsPlugin
from qq.plugins.logging import LoggingPlugin
from qq.plugins.sqlalchemy.plugin import AsyncSqlAlchemyPlugin

SQLALCHEMY_PLUGIN_KEY = "sql"


class IcecreamPlugin(Plugin):
    key = "icecream"

    def start(self, application: Application):
        print("Initializing debug with icecream")
        install()
        ic.configureOutput(includeContext=True, contextAbsPath=True)


class GrawanturaApplication(Application):
    def create_plugins(self):
        self.plugins(IcecreamPlugin())
        self.plugins(SettingsPlugin("grawantura.main.settings"))
        self.plugins(LoggingPlugin())
        self.plugins[SQLALCHEMY_PLUGIN_KEY] = AsyncSqlAlchemyPlugin()
