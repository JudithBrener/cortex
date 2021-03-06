import copy

import pymongo
import pytest

from tests.saver.test_data import _TEST_TOPIC, _USER, _TIMESTAMP, _TEST_DATA, _USER_ID, \
    _POSE_DATA


def test_mongo_client(mongo_client):
    response = mongo_client.irkkt.command("ping")
    assert response == {"ok": 1.0}


def test_create_user(db, users):
    user_id = db.create_or_update_user(_USER)
    user_in_db = users.find_one({"user_id": _USER_ID})
    assert_db_object_equals(user_in_db, _USER)
    assert user_id == _USER_ID


def test_update_user(db, users):
    user_id1 = db.create_or_update_user(_USER)
    changed_user = copy.deepcopy(_USER)
    changed_user["username"] = "name changed"
    user_id2 = db.create_or_update_user(changed_user)
    user_in_db = users.find_one({"user_id": _USER_ID})
    assert_db_object_equals(user_in_db, changed_user)
    assert user_id1 == _USER_ID
    assert user_id2 == _USER_ID


def test_user_id_is_unique(db, users):
    users.insert(_USER, manipulate=False)
    with pytest.raises(pymongo.errors.DuplicateKeyError):
        users.insert({"user_id": _USER_ID, "username": 'different name'}, manipulate=False)


def test_create_snapshot(db, snapshots):
    snapshot_id = db.create_or_update_snapshot(_USER_ID, _TIMESTAMP, _TEST_TOPIC, _TEST_DATA)
    snapshot_in_db = snapshots.find_one({"user_id": _USER_ID, "datetime": _TIMESTAMP})
    assert_db_object_equals(snapshot_in_db, {"user_id": _USER_ID, "datetime": _TIMESTAMP,
                                             _TEST_TOPIC: _TEST_DATA})
    assert snapshot_id == db.get_snapshot_key(_USER_ID, _TIMESTAMP)


def test_update_snapshot(db, snapshots):
    db.create_or_update_snapshot(_USER_ID, _TIMESTAMP, _TEST_TOPIC, _TEST_DATA)
    db.create_or_update_snapshot(_USER_ID, _TIMESTAMP, "pose", _POSE_DATA)
    snapshot_in_db = snapshots.find_one({"user_id": _USER_ID, "datetime": _TIMESTAMP})
    assert_db_object_equals(snapshot_in_db,
                            {"user_id": _USER_ID, "datetime": _TIMESTAMP,
                             _TEST_TOPIC: _TEST_DATA,
                             "pose": _POSE_DATA})


def test_snapshots_uniqueness(db, snapshots):
    snapshots.insert(user_data(_TIMESTAMP), manipulate=False)
    with pytest.raises(pymongo.errors.DuplicateKeyError):
        snapshots.insert(user_data(_TIMESTAMP), manipulate=False)
    snapshots.insert(user_data(_TIMESTAMP + 1), manipulate=False)


def user_data(timestamp):
    return {"user_id": _USER_ID, "datetime": timestamp, "topic": "data"}


def assert_db_object_equals(db_object, expected_object):
    assert db_object is not None
    del db_object["_id"]  # delete the auto generated id
    assert db_object == expected_object
