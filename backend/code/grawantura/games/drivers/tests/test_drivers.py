from datetime import datetime
from datetime import timedelta
from uuid import uuid4

from grawantura.games.drivers.commands import create_game
from grawantura.games.drivers.commands import delete_game
from grawantura.games.drivers.commands import update_game
from grawantura.games.drivers.queries import get_game_by_id
from grawantura.games.drivers.queries import get_games
from grawantura.games.drivers.queries import has_access
from grawantura.main.testing import DbTest


@DbTest
def test_creating(testdb):
    game_id = uuid4()
    user_id = uuid4()
    now = datetime.now()
    create_game("My Game", game_id=game_id, user_id=user_id, now=now, db=testdb)
    assert get_game_by_id(game_id, db=testdb) == {
        "id": game_id,
        "name": "My Game",
        "created_at": now,
        "updated_at": now,
        "is_deleted": None,
        "user_id": user_id,
    }


@DbTest
def test_empty(testdb):
    assert get_game_by_id(uuid4(), db=testdb) is None


@DbTest
def test_listening(testdb):
    game_id = uuid4()
    user_id = uuid4()
    now = datetime.now()
    create_game("My Game", game_id=game_id, user_id=user_id, now=now, db=testdb)
    assert list(get_games(db=testdb)) == [
        {
            "id": game_id,
            "name": "My Game",
            "created_at": now,
            "updated_at": now,
            "is_deleted": None,
            "user_id": user_id,
        }
    ]


@DbTest
def test_deleted(testdb):
    game_id = uuid4()
    user_id = uuid4()
    now = datetime.now()
    create_game("My Game", user_id=user_id, game_id=game_id, now=now, db=testdb)

    delete_game(game_id)

    assert get_game_by_id(game_id, db=testdb) is None
    assert list(get_games(db=testdb)) == []


@DbTest
def test_updating(testdb):
    game_id = uuid4()
    user_id = uuid4()
    now = datetime.now()

    after = datetime.now() + timedelta(seconds=1)
    new_user_id = uuid4()

    create_game("My Game", game_id=game_id, user_id=user_id, now=now, db=testdb)

    update_game(game_id, "New Name", user_id=new_user_id, now=after, db=testdb)

    assert get_game_by_id(game_id, db=testdb) == {
        "id": game_id,
        "name": "New Name",
        "created_at": now,
        "updated_at": after,
        "is_deleted": None,
        "user_id": new_user_id,
    }


@DbTest
def test_has_access_ok(testdb):
    game_id = uuid4()
    user_id = uuid4()
    now = datetime.now()

    assert has_access(user_id, game_id) is False

    create_game("My Game", game_id=game_id, user_id=user_id, now=now, db=testdb)
    assert has_access(user_id, game_id) is True


@DbTest
def test_has_access_fail(testdb):
    game_id = uuid4()
    user_id = uuid4()
    now = datetime.now()

    create_game("My Game", game_id=game_id, user_id=user_id, now=now, db=testdb)
    assert has_access(user_id, uuid4()) is False
    assert has_access(uuid4(), game_id) is False
