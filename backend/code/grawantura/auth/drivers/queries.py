from typing import Optional
from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from grawantura.auth.drivers.hashpassword import hash_password
from grawantura.auth.drivers.tables import UserTable
from grawantura.main.globals import Query


@Query
def get_user_by_email(
    email: str,
    db: Optional[Session] = None,
) -> Optional[dict]:
    stmt = select(UserTable).filter(UserTable.email == email, UserTable.is_deleted.isnot(True))
    obj = db.execute(stmt).first()
    if obj:
        return obj[0]._asdict()


@Query
def validate_user(
    email: str,
    password: str,
    db: Optional[Session] = None,
) -> Optional[UUID]:
    stmt = select(UserTable.id).filter(
        UserTable.email == email,
        UserTable.password == hash_password(password),
        UserTable.is_deleted.isnot(True),
    )
    obj = db.execute(stmt).first()
    if obj:
        return obj[0]


@Query
def validate_user_id(
    user_id: UUID,
    db: Optional[Session] = None,
) -> bool:
    stmt = select(UserTable.id).filter(
        UserTable.id == user_id,
        UserTable.is_deleted.isnot(True),
    )
    obj = db.execute(stmt).first()
    return obj is not None
