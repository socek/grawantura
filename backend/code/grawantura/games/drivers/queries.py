from typing import Optional
from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from grawantura.games.drivers.tables import GameTable
from grawantura.main.globals import Query


@Query
def get_game_by_id(
    game_id: UUID,
    db: Session = None,
) -> Optional[dict]:
    stmt = select(GameTable).filter(
        GameTable.id == game_id,
        GameTable.is_deleted.isnot(True),
    )
    result = db.execute(stmt)
    obj = result.first()
    if obj:
        return obj[0]._asdict()


@Query
def get_games(
    db: Session = None,
) -> list:
    stmt = (
        select(GameTable)
        .order_by(GameTable.created_at.asc())
        .filter(
            GameTable.is_deleted.isnot(True),
        )
    )
    result = db.execute(stmt)
    elements = []
    for game in result:
        elements.append(game[0]._asdict())
    return elements
