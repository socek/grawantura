from datetime import datetime
from datetime import timedelta
from uuid import uuid4

from grawantura.games.drivers.commands import create_game
from grawantura.main.testing import DbTest
from grawantura.plays.drivers.commands import change_view
from grawantura.plays.drivers.commands import create_play
from grawantura.plays.drivers.commands import delete_play
from grawantura.plays.drivers.commands import draw_question
from grawantura.plays.drivers.commands import update_play
from grawantura.plays.drivers.queries import current_question
from grawantura.plays.drivers.queries import current_view
from grawantura.plays.drivers.queries import get_play_by_id
from grawantura.plays.drivers.queries import get_plays
from grawantura.plays.drivers.queries import has_access
from grawantura.plays.drivers.queries import list_unused_questions
from grawantura.plays.drivers.tables import View
from grawantura.questions.drivers.commands import create_question


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


@DbTest
def test_list_unused_questions_with_one_question_avalible(testdb):
    game_id = uuid4()
    user_id = uuid4()
    play_id = uuid4()
    question_id = uuid4()
    question_id2 = uuid4()

    create_game("game", game_id, user_id, db=testdb)
    create_question("question", "", "", game_id=game_id, question_id=question_id, db=testdb)
    create_question("question2", "", "", game_id=game_id, question_id=question_id2, db=testdb)
    create_play("play", play_id=play_id, game_id=game_id, db=testdb)
    draw_question(play_id, question_id, db=testdb)

    result = list_unused_questions(play_id, db=testdb)
    assert result == [question_id2]


@DbTest
def test_list_unused_questions_with_many_games(testdb):
    game_id = uuid4()
    game_id2 = uuid4()
    user_id = uuid4()
    play_id = uuid4()
    play_id2 = uuid4()
    question_id = uuid4()
    question_id2 = uuid4()

    create_game("game", game_id, user_id, db=testdb)
    create_question("question", "", "", game_id=game_id, question_id=question_id, db=testdb)
    create_play("play", play_id=play_id, game_id=game_id, db=testdb)

    create_game("game2", game_id2, user_id, db=testdb)
    create_question("question2", "", "", game_id=game_id2, question_id=question_id2, db=testdb)
    create_play("play", play_id=play_id2, game_id=game_id2, db=testdb)

    result = list_unused_questions(play_id, db=testdb)
    assert result == [question_id]


@DbTest
def test_list_unused_questions_with_many_plays(testdb):
    game_id = uuid4()
    user_id = uuid4()
    play_id = uuid4()
    play_id2 = uuid4()
    question_id = uuid4()

    create_game("game", game_id, user_id, db=testdb)
    create_question("question", "", "", game_id=game_id, question_id=question_id, db=testdb)
    create_play("play", play_id=play_id, game_id=game_id, db=testdb)
    create_play("play", play_id=play_id2, game_id=game_id, db=testdb)

    result = list_unused_questions(play_id, db=testdb)
    assert result == [question_id]


@DbTest
def test_current_question(testdb):
    game_id = uuid4()
    user_id = uuid4()
    play_id = uuid4()
    question_id = uuid4()
    question_id2 = uuid4()

    create_game("game", game_id, user_id, db=testdb)
    create_question("question", "", "", game_id=game_id, question_id=question_id, db=testdb)
    create_question("question2", "", "", game_id=game_id, question_id=question_id2, db=testdb)
    create_play("play", play_id=play_id, game_id=game_id, db=testdb)
    draw_question(play_id, question_id, db=testdb)
    draw_question(play_id, question_id2, db=testdb)

    result = current_question(play_id)
    assert result
    assert result["id"] == question_id2


@DbTest
def test_current_view_default(testdb):
    play_id = uuid4()
    assert current_view(play_id, db=testdb) == View.scoreboard


@DbTest
def test_current_view_with_one_change(testdb):
    play_id = uuid4()
    change_view(play_id, View.question)
    assert current_view(play_id, db=testdb) == View.question


@DbTest
def test_current_view_with_many_changes(testdb):
    play_id = uuid4()
    change_view(play_id, View.question)
    change_view(play_id, View.scoreboard)
    assert current_view(play_id, db=testdb) == View.scoreboard
