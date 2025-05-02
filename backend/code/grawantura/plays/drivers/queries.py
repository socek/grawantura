from typing import Optional
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from grawantura.games.drivers.tables import GameTable
from grawantura.main.globals import Query
from grawantura.plays.drivers.tables import PlayEventTable
from grawantura.plays.drivers.tables import PlayTable
from grawantura.plays.drivers.tables import View
from grawantura.questions.drivers.tables import QuestionTable


@Query
def get_play_by_id(
    play_id: UUID,
    db: Optional[Session] = None,
) -> Optional[dict]:
    assert db
    stmt = select(PlayTable).filter(
        PlayTable.id == play_id,
        PlayTable.is_deleted.isnot(True),
    )
    result = db.execute(stmt)
    obj = result.first()
    if obj:
        return obj[0]._asdict()


@Query
def get_plays(
    game_id: UUID,
    db: Optional[Session] = None,
) -> list[dict]:
    assert db
    stmt = (
        select(PlayTable)
        .order_by(PlayTable.created_at.asc())
        .filter(
            PlayTable.is_deleted.isnot(True),
            PlayTable.game_id == game_id,
        )
    )
    result = db.execute(stmt)
    return [row[0]._asdict() for row in result]


@Query
def has_access(
    user_id: UUID,
    play_id: UUID,
    db: Optional[Session] = None,
) -> bool:
    """
    Check if user hase access to the game.
    """
    assert db
    stmt = (
        select(GameTable.id)
        .join(PlayTable, PlayTable.game_id == GameTable.id)
        .filter(
            GameTable.user_id == user_id,
            GameTable.is_deleted.isnot(True),
            PlayTable.id == play_id,
        )
    )
    obj = db.execute(stmt).first()
    return True if obj else False


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
    stmt = (
        select(QuestionTable)
        .join(GameTable, GameTable.id == QuestionTable.game_id)
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
        select(PlayEventTable.view_name)
        .filter(PlayEventTable.play_id == play_id)
        .order_by(PlayEventTable.created_at.desc())
        .limit(1)
    )
    obj = db.execute(stmt).first()
    if obj:
        return View(obj[0])

    return View.scoreboard
