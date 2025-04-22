from typing import Optional
from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from grawantura.main.globals import Query
from grawantura.play.drivers.tables import PlayTable


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
