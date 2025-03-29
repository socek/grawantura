from sqlalchemy import JSON
from sqlalchemy import Column

from grawantura.main.tables import SqlTable


class EventTable(SqlTable):
    __tablename__ = "events"

    payload = Column(JSON, nullable=True)
