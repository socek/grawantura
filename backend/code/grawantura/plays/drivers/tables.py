from enum import Enum

from sqlalchemy import UUID
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import String

from grawantura.main.tables import SqlTable


class View(Enum):
    scoreboard = "scoreboard"
    question = "question"


class EventTypenames(Enum):
    init_money = "init money"
    question_draw = "question draw"
    team_auction = "team auction"
    hint_bought = "hint bought"
    hint_used = "hint used"
    answer_success = "answer success"
    answer_fail = "answer fail"
    remove_money = "remove money"
    change_view = "change view"


class PlayTable(SqlTable):
    __tablename__ = "plays"

    name = Column(String, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    game_id = Column(UUID, nullable=True)


class PlayEventTable(SqlTable):
    __tablename__ = "play_events"
    __table_args__ = (Index("play_events_play_id", "play_id", "typename"),)

    play_id = Column(UUID, nullable=True)
    team_id = Column(UUID, nullable=True)
    question_id = Column(UUID, nullable=True)
    typename = Column(String, nullable=True)
    money = Column(Integer, nullable=True)
    view_name = Column(String, nullable=True)
