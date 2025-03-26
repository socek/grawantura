from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String

from grawantura.main.tables import SqlTable


class InstanceTable(SqlTable):
    __tablename__ = "instances"

    name = Column(String, nullable=True)
    game_id = Column(ForeignKey("games.id"))
