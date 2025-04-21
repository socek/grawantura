from datetime import datetime
from datetime import timedelta
from uuid import uuid4

from grawantura.main.testing import DbTest
from grawantura.play.drivers.commands import create_play
from grawantura.play.drivers.commands import delete_play
from grawantura.play.drivers.commands import update_play
from grawantura.play.drivers.queries import get_play_by_id
from grawantura.play.drivers.queries import get_plays


@DbTest
def test_creating(testdb):
    play_id = uuid4()
    now = datetime.now()
    create_play("My play", play_id=play_id, now=now, db=testdb)
    assert get_play_by_id(play_id, db=testdb) == {
        "id": play_id,
        "name": "My play",
        "created_at": now,
        "updated_at": now,
        "is_deleted": None,
        "game_id": None,
    }


@DbTest
def test_empty(testdb):
    assert get_play_by_id(uuid4(), db=testdb) is None


@DbTest
def test_listening(testdb):
    play_id = uuid4()
    game_id = uuid4()
    now = datetime.now()
    create_play("My play", play_id=play_id, game_id=game_id, now=now, db=testdb)
    assert list(get_plays(game_id, db=testdb)) == [
        {
            "id": play_id,
            "name": "My play",
            "created_at": now,
            "updated_at": now,
            "is_deleted": None,
            "game_id": game_id,
        }
    ]


@DbTest
def test_deleted(testdb):
    play_id = uuid4()
    game_id = uuid4()
    now = datetime.now()
    create_play("My play", game_id=game_id, play_id=play_id, now=now, db=testdb)

    delete_play(play_id)

    assert get_play_by_id(play_id, db=testdb) is None
    assert list(get_plays(game_id, db=testdb)) == []


@DbTest
def test_updating(testdb):
    play_id = uuid4()
    game_id = uuid4()
    now = datetime.now()

    after = datetime.now() + timedelta(seconds=1)
    new_game_id = uuid4()

    create_play("My play", play_id=play_id, game_id=game_id, now=now, db=testdb)

    update_play(play_id, "New Name", game_id=new_game_id, now=after, db=testdb)

    assert get_play_by_id(play_id, db=testdb) == {
        "id": play_id,
        "name": "New Name",
        "created_at": now,
        "updated_at": after,
        "is_deleted": None,
        "game_id": new_game_id,
    }


@DbTest
def test_updating_when_empty(testdb):
    play_id = uuid4()
    game_id = uuid4()
    now = datetime.now()

    create_play("My play", play_id=play_id, game_id=game_id, now=now, db=testdb)

    update_play(play_id)

    assert get_play_by_id(play_id, db=testdb) == {
        "id": play_id,
        "name": "My play",
        "created_at": now,
        "updated_at": now,
        "is_deleted": None,
        "game_id": game_id,
    }
