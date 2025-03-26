from sqlalchemy import Column
from sqlalchemy import String

from grawantura.main.tables import SqlTable


class GameTable(SqlTable):
    __tablename__ = "games"

    name = Column(String, nullable=True)
