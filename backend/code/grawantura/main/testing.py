from pytest import mark


def DbTest(fun):
    def wrapper(*args, testdb, **kwargs):
        try:
            fun(*args, testdb=testdb, **kwargs)
        finally:
            testdb.rollback()

    return mark.integration(wrapper)
