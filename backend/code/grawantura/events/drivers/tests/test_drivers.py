from datetime import datetime
from datetime import timedelta
from uuid import uuid4

from grawantura.events.drivers.commands import add_event
from grawantura.events.drivers.queries import get_events
from grawantura.main.testing import DbTest


@DbTest
def test_events_empty(testdb):
    now = datetime.now()
    assert list(get_events(now, db=testdb)) == []


@DbTest
def test_events_before(testdb):
    now = datetime.now()
    event_id = uuid4()
    payload = {"payload": 1}
    add_event(
        payload,
        event_id,
        now,
        db=testdb,
    )
    assert list(get_events(now - timedelta(seconds=1), db=testdb)) == [
        {
            "created_at": now,
            "payload": payload,
        }
    ]


@DbTest
def test_events_at_time(testdb):
    now = datetime.now()
    event_id = uuid4()
    payload = {"payload": 1}
    add_event(
        payload,
        event_id,
        now,
        db=testdb,
    )
    assert list(get_events(now, db=testdb)) == [
        {
            "created_at": now,
            "payload": payload,
        }
    ]


@DbTest
def test_events_after(testdb):
    now = datetime.now()
    event_id = uuid4()
    payload = {"payload": 1}
    add_event(
        payload,
        event_id,
        now,
        db=testdb,
    )
    assert list(get_events(now + timedelta(seconds=1), db=testdb)) == []
