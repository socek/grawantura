from datetime import datetime
from uuid import uuid4

from grawantura.main.web import sanitize


def test_sanitize():
    data = {
        "id1": uuid4(),
        "now": datetime.now(),
        "map": {
            "id2": uuid4(),
            "now": datetime.now(),
        },
        "list": [
            uuid4(),
            datetime.now(),
        ],
        "normal": "elo",
    }

    assert sanitize(data) == {
        "id1": data["id1"].hex,
        "now": data["now"].isoformat(),
        "map": {
            "id2": data["map"]["id2"].hex,
            "now": data["map"]["now"].isoformat(),
        },
        "list": [
            data["list"][0].hex,
            data["list"][1].isoformat(),
        ],
        "normal": "elo",
    }
