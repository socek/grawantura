from pytest import fixture
from pytest import mark
from qq.context import Context

from grawantura.main.globals import app
from grawantura.main.tables import SqlTable
from grawantura.main.tables import TableFinder

app.start("tests")


@fixture(scope="session")
async def application():
    TableFinder(["grawantura"], []).find()
    engine = app.globals["sql"]["engine"]
    async with engine.begin() as conn:
        await conn.run_sync(SqlTable.metadata.drop_all)
        await conn.run_sync(SqlTable.metadata.create_all)
    return app


@fixture(scope="session")
async def testdb(application):
    async with Context(application) as ctx:
        yield await ctx["sql"]
