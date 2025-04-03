from collections.abc import Iterable
from collections.abc import Mapping
from datetime import datetime
from functools import wraps
from uuid import UUID

from starlette.responses import JSONResponse


def sanitize(data: dict):
    """
    Sanitize data so it can be json serialize.
    """
    sanitized = {}
    for key, value in data.items():
        sanitized[key] = sanizite_value(value)
    return sanitized

def sanizite_value(value):
    if isinstance(value, UUID):
        return value.hex
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Mapping):
        return sanitize(value)
    if isinstance(value, Iterable) and not isinstance(value, str):
        return [sanizite_value(element) for element in value]
    return value

def WebEndpoint(fun):
    @wraps(fun)
    async def wrapper(*args, **kwargs):
        result = await fun(*args, **kwargs)
        if isinstance(result, Mapping):
            return JSONResponse(sanitize(result))
        return result

    return wrapper
