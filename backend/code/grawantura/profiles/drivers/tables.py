from sqlalchemy import Column
from sqlalchemy import String

from grawantura.main.tables import SqlTable


class ProfileTable(SqlTable):
    __tablename__ = "profiles"

    username = Column(String, nullable=True)
