from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from grawantura.games.drivers.tables import GameTable
from grawantura.main.globals import Query


@Query
async def get_game_by_id(
    game_id: UUID,
    db: AsyncSession = None,
) -> Optional[dict]:
    stmt = select(GameTable).filter(
        GameTable.id == game_id,
    )
    result = db.execute(stmt)
    obj = (await result).first()
    if obj:
        return obj[0]._asdict()


@Query
async def get_games(
    db: AsyncSession = None,
) -> list:
    stmt = select(GameTable)
    result = db.execute(stmt)
    elements = []
    for game in await result:
        elements.append(game[0]._asdict())
    return elements
