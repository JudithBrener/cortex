import json
from json import JSONDecodeError

import pytest

from tests.saver.in_memory_db import InMemoryCortexDao
from cortex.saver.saver import Saver
from tests.saver.test_data import _TEST_TOPIC, _USER, _TIMESTAMP, _TEST_DATA, _MESSAGE, _REAL_MESSAGE, _USER_ID


@pytest.fixture
def db():
    return InMemoryCortexDao()


@pytest.fixture
def saver(db):
    return Saver(db)


def test_input_not_json(saver):
    with pytest.raises(JSONDecodeError) as e:
        saver.save(_TEST_TOPIC, "invalid json data")

    assert 'JSONDecodeError' in str(e.typename)


def test_input_without_user_info(saver):
    with pytest.raises(KeyError):
        saver.save(_TEST_TOPIC, json.dumps({"datetime": _TIMESTAMP, _TEST_TOPIC: _TEST_DATA}))


def test_input_without_timestamp(saver):
    with pytest.raises(KeyError):
        saver.save(_TEST_TOPIC, json.dumps({"user": _USER, _TEST_TOPIC: _TEST_DATA}))


def test_input_without_topic_data(saver):
    with pytest.raises(KeyError):
        saver.save(_TEST_TOPIC, json.dumps({"user": _USER, "datetime": _TIMESTAMP}))

    with pytest.raises(KeyError):
        saver.save("pose", json.dumps(_MESSAGE))


def test_save_user_info(saver, db):
    saver.save(_TEST_TOPIC, json.dumps(_MESSAGE))
    assert _USER_ID in db.users


def test_save_topic_data(saver, db):
    saver.save(_TEST_TOPIC, json.dumps(_MESSAGE))
    assert_snapshot_data(db, _USER_ID, _TIMESTAMP, _TEST_TOPIC, _TEST_DATA)


def test_save_real_message(saver, db):
    topic = "pose"
    saver.save(topic, _REAL_MESSAGE)
    message = json.loads(_REAL_MESSAGE)
    assert_snapshot_data(db, message["user"]["user_id"], message["datetime"], topic, json.loads('{"data": [1, 1]}'))


def assert_snapshot_data(db, user_id, timestamp, topic, topic_data):
    snapshot_key = db.get_snapshot_key(user_id, timestamp)
    assert snapshot_key in db.snapshots
    snapshot = db.snapshots[snapshot_key]
    assert topic in snapshot
    assert topic_data == snapshot[topic]
    assert user_id == snapshot["user_id"]
    assert timestamp == snapshot["datetime"]
