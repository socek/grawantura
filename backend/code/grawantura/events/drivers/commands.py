from datetime import datetime
from typing import Optional
from uuid import UUID
from uuid import uuid4

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from grawantura.events.drivers.tables import EventTable
from grawantura.main.globals import Command
from grawantura.main.web import sanitize


@Command
def add_event(
    payload: dict,
    event_id: Optional[UUID] = None,
    now: Optional[datetime] = None,
    db: Session = None,
):
    now = now or datetime.now()
    row = {
        "id": uuid4(),
        "created_at": now,
        "updated_at": now,
        "payload": sanitize(payload),
    }
    ic(row)
    stmt = insert(EventTable).values([row])
    db.execute(stmt)
