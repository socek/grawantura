from sqlalchemy import UUID
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String

from grawantura.main.tables import SqlTable


class PlayTable(SqlTable):
    __tablename__ = "plays"

    name = Column(String, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    game_id = Column(UUID, nullable=True)
