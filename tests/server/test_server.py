import json
import pathlib
import time

import pybson as bson
import pytest

from cortex.server.server import Server, set_server
from cortex.server.server import app as flask_app

# Sample Snapshot
_USER_ID = 1234
_USER = {"user_id": _USER_ID, "username": 'test user'}
_IMAGE_WITH_DATA = {"data": [1, 1, 1, 1, 1]}
_TIMESTAMP = 1456886665
_SNAPSHOT = {"datetime": _TIMESTAMP, "color_image": _IMAGE_WITH_DATA, "depth_image": _IMAGE_WITH_DATA}
_MESSAGE = {"user": _USER, "snapshot": _SNAPSHOT}

_FILE = 'test_file'


@pytest.fixture
def data_dir(tmp_path):
    return tmp_path


@pytest.fixture
def client(data_dir):
    def publish_method(message):
        with open(data_dir / _FILE, 'w') as f:
            f.write(message)

    set_server(Server(publish_method, str(data_dir)))
    app = flask_app
    with app.test_client() as client:
        time.sleep(0.1)
        yield client


def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'Server is up and running!'


def test_bad_request(client):
    response = client.put('/snapshot', data=bson.dumps({"user": {"malformed_user": 111}, "snapshot": _SNAPSHOT}))
    assert response.status_code == 400
    assert 'Invalid snapshot message' in str(response.data)


def test_bad_encoding(client):
    response = client.put('/snapshot', data=json.dumps({"user": {"malformed_user": 111}, "snapshot": _SNAPSHOT}))
    assert response.status_code == 400
    assert 'Invalid snapshot message' in str(response.data)


def test_mock_snapshot(client, data_dir):
    response = client.put('/snapshot', data=bson.dumps(_MESSAGE))
    assert response.status_code == 200
    f = data_dir / _FILE
    assert f.read_text() == json.dumps({
        "user": _USER,
        "snapshot": {
            "datetime": _TIMESTAMP,
            "color_image": {"data_path": str(data_dir / str(_USER_ID) / str(_TIMESTAMP) / "color_image.bin")},
            "depth_image": {"data_path": str(data_dir / str(_USER_ID) / str(_TIMESTAMP) / "depth_image.bin")}
        }
    })


def test_real_snapshot(client, data_dir):
    sample = pathlib.Path(__file__).resolve().parent.parent / 'resources' / 'test_snapshot.bin'
    snapshot_binary = sample.read_bytes()
    response = client.put('/snapshot', data=snapshot_binary)
    assert response.status_code == 200
    f = data_dir / _FILE
    assert sample.stat().st_size > 5 * 1024 * 1024  # 5MB
    assert f.stat().st_size < 10 * 1024  # 10KB
    assert json.loads(f.read_text())
