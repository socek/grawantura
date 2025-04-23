from typing import Optional
from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from grawantura.main.globals import Query
from grawantura.teams.drivers.tables import TeamTable


@Query
def get_team_by_id(
    team_id: UUID,
    db: Optional[Session] = None,
) -> Optional[dict]:
    assert db
    stmt = select(TeamTable).filter(
        TeamTable.id == team_id,
        TeamTable.is_deleted.isnot(True),
    )
    result = db.execute(stmt)
    obj = result.first()
    if obj:
        return obj[0]._asdict()


@Query
def get_teams(
    play_id: UUID,
    db: Optional[Session] = None,
) -> list[dict]:
    assert db
    stmt = (
        select(TeamTable)
        .order_by(TeamTable.created_at.asc())
        .filter(
            TeamTable.is_deleted.isnot(True),
            TeamTable.play_id == play_id,
        )
    )
    result = db.execute(stmt)
    return [row[0]._asdict() for row in result]
