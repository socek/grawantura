from datetime import datetime
from uuid import UUID
from uuid import uuid4

from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.orm import Session

from grawantura.auth.drivers.hashpassword import hash_password
from grawantura.auth.drivers.tables import UserTable
from grawantura.main.globals import Command


@Command
def create_user(
    email: str,
    password: str,
    user_id: UUID = None,
    now: datetime = None,
    db: Session = None,
):
    user_id = user_id or uuid4()
    now = now or datetime.now()
    row = {
        "id": user_id,
        "email": email,
        "password": hash_password(password),
        "created_at": now,
        "updated_at": now,
    }
    stmt = insert(UserTable).values([row])
    db.execute(stmt)


@Command
def update_user(
    user_id: UUID,
    email: str = None,
    password: str = None,
    now: datetime = None,
    db: Session = None,
):
    now = now or datetime.now()
    row = {
        "updated_at": now,
    }
    if email:
        row["email"] = email
    if password:
        row["password"] = hash_password(password)
    stmt = update(UserTable).where(UserTable.id == user_id).values(**row)
    db.execute(stmt)


@Command
def delete_user(
    user_id: UUID,
    db: Session = None,
):
    stmt = update(UserTable).where(UserTable.id == user_id).values({"is_deleted": True})
    db.execute(stmt)
