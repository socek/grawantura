from decouple import config
from qq.plugins.settings import TESTS_KEY
from qq.plugins.types import Settings


def default() -> Settings:
    settings = Settings()
    settings["sql"] = sql()
    settings["logging"] = logging()
    settings["auth"] = auth()
    return settings


def sql() -> Settings:
    name = config("POSTGRES_DB")
    user = config("POSTGRES_USER")
    password = config("POSTGRES_PASSWORD")
    host = config("POSTGRES_HOST")
    return {
        "url": f"postgresql+psycopg2://{user}:{password}@{host}:5432/{name}",
        "options": {
            "pool_recycle": config("DB_POOL_RECYCLE", 3600, cast=int),
            "pool_pre_ping": config("DB_PRE_PING", True, cast=bool),
            "pool_size": config("DB_SIZE", 40, cast=int),
            "max_overflow": config("DB_OVERFLOW", 20, cast=int),
        },
    }


def logging() -> Settings:
    return {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "generic": {
                "format": "%(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "generic",
            },
        },
        "loggers": {
            "": {
                "level": "DEBUG",
                "handlers": [],
            },
            "sqlalchemy": {
                "level": "ERROR",
                "handlers": ["console"],
                "qualname": "sqlalchemy.engine",
            },
            "alembic": {
                "level": "ERROR",
                "handlers": ["console"],
                "qualname": "alembic",
            },
            "grawantura": {
                "level": "DEBUG",
                "handlers": ["console"],
                "qualname": "fajabot",
            },
        },
    }


def auth() -> Settings:
    return {
        "salt": config("AUTH_SALT", "x").encode("UTF8"),
        "jwt_secret": config("AUTH_JWT_SECRET", "xy").encode("UTF8"),
    }


# --------------------
# Tests settings below
# --------------------


def tests() -> Settings:
    settings = default()
    settings[TESTS_KEY] = True
    settings["sql"] = test_sql()
    return settings


def test_sql() -> Settings:
    name = f"{config('POSTGRES_DB')}_tests"
    user = config("POSTGRES_USER")
    password = config("POSTGRES_PASSWORD")
    host = config("POSTGRES_HOST")
    return {
        "url": f"postgresql+psycopg2://{user}:{password}@{host}:5432/{name}",
        "options": {
            "pool_recycle": config("DB_POOL_RECYCLE", 3600, cast=int),
            "pool_pre_ping": config("DB_PRE_PING", True, cast=bool),
            "pool_size": config("DB_SIZE", 40, cast=int),
            "max_overflow": config("DB_OVERFLOW", 20, cast=int),
        },
    }
