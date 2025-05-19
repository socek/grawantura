from datetime import datetime
from typing import Any
from typing import Optional
from uuid import UUID
from uuid import uuid4

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import Session

from grawantura.hostdashboard.drivers import queries
from grawantura.hostdashboard.drivers.tables import EventTypenames
from grawantura.hostdashboard.drivers.tables import PlayEventTable
from grawantura.hostdashboard.drivers.tables import View
from grawantura.main.globals import Command
from grawantura.plays.drivers.tables import PlayTable
from grawantura.questions.drivers.tables import QuestionTable


@Command
def draw_question(
    play_id: UUID,
    question_id: UUID,
    event_id: Optional[UUID] = None,
    now: Optional[datetime] = None,
    db: Optional[Session] = None,
):
    assert db
    event_id = event_id or uuid4()
    now = now or datetime.now()
    row = {
        "id": event_id,
        "created_at": now,
        "updated_at": now,
        "play_id": play_id,
        "typename": EventTypenames.question_draw.value,
        "question_id": question_id,
    }
    stmt = insert(PlayEventTable).values([row])
    db.execute(stmt)


@Command
def change_view(
    play_id: UUID,
    view: View,
    event_id: Optional[UUID] = None,
    now: Optional[datetime] = None,
    db: Optional[Session] = None,
):
    assert db
    event_id = event_id or uuid4()
    now = now or datetime.now()
    row = {
        "id": event_id,
        "created_at": now,
        "updated_at": now,
        "play_id": play_id,
        "typename": EventTypenames.change_view.value,
        "payload": {
            "view_name": view.value,
        },
    }
    stmt = insert(PlayEventTable).values([row])
    db.execute(stmt)


@Command
def init_money(
    play_id: UUID,
    payload: dict[str, int],
    event_id: Optional[UUID] = None,
    now: Optional[datetime] = None,
    db: Optional[Session] = None,
):
    assert db
    event_id = event_id or uuid4()
    now = now or datetime.now()
    question_id_stmt = queries.get_current_question_query(
        select(QuestionTable.id),
        play_id,
    ).scalar_subquery()
    row = {
        "id": event_id,
        "created_at": now,
        "updated_at": now,
        "play_id": play_id,
        "typename": EventTypenames.init_money.value,
        "question_id": question_id_stmt,
        "payload": payload,
    }
    stmt = insert(PlayEventTable).values([row])
    db.execute(stmt)


@Command
def end_auction(
    play_id: UUID,
    payload: dict,
    event_id: Optional[UUID] = None,
    now: Optional[datetime] = None,
    db: Optional[Session] = None,
):
    assert db
    event_id = event_id or uuid4()
    now = now or datetime.now()
    question_id_stmt = queries.get_current_question_query(
        select(QuestionTable.id),
        play_id,
    ).scalar_subquery()
    row = {
        "id": event_id,
        "created_at": now,
        "updated_at": now,
        "play_id": play_id,
        "typename": EventTypenames.end_auction.value,
        "question_id": question_id_stmt,
        "payload": payload,
    }
    stmt = insert(PlayEventTable).values([row])
    db.execute(stmt)


@Command
def hint(
    play_id: UUID,
    change: dict,
    money: dict,
    event_id: Optional[UUID] = None,
    now: Optional[datetime] = None,
    db: Optional[Session] = None,
):
    assert db
    event_id = event_id or uuid4()
    now = now or datetime.now()
    question_id_stmt = queries.get_current_question_query(
        select(QuestionTable.id),
        play_id,
    ).scalar_subquery()
    row = {
        "id": event_id,
        "created_at": now,
        "updated_at": now,
        "play_id": play_id,
        "typename": EventTypenames.hint.value,
        "question_id": question_id_stmt,
        "payload": {
            "change": change,
            "money": money,
        },
    }
    stmt = insert(PlayEventTable).values([row])
    db.execute(stmt)


@Command
def answer(
    play_id: UUID,
    success: bool,
    event_id: Optional[UUID] = None,
    now: Optional[datetime] = None,
    db: Optional[Session] = None,
):
    assert db
    event_id = event_id or uuid4()
    now = now or datetime.now()
    question_id_stmt = queries.get_current_question_query(
        select(QuestionTable.id),
        play_id,
    ).scalar_subquery()
    row = {
        "id": event_id,
        "created_at": now,
        "updated_at": now,
        "play_id": play_id,
        "typename": EventTypenames.answer.value,
        "question_id": question_id_stmt,
        "payload": {"success": success},
    }
    stmt = insert(PlayEventTable).values([row])
    db.execute(stmt)


@Command
def delete_event(
    play_id: UUID,
    event_id: UUID,
    db: Optional[Session] = None,
):
    stmt = (
        update(PlayEventTable)
        .where(PlayEventTable.id == event_id, PlayEventTable.play_id == play_id)
        .values({"is_deleted": True})
    )
    db.execute(stmt)
