from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from grawantura.main.tables import SqlTable


class GameTable(SqlTable):
    __tablename__ = "games"

    name = Column(String, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    user_id = Column(UUID(as_uuid=True), nullable=True)
