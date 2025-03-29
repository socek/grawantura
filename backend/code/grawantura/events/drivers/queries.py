from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from grawantura.events.drivers.tables import EventTable
from grawantura.main.globals import Query


@Query
def get_events(
    fromtime: datetime,
    db: Session = None,
) -> list:
    stmt = select(
        EventTable.created_at,
        EventTable.payload,
    ).filter(
        EventTable.created_at >= fromtime,
    )
    result = db.execute(stmt)
    return [row._asdict() for row in result]
