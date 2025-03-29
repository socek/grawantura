from qq.injectors import SetApplication
from qq.injectors import SetInicjator
from qq.plugins.sqlalchemy.injectors import SesssionInicjator
from qq.plugins.sqlalchemy.injectors import TransactionInicjator

from grawantura.main.app import SQLALCHEMY_PLUGIN_KEY
from grawantura.main.app import GrawanturaApplication

app = GrawanturaApplication()

AppFun = SetApplication(app)

query_inicjator = SetInicjator("db", SesssionInicjator(SQLALCHEMY_PLUGIN_KEY))
transaction_inicjator = SetInicjator("db", TransactionInicjator(SQLALCHEMY_PLUGIN_KEY))

# database functions
Query = lambda fun: AppFun(query_inicjator(fun))
Command = lambda fun: AppFun(transaction_inicjator(fun))
