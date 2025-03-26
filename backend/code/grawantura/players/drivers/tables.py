from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String

from grawantura.main.tables import SqlTable


class PlayerTable(SqlTable):
    __tablename__ = "players"

    name = Column(String, nullable=True)
    instance_id = Column(ForeignKey("instances.id"))
