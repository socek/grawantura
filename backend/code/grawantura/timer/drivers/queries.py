from typing import Optional
from grawantura.timer.models import TimerStatus
from grawantura.timer.drivers.tables import TimerTable
from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from grawantura.main.globals import Query



@Query
def get_time_for_play(
    play_id: UUID,
    db: Optional[Session] = None,
) -> dict:
    assert db
    stmt = select(TimerTable).filter(
        TimerTable.play_id == play_id,
    )
    result = db.execute(stmt)
    obj = result.first()
    if obj:
        return obj[0]._asdict()
    else:
        return {
            "id": None,
            "play_id": play_id,
            "end_time": None,
            "status": TimerStatus.stopped,
        }
