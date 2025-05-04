from datetime import datetime
from typing import Any
from typing import Optional
from uuid import UUID
from uuid import uuid4

from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.orm import Session

from grawantura.main.globals import Command
from grawantura.plays.drivers.tables import PlayTable


@Command
def create_play(
    name: str,
    game_id: Optional[UUID] = None,
    play_id: Optional[UUID] = None,
    now: Optional[datetime] = None,
    db: Optional[Session] = None,
):
    assert db
    play_id = play_id or uuid4()
    now = now or datetime.now()
    row: dict[str, Any] = {
        "id": play_id,
        "name": name,
        "game_id": game_id,
        "created_at": now,
        "updated_at": now,
    }
    stmt = insert(PlayTable).values([row])
    db.execute(stmt)


@Command
def update_play(
    play_id: UUID,
    name: Optional[str] = None,
    game_id: Optional[UUID] = None,
    now: Optional[datetime] = None,
    db: Optional[Session] = None,
):
    assert db
    now = now or datetime.now()
    row: dict[str, Any] = {
        "name": name,
        "game_id": game_id,
    }
    filtered = {k: v for k, v in row.items() if v is not None}
    if not filtered:
        return
    filtered["updated_at"] = now
    stmt = update(PlayTable)
    stmt = stmt.where(PlayTable.id == play_id)
    stmt = stmt.values(**filtered)
    db.execute(stmt)


@Command
def delete_play(
    play_id: UUID,
    db: Optional[Session] = None,
):
    assert db
    stmt = update(PlayTable)
    stmt = stmt.where(PlayTable.id == play_id)
    stmt = stmt.values({"is_deleted": True})
    db.execute(stmt)
