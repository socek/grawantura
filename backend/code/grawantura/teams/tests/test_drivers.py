from datetime import datetime
from datetime import timedelta
from uuid import uuid4

from grawantura.main.testing import DbTest
from grawantura.teams.drivers.commands import create_team
from grawantura.teams.drivers.commands import delete_team
from grawantura.teams.drivers.commands import update_team
from grawantura.teams.drivers.queries import get_team_by_id
from grawantura.teams.drivers.queries import get_teams


@DbTest
def test_creating(testdb):
    team_id = uuid4()
    now = datetime.now()
    create_team("My team", team_id=team_id, now=now, db=testdb)
    assert get_team_by_id(team_id, db=testdb) == {
        "id": team_id,
        "name": "My team",
        "created_at": now,
        "updated_at": now,
        "is_deleted": None,
        "play_id": None,
    }


@DbTest
def test_empty(testdb):
    assert get_team_by_id(uuid4(), db=testdb) is None


@DbTest
def test_listening(testdb):
    team_id = uuid4()
    play_id = uuid4()
    now = datetime.now()
    create_team("My team", team_id=team_id, play_id=play_id, now=now, db=testdb)
    assert get_teams(play_id, db=testdb) == [
        {
            "id": team_id,
            "name": "My team",
            "created_at": now,
            "updated_at": now,
            "is_deleted": None,
            "play_id": play_id,
        }
    ]


@DbTest
def test_deleted(testdb):
    team_id = uuid4()
    play_id = uuid4()
    now = datetime.now()
    create_team("My team", play_id=play_id, team_id=team_id, now=now, db=testdb)

    delete_team(team_id)

    assert get_team_by_id(team_id, db=testdb) is None
    assert get_teams(play_id, db=testdb) == []


@DbTest
def test_updating(testdb):
    team_id = uuid4()
    play_id = uuid4()
    now = datetime.now()

    after = datetime.now() + timedelta(seconds=1)
    new_play_id = uuid4()

    create_team("My team", team_id=team_id, play_id=play_id, now=now, db=testdb)

    update_team(team_id, "New Name", play_id=new_play_id, now=after, db=testdb)

    assert get_team_by_id(team_id, db=testdb) == {
        "id": team_id,
        "name": "New Name",
        "created_at": now,
        "updated_at": after,
        "is_deleted": None,
        "play_id": new_play_id,
    }


@DbTest
def test_updating_when_empty(testdb):
    team_id = uuid4()
    play_id = uuid4()
    now = datetime.now()

    create_team("My team", team_id=team_id, play_id=play_id, now=now, db=testdb)

    update_team(team_id)

    assert get_team_by_id(team_id, db=testdb) == {
        "id": team_id,
        "name": "My team",
        "created_at": now,
        "updated_at": now,
        "is_deleted": None,
        "play_id": play_id,
    }
