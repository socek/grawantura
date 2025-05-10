from typing import Generator
from typing import Optional
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from grawantura.games.drivers.tables import GameTable
from grawantura.hostdashboard.drivers.tables import EventTypenames
from grawantura.hostdashboard.drivers.tables import PlayEventTable
from grawantura.hostdashboard.drivers.tables import View
from grawantura.main.globals import Query
from grawantura.plays.drivers.tables import PlayTable
from grawantura.questions.drivers.tables import QuestionTable


def get_current_question_query(select_stmt, play_id):
    return (
        select_stmt.join(GameTable, GameTable.id == QuestionTable.game_id)
        .join(PlayTable, PlayTable.game_id == GameTable.id)
        .join(
            PlayEventTable,
            and_(
                PlayEventTable.play_id == PlayTable.id,
                PlayEventTable.question_id == QuestionTable.id,
            ),
        )
        .filter(PlayTable.id == play_id)
        .order_by(PlayEventTable.created_at.desc())
        .limit(1)
    )


@Query
def list_unused_questions(
    play_id: UUID,
    db: Optional[Session] = None,
) -> list[UUID]:
    assert db
    stmt = (
        select(QuestionTable.id)
        .join(GameTable, GameTable.id == QuestionTable.game_id)
        .join(PlayTable, PlayTable.game_id == GameTable.id)
        .outerjoin(
            PlayEventTable,
            and_(
                PlayEventTable.play_id == PlayTable.id,
                PlayEventTable.question_id == QuestionTable.id,
            ),
        )
        .filter(
            PlayEventTable.id.is_(None),
            PlayTable.id == play_id,
            QuestionTable.is_deleted.isnot(True),
        )
    )

    return [obj.id for obj in db.execute(stmt)]


@Query
def current_question(
    play_id: UUID,
    db: Optional[Session] = None,
) -> Optional[dict]:
    assert db
    stmt = get_current_question_query(select(QuestionTable), play_id)
    obj = db.execute(stmt).first()
    if obj:
        return obj[0]._asdict()


@Query
def current_view(
    play_id: UUID,
    db: Optional[Session] = None,
) -> View:
    assert db
    stmt = (
        select(PlayEventTable.payload)
        .filter(
            PlayEventTable.play_id == play_id,
            PlayEventTable.typename == EventTypenames.change_view.value,
        )
        .order_by(PlayEventTable.created_at.desc())
        .limit(1)
    )
    obj = db.execute(stmt).first()

    if obj and obj[0]:
        ic(obj)
        return View(obj[0]["view_name"])

    return View.scoreboard


@Query
def current_money(
    play_id: UUID,
    db: Optional[Session] = None,
) -> dict:
    assert db
    stmt = (
        select(PlayEventTable.typename, PlayEventTable.payload)
        .filter(
            PlayEventTable.play_id == play_id,
            PlayEventTable.typename.in_(
                [
                    EventTypenames.init_money.value,
                    EventTypenames.end_auction.value,
                    EventTypenames.hint_bought.value,
                    EventTypenames.answer.value,
                ]
            ),
        )
        .order_by(PlayEventTable.created_at)
    )

    result = {
        "money_pool": 0,
    }
    last_auction_win = None
    for row in db.execute(stmt):
        if row.typename == EventTypenames.init_money.value:
            for key, value in row.payload.items():
                result[key] = result.get(key, 0) + value
        elif row.typename == EventTypenames.end_auction.value:
            last_auction_win = max(row.payload, key=row.payload.get)
            for key, value in row.payload.items():
                result[key] = result.get(key, 0) - value
                result["money_pool"] += value
        elif row.typename == EventTypenames.hint_bought.value:
            for key, value in row.payload.items():
                result[key] = result.get(key, 0) - value
        elif row.typename == EventTypenames.answer.value:
            if row.payload["success"]:
                result[last_auction_win] = result.get(last_auction_win, 0) + result["money_pool"]
                result["money_pool"] = 0
    return result


@Query
def play_events(
    play_id: UUID,
    db: Optional[Session] = None,
) -> Generator[dict]:
    assert db
    stmt = select(
        PlayEventTable.question_id,
        PlayEventTable.typename,
        PlayEventTable.payload,
        PlayEventTable.created_at,
    ).filter(
        PlayEventTable.play_id == play_id,
        PlayEventTable.typename == EventTypenames.init_money.value,
    )
    for row in db.execute(stmt):
        yield row._asdict()
