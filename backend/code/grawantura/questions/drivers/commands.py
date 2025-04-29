from datetime import datetime
from typing import Optional
from uuid import UUID
from uuid import uuid4

from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.orm import Session

from grawantura.main.globals import Command
from grawantura.questions.drivers.tables import QuestionTable


@Command
def create_question(
    question: str,
    answer: str,
    hints: str,
    game_id: UUID,
    question_id: UUID = None,
    now: datetime = None,
    db: Session = None,
):
    game_id = game_id or uuid4()
    question_id = question_id or uuid4()
    now = now or datetime.now()
    row = {
        "id": question_id,
        "question": question,
        "answer": answer,
        "hints": hints,
        "game_id": game_id,
        "created_at": now,
        "updated_at": now,
    }
    stmt = insert(QuestionTable).values([row])
    db.execute(stmt)


@Command
def update_question(
    question_id: UUID,
    question: Optional[str] = None,
    answer: Optional[str] = None,
    hints: Optional[str] = None,
    game_id: Optional[UUID] = None,
    now: Optional[datetime] = None,
    db: Optional[Session] = None,
):
    now = now or datetime.now()
    row = {
        "question": question,
        "answer": answer,
        "hints": hints,
        "game_id": game_id,
    }
    filtered = {k: v for k, v in row.items() if v is not None}
    if not filtered:
        return
    filtered["updated_at"] = now
    stmt = update(QuestionTable).where(QuestionTable.id == question_id).values(**filtered)
    db.execute(stmt)


@Command
def delete_question(
    question_id: UUID,
    db: Session = None,
):
    stmt = (
        update(QuestionTable).where(QuestionTable.id == question_id).values({"is_deleted": True})
    )
    db.execute(stmt)
