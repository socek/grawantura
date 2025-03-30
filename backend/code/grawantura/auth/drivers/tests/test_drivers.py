from datetime import datetime
from datetime import timedelta
from uuid import uuid4

from grawantura.auth.drivers.commands import create_user
from grawantura.auth.drivers.commands import delete_user
from grawantura.auth.drivers.commands import update_user
from grawantura.auth.drivers.hashpassword import hash_password
from grawantura.auth.drivers.queries import get_user_by_email
from grawantura.auth.drivers.queries import validate_user
from grawantura.main.testing import DbTest


def test_hash_password():
    assert (
        hash_password("my password", {"salt": b"my salt"})
        == "320887b3816e92971323a88ba115ccda2c87df60ec939a893e16a21dae89a37a9b462c9a13d76d62ae60c7ce746c59d81a9689118bb426749fdec10a571c5d30"
    )


@DbTest
def test_creating(testdb):
    user_id = uuid4()
    now = datetime.now()
    email = "email@email.com"
    create_user(email, "password", user_id=user_id, now=now, db=testdb)
    assert get_user_by_email(email, db=testdb) == {
        "id": user_id,
        "email": email,
        "password": hash_password("password"),
        "created_at": now,
        "updated_at": now,
        "is_deleted": None,
    }


@DbTest
def test_empty(testdb):
    assert get_user_by_email("email@email.com", db=testdb) is None


@DbTest
def test_deleted(testdb):
    user_id = uuid4()
    now = datetime.now()
    email = "email@email.com"
    password = "password1"
    create_user(email, password, user_id=user_id, now=now, db=testdb)

    delete_user(user_id)

    assert get_user_by_email(email, db=testdb) is None


@DbTest
def test_updating(testdb):
    user_id = uuid4()
    now = datetime.now()
    email = "email@email.com"
    after = datetime.now() + timedelta(seconds=1)
    create_user(email, "password", user_id=user_id, now=now, db=testdb)

    update_user(user_id, "New Name", "New Password", after, db=testdb)

    assert get_user_by_email("New Name", db=testdb) == {
        "id": user_id,
        "email": "New Name",
        "password": hash_password("New Password"),
        "created_at": now,
        "updated_at": after,
        "is_deleted": None,
    }
