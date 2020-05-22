import copy

import pytest

from cortex.saver.mongo import MongoDB, _NAMESPACE
from tests.saver.test_data import _TEST_TOPIC, _USER, _TIMESTAMP, _TEST_DATA, _USER_ID, \
    _POSE_DATA


def test_mongo_client(mongo_client):
    response = mongo_client.irkkt.command("ping")
    assert response == {"ok": 1.0}


@pytest.fixture
def mongo_db(mongo_client):
    return MongoDB(mongo_client)


def test_created_instance(mongo_db):
    assert mongo_db is not None


def test_created_user(mongo_db, mongo_client):
    mongo_db.create_or_update_user(_USER)
    user_in_db = mongo_client[_NAMESPACE]["users"].find_one({"user_id": _USER_ID})
    assert_db_object_equals(user_in_db, _USER)


def test_update_user(mongo_db, mongo_client):
    mongo_db.create_or_update_user(_USER)
    changed_user = copy.deepcopy(_USER)
    changed_user["username"] = "name changed"
    mongo_db.create_or_update_user(changed_user)
    user_in_db = mongo_client[_NAMESPACE]["users"].find_one({"user_id": _USER_ID})
    assert_db_object_equals(user_in_db, changed_user)


def test_create_snapshot(mongo_db, mongo_client):
    mongo_db.create_or_update_snapshot(_USER_ID, _TIMESTAMP, _TEST_TOPIC, _TEST_DATA)
    snapshot_in_db = mongo_client[_NAMESPACE]["snapshots"].find_one({"user_id": _USER_ID, "datetime": _TIMESTAMP})
    assert_db_object_equals(snapshot_in_db, {"user_id": _USER_ID, "datetime": _TIMESTAMP,
                                             _TEST_TOPIC: _TEST_DATA})


def test_update_snapshot(mongo_db, mongo_client):
    mongo_db.create_or_update_snapshot(_USER_ID, _TIMESTAMP, _TEST_TOPIC, _TEST_DATA)
    mongo_db.create_or_update_snapshot(_USER_ID, _TIMESTAMP, "pose", _POSE_DATA)
    snapshot_in_db = mongo_client[_NAMESPACE]["snapshots"].find_one({"user_id": _USER_ID, "datetime": _TIMESTAMP})
    assert_db_object_equals(snapshot_in_db,
                            {"user_id": _USER_ID, "datetime": _TIMESTAMP,
                             _TEST_TOPIC: _TEST_DATA,
                             "pose": _POSE_DATA})


def assert_db_object_equals(db_object, expected_object):
    assert db_object is not None
    del db_object["_id"]  # delete the auto generated id
    assert db_object == expected_object
