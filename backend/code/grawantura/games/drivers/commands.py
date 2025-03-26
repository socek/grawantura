from datetime import datetime
from uuid import UUID
from uuid import uuid4

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from grawantura.games.drivers.tables import GameTable
from grawantura.main.globals import Command


@Command
async def create_game(
    name: str,
    game_id: UUID = None,
    now: datetime = None,
    db: AsyncSession = None,
) -> list:
    game_id = game_id or uuid4()
    now = now or datetime.now()
    row = {
        "id": game_id,
        "name": name,
        "created_at": now,
        "updated_at": now,
    }
    stmt = insert(GameTable).values([row])
    await db.execute(stmt)
