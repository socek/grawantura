from pytest import mark


def DbTest(fun):
    async def wrapper(*args, testdb, **kwargs):
        try:
            await fun(*args, testdb=testdb, **kwargs)
        finally:
            await testdb.rollback()

    return mark.asyncio(loop_scope="session")(
        mark.usefixtures("application")(mark.integration(wrapper))
    )
