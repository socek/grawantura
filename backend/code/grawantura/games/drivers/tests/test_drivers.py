from datetime import datetime
from uuid import uuid4

from grawantura.games.drivers.commands import create_game
from grawantura.games.drivers.queries import get_game_by_id
from grawantura.games.drivers.queries import get_games
from grawantura.main.testing import DbTest


@DbTest
def test_creating(testdb):
    game_id = uuid4()
    now = datetime.now()
    create_game("My Game", game_id=game_id, now=now, db=testdb)
    assert get_game_by_id(game_id, db=testdb) == {
        "id": game_id,
        "name": "My Game",
        "created_at": now,
        "updated_at": now,
    }


@DbTest
def test_empty(testdb):
    assert get_game_by_id(uuid4(), db=testdb) is None


@DbTest
def test_listening(testdb):
    game_id = uuid4()
    now = datetime.now()
    create_game("My Game", game_id=game_id, now=now, db=testdb)
    assert list(get_games(db=testdb)) == [
        {
            "id": game_id,
            "name": "My Game",
            "created_at": now,
            "updated_at": now,
        }
    ]
