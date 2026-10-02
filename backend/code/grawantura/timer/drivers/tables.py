from sqlalchemy import UUID
from sqlalchemy import Column
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

from grawantura.main.tables import SqlTable


class TimerTable(SqlTable):
    __tablename__ = "timers"
    __table_args__ = (UniqueConstraint("play_id"),)

    play_id = Column(UUID, nullable=False)
    status = Column(String, nullable=True)
    end_time = Column(BigInteger, nullable=True)
