from decouple import config
from qq.plugins.types import Settings


def default() -> Settings:
    settings = Settings()
    settings["psql"] = psql()
    settings["logging"] = logging()
    return settings


def psql() -> Settings:
    name = config("POSTGRES_DB")
    user = config("POSTGRES_USER")
    password = config("POSTGRES_PASSWORD")
    host = config("POSTGRES_HOST")
    return {
        "url": f"postgresql+asyncpg://{user}:{password}@{host}:5432/{name}",
        "options": {
            "pool_recycle": config("DB_POOL_RECYCLE", 3600, cast=int),
            "pool_pre_ping": config("DB_PRE_PING", True, cast=bool),
            "pool_size": config("DB_SIZE", 40, cast=int),
            "max_overflow": config("DB_OVERFLOW", 20, cast=int),
        },
    }


def logging():
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
