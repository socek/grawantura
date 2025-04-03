from datetime import datetime
from datetime import timedelta
from unittest.mock import MagicMock
from uuid import uuid4

from grawantura.main.testing import DbTest
from grawantura.questions.drivers.commands import create_question
from grawantura.questions.drivers.commands import delete_question
from grawantura.questions.drivers.commands import update_question
from grawantura.questions.drivers.queries import get_question_by_id
from grawantura.questions.drivers.queries import get_questions


def base_row(prefix: str = "", game_id=None, now=None):
    now = now or datetime.now()
    game_id = game_id or uuid4()
    return {
        "question_id": uuid4(),
        "question": f"{prefix}question",
        "answer": f"{prefix}answer",
        "hints": f"{prefix}hints",
        "game_id": game_id,
        "now": now,
    }


@DbTest
def test_creating(testdb):
    row = base_row()
    create_question(db=testdb, **row)
    assert get_question_by_id(row["question_id"], db=testdb) == {
        "id": row["question_id"],
        "question": row["question"],
        "answer": row["answer"],
        "hints": row["hints"],
        "game_id": row["game_id"],
        "created_at": row["now"],
        "updated_at": row["now"],
        "is_deleted": None,
    }


@DbTest
def test_empty(testdb):
    assert list(get_questions(uuid4(), db=testdb)) == []


@DbTest
def test_listening(testdb):
    game_id = uuid4()
    row1 = base_row("A", game_id)
    row2 = base_row("B", game_id)
    row3 = base_row("C")
    create_question(db=testdb, **row1)
    create_question(db=testdb, **row2)
    create_question(db=testdb, **row3)
    question_ids = set([element["id"] for element in get_questions(game_id, db=testdb)])
    assert question_ids == set([row1["question_id"], row2["question_id"]])


@DbTest
def test_deleted(testdb):
    row = base_row()
    create_question(db=testdb, **row)
    delete_question(row["question_id"])
    assert get_question_by_id(row["question_id"], db=testdb) is None
    assert list(get_questions(row["game_id"], db=testdb)) == []


@DbTest
def test_updating(testdb):
    row = base_row()
    create_question(db=testdb, **row)

    after = datetime.now() + timedelta(seconds=1)
    updated_row = base_row("B_", now=after)
    del updated_row["question_id"]

    update_question(row["question_id"], db=testdb, **updated_row)

    assert get_question_by_id(row["question_id"], db=testdb) == {
        "id": row["question_id"],
        "question": updated_row["question"],
        "answer": updated_row["answer"],
        "hints": updated_row["hints"],
        "game_id": updated_row["game_id"],
        "created_at": row["now"],
        "updated_at": updated_row["now"],
        "is_deleted": None,
    }

@DbTest
def test_empty_updating(testdb):
    testdb = MagicMock()
    update_question(uuid4(), db=testdb)
    assert not testdb.execute.called
