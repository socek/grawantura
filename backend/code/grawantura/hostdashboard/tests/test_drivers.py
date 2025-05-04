from uuid import UUID
from uuid import uuid4

from grawantura.games.drivers.commands import create_game
from grawantura.hostdashboard.drivers.commands import answer
from grawantura.hostdashboard.drivers.commands import change_view
from grawantura.hostdashboard.drivers.commands import draw_question
from grawantura.hostdashboard.drivers.commands import end_auction
from grawantura.hostdashboard.drivers.commands import hint_bought
from grawantura.hostdashboard.drivers.commands import init_money
from grawantura.hostdashboard.drivers.queries import current_money
from grawantura.hostdashboard.drivers.queries import current_question
from grawantura.hostdashboard.drivers.queries import current_view
from grawantura.hostdashboard.drivers.queries import list_unused_questions
from grawantura.hostdashboard.drivers.tables import View
from grawantura.main.testing import DbTest
from grawantura.plays.drivers.commands import create_play
from grawantura.questions.drivers.commands import create_question


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


@DbTest
def test_current_money_when_empty(testdb):
    play_id = uuid4()
    assert current_money(play_id, db=testdb) == {"money_pool": 0}


@DbTest
def test_current_money_when_only_init_money(testdb):
    play_id = uuid4()
    team1_id = uuid4().hex
    team2_id = uuid4().hex
    init_money(
        play_id,
        {
            team1_id: 100,
            team2_id: 200,
        },
        db=testdb,
    )
    assert current_money(play_id, db=testdb) == {
        "money_pool": 0,
        team1_id: 100,
        team2_id: 200,
    }


@DbTest
def test_current_money_when_auction_end(testdb):
    play_id = uuid4()
    team1_id = uuid4().hex
    team2_id = uuid4().hex
    team3_id = uuid4().hex
    init_money(
        play_id,
        {
            team1_id: 100,
            team2_id: 200,
            team3_id: 300,
        },
        db=testdb,
    )
    end_auction(
        play_id,
        {
            team1_id: 50,
            team2_id: 45,
            team3_id: 0,
        },
        db=testdb,
    )
    assert current_money(play_id, db=testdb) == {
        "money_pool": 95,
        team1_id: 50,
        team2_id: 155,
        team3_id: 300,
    }

@DbTest
def test_current_money_when_hint_bought(testdb):
    play_id = uuid4()
    team1_id = uuid4().hex
    team2_id = uuid4().hex
    team3_id = uuid4().hex
    init_money(
        play_id,
        {
            team1_id: 100,
            team2_id: 200,
            team3_id: 300,
        },
        db=testdb,
    )
    end_auction(
        play_id,
        {
            team1_id: 50,
            team2_id: 45,
            team3_id: 0,
        },
        db=testdb,
    )
    hint_bought(
        play_id,
        UUID(team1_id),
        50,
        db=testdb,
    )
    assert current_money(play_id, db=testdb) == {
        "money_pool": 95,
        team1_id: 0,
        team2_id: 155,
        team3_id: 300,
    }

@DbTest
def test_current_money_when_success_answer(testdb):
    play_id = uuid4()
    team1_id = uuid4().hex
    team2_id = uuid4().hex
    team3_id = uuid4().hex
    init_money(
        play_id,
        {
            team1_id: 100,
            team2_id: 200,
            team3_id: 300,
        },
        db=testdb,
    )
    end_auction(
        play_id,
        {
            team1_id: 50,
            team2_id: 45,
            team3_id: 0,
        },
        db=testdb,
    )
    answer(
        play_id,
        True,
        db=testdb,
    )
    assert current_money(play_id, db=testdb) == {
        "money_pool": 0,
        team1_id: 145,
        team2_id: 155,
        team3_id: 300,
    }

@DbTest
def test_current_money_when_fail_answer(testdb):
    play_id = uuid4()
    team1_id = uuid4().hex
    team2_id = uuid4().hex
    team3_id = uuid4().hex
    init_money(
        play_id,
        {
            team1_id: 100,
            team2_id: 200,
            team3_id: 300,
        },
        db=testdb,
    )
    end_auction(
        play_id,
        {
            team1_id: 50,
            team2_id: 45,
            team3_id: 0,
        },
        db=testdb,
    )
    answer(
        play_id,
        False,
        db=testdb,
    )
    assert current_money(play_id, db=testdb) == {
        "money_pool": 95,
        team1_id: 50,
        team2_id: 155,
        team3_id: 300,
    }
