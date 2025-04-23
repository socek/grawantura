from datetime import datetime
from typing import Any
from typing import Optional
from uuid import UUID
from uuid import uuid4

from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.orm import Session

from grawantura.main.globals import Command
from grawantura.teams.drivers.tables import TeamTable


@Command
def create_team(
    name: str,
    play_id: Optional[UUID] = None,
    team_id: Optional[UUID] = None,
    now: Optional[datetime] = None,
    db: Optional[Session] = None,
):
    assert db
    team_id = team_id or uuid4()
    now = now or datetime.now()
    row: dict[str, Any] = {
        "id": team_id,
        "name": name,
        "play_id": play_id,
        "created_at": now,
        "updated_at": now,
    }
    stmt = insert(TeamTable).values([row])
    db.execute(stmt)


@Command
def update_team(
    team_id: UUID,
    name: Optional[str] = None,
    play_id: Optional[UUID] = None,
    now: Optional[datetime] = None,
    db: Optional[Session] = None,
):
    assert db
    now = now or datetime.now()
    row: dict[str, Any] = {
        "name": name,
        "play_id": play_id,
    }
    filtered = {k: v for k, v in row.items() if v is not None}
    if not filtered:
        return
    filtered["updated_at"] = now
    stmt = update(TeamTable)
    stmt = stmt.where(TeamTable.id == team_id)
    stmt = stmt.values(**filtered)
    db.execute(stmt)


@Command
def delete_team(
    team_id: UUID,
    db: Optional[Session] = None,
):
    assert db
    stmt = update(TeamTable)
    stmt = stmt.where(TeamTable.id == team_id)
    stmt = stmt.values({"is_deleted": True})
    db.execute(stmt)
