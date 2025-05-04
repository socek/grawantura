from enum import Enum

from sqlalchemy import JSON
from sqlalchemy import UUID
from sqlalchemy import Column
from sqlalchemy import Index
from sqlalchemy import String

from grawantura.main.tables import SqlTable


class View(Enum):
    scoreboard = "scoreboard"
    question = "question"


class EventTypenames(Enum):
    question_draw = "question draw"
    change_view = "change view"
    end_auction = "end auction"
    init_money = "init money"
    hint_bought = "hint bought"
    hint_used = "hint used"
    answer = "answer"


class PlayEventTable(SqlTable):
    __tablename__ = "play_events"
    __table_args__ = (Index("play_events_play_id", "play_id", "typename"),)

    play_id = Column(UUID, nullable=True)
    question_id = Column(UUID, nullable=True)
    typename = Column(String, nullable=True)
    payload = Column(JSON, nullable=True)
