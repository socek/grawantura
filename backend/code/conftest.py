from pytest import fixture
from pytest import mark
from qq.context import Context

from grawantura.main.globals import app
from grawantura.main.tables import SqlTable
from grawantura.main.tables import TableFinder

app.start("tests")


@fixture(scope="session")
def application():
    TableFinder(["grawantura"], []).find()
    engine = app.globals["sql"]["engine"]
    with engine.begin() as conn:
        SqlTable.metadata.drop_all(conn)
        SqlTable.metadata.create_all(conn)
    return app


@fixture
def testdb(application):
    with Context(application) as ctx:
        yield ctx["sql"]
