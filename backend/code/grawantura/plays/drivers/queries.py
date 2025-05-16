from typing import Optional
from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from grawantura.games.drivers.tables import GameTable
from grawantura.main.globals import Query
from grawantura.plays.drivers.tables import PlayTable


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
def get_game_id(
    play_id: UUID,
    db: Optional[Session] = None,
) -> Optional[UUID]:
    assert db
    stmt = (
        select(PlayTable.game_id)
        .join(GameTable, PlayTable.game_id == GameTable.id)
        .filter(
            GameTable.is_deleted.isnot(True),
            PlayTable.id == play_id,
        )
    )
    obj = db.execute(stmt).first()
    if obj and obj[0]:
        return obj[0]
