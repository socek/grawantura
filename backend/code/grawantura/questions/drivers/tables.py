from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String

from grawantura.main.tables import SqlTable


class QuestionTable(SqlTable):
    __tablename__ = "questions"

    question = Column(String, nullable=True)
    answer = Column(String, nullable=True)
    hints = Column(String, nullable=True)
    game_id = Column(ForeignKey("games.id"))
