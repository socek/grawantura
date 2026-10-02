from datetime import datetime
from decimal import Decimal
from typing import Any
from typing import Optional
from uuid import UUID
from uuid import uuid4

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from grawantura.main.globals import Command
from grawantura.timer.drivers.tables import TimerTable
from grawantura.timer.models import TimerStatus
from grawantura.timer.models import get_now_ms


@Command
def start_timer(
    play_id: Optional[UUID],
    microseconds: int,
    db: Optional[Session] = None,
):
    assert db
    row_id = uuid4()
    end_time = get_now_ms() + microseconds

    row: dict[str, Any] = {
        "id": row_id,
        "play_id": play_id,
        "end_time": end_time,
        "status": TimerStatus.running,
    }
    stmt = (
        insert(TimerTable)
        .values(**row)
        .on_conflict_do_update(
            index_elements=["play_id"],
            set_={
                "end_time": end_time,
                "status": TimerStatus.running,
            },
        )
    )
    db.execute(stmt)


@Command
def stop_timer(
    play_id: Optional[UUID],
    db: Optional[Session] = None,
):
    assert db
    row_id = uuid4()

    row: dict[str, Any] = {
        "id": row_id,
        "play_id": play_id,
        "status": TimerStatus.stopped,
    }
    stmt = (
        insert(TimerTable)
        .values(**row)
        .on_conflict_do_update(
            index_elements=["play_id"],
            set_={
                "status": TimerStatus.stopped,
            },
        )
    )
    db.execute(stmt)
