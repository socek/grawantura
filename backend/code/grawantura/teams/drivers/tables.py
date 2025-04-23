from sqlalchemy import UUID
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String

from grawantura.main.tables import SqlTable


class TeamTable(SqlTable):
    __tablename__ = "teams"

    name = Column(String, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    play_id = Column(UUID, nullable=True)
