from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String

from grawantura.main.tables import SqlTable


class UserTable(SqlTable):
    __tablename__ = "app_users"

    email = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
