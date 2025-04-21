from typing import Optional
from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from grawantura.main.globals import Query
from grawantura.questions.drivers.tables import QuestionTable


@Query
def get_questions(
    game_id: UUID = None,
    db: Session = None,
) -> list[dict]:
    stmt = (
        select(QuestionTable)
        .order_by(QuestionTable.created_at.asc())
        .filter(
            QuestionTable.game_id == game_id,
            QuestionTable.is_deleted.isnot(True),
        )
    )
    result = db.execute(stmt)
    for obj in result:
        yield obj[0]._asdict()


@Query
def get_question_by_id(
    question_id: UUID = None,
    db: Session = None,
) -> Optional[dict]:
    stmt = (
        select(QuestionTable)
        .order_by(QuestionTable.created_at.asc())
        .filter(
            QuestionTable.id == question_id,
            QuestionTable.is_deleted.isnot(True),
        )
    )
    obj = db.execute(stmt).first()
    if obj:
        return obj[0]._asdict()
