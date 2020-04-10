import json
import os
import pathlib
import time

import bson
import pytest

from cortex.server.server import app as flask_app, Server
from cortex.server.server import set_server

root = pathlib.Path(__file__).absolute().parent.parent

_USER = {"user_id": 1234, "username": 'test user'}
_IMAGE_WITH_DATA = {"data": [1, 1, 1, 1, 1]}
_COLOR_IMAGE_WITH_PATH = {"data_path": ''}
_DEPTH_IMAGE_WITH_PATH = {"data_path": ''}
_SNAPSHOT = {"datetime": 1456886665, "color_image": _IMAGE_WITH_DATA, "depth_image": _IMAGE_WITH_DATA}
_SLIM_SNAPSHOT = {"datetime": 1456886665, "color_image": _COLOR_IMAGE_WITH_PATH, "depth_image": _DEPTH_IMAGE_WITH_PATH}
_MESSAGE = {"user": _USER, "snapshot": _SNAPSHOT}
_FILE = 'test_file'


@pytest.fixture
def client(tmp_path):
    def publish_method(message):
        with open(tmp_path / _FILE, 'w') as f:
            f.write(message)

    cwd = os.getcwd()
    os.chdir(root)

    set_server(Server(publish_method, str(tmp_path)))
    app = flask_app
    with app.test_client() as client:
        yield client, tmp_path

    os.chdir(cwd)


def test_health(client):
    client, _ = client
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'Server is up and running!'


def test_snapshot(client):
    client, data_dir = client
    time.sleep(0.5)
    response = client.put('/snapshot', data=bson.dumps(_MESSAGE))
    assert response.status_code == 200
    f = data_dir / _FILE
    assert f.read_text() == json.dumps({"user": _USER,
                                        "snapshot": {
                                            "datetime": _SNAPSHOT["datetime"],
                                            "color_image": {"data_path": str(data_dir / str(_USER["user_id"]) / str(
                                                _SNAPSHOT["datetime"]) / "color_image.bin")},
                                            "depth_image": {"data_path": str(data_dir / str(_USER["user_id"]) / str(
                                                _SNAPSHOT["datetime"]) / "depth_image.bin")}
                                        }
                                        })
