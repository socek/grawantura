from datetime import datetime
from datetime import timedelta
from uuid import uuid4

from grawantura.games.drivers.commands import create_game
from grawantura.main.testing import DbTest
from grawantura.play.drivers.commands import create_play
from grawantura.play.drivers.commands import delete_play
from grawantura.play.drivers.commands import update_play
from grawantura.play.drivers.queries import get_play_by_id
from grawantura.play.drivers.queries import get_plays
from grawantura.play.drivers.queries import has_access


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
    assert get_plays(game_id, db=testdb) == [
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
    assert get_plays(game_id, db=testdb) == []


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


@DbTest
def test_has_access_when_no_game_exists(testdb):
    assert has_access(uuid4(), uuid4(), db=testdb) is False


@DbTest
def test_has_access_when_different_user(testdb):
    left_game_id = uuid4()
    left_user_id = uuid4()
    left_play_id = uuid4()
    create_game("game", left_game_id, left_user_id)
    create_play("play", play_id=left_play_id, game_id=left_game_id, db=testdb)

    right_game_id = uuid4()
    right_user_id = uuid4()
    right_play_id = uuid4()
    create_game("game", right_game_id, right_user_id)
    create_play("play", play_id=right_play_id, game_id=right_game_id, db=testdb)
    assert has_access(left_user_id, right_play_id) is False


@DbTest
def test_has_access_when_same_user(testdb):
    game_id = uuid4()
    user_id = uuid4()
    play_id = uuid4()
    create_game("game", game_id, user_id)
    create_play("play", play_id=play_id, game_id=game_id, db=testdb)

    assert has_access(user_id, play_id) is True
