from datetime import datetime
from uuid import UUID
from uuid import uuid4

from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.orm import Session

from grawantura.games.drivers.tables import GameTable
from grawantura.main.globals import Command


@Command
def create_game(
    name: str,
    game_id: UUID = None,
    now: datetime = None,
    db: Session = None,
):
    game_id = game_id or uuid4()
    now = now or datetime.now()
    row = {
        "id": game_id,
        "name": name,
        "created_at": now,
        "updated_at": now,
    }
    stmt = insert(GameTable).values([row])
    db.execute(stmt)


@Command
def update_game(
    game_id: UUID,
    name: str,
    now: datetime = None,
    db: Session = None,
):
    now = now or datetime.now()
    row = {
        "name": name,
        "updated_at": now,
    }
    stmt = update(GameTable).where(GameTable.id == game_id).values(**row)
    db.execute(stmt)


@Command
def delete_game(
    game_id: UUID,
    db: Session = None,
):
    stmt = update(GameTable).where(GameTable.id == game_id).values({"is_deleted": True})
    db.execute(stmt)
