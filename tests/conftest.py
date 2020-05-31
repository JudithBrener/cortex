import os
import pathlib
import socket
import struct
import sys
import datetime as dt
import uuid

import docker as libdocker
import pytest

from cortex.proto.cortex_pb2 import User, Snapshot, ColorImage, DepthImage, Feelings, Pose

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

pytest_plugins = ['mongo_fixtures']


@pytest.fixture(scope="session")
def session_id():
    return str(uuid.uuid4())


@pytest.fixture(scope="session")
def unused_port():
    def f():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('127.0.0.1', 0))
            return sock.getsockname()[1]

    return f


@pytest.fixture(scope="session")
def docker():
    return libdocker.APIClient(version="auto")


@pytest.fixture(scope="session")
def snapshot():
    translation = Pose.Translation(x=1, y=2, z=3)
    rotation = Pose.Rotation(x=1, y=2, z=3, w=4)
    pose = Pose(translation=translation, rotation=rotation)
    data = (1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1)
    data = struct.pack('27B', *data)
    color_image = ColorImage(width=3, height=3, data=data)
    depth_image = DepthImage(width=3, height=3, data=[0.0, 0.0, 0.0, 1.0, 1.1, 1.0, 1.6, 1.1, 1.6])
    feelings = Feelings(hunger=1.0, thirst=2.0, exhaustion=3.0, happiness=4.0)

    return Snapshot(datetime=1590954369, pose=pose, color_image=color_image, depth_image=depth_image, feelings=feelings)


@pytest.fixture(scope="session")
def user():
    return User(user_id=6, username="Judith Brener", birthday=int(dt.datetime(1994, 5, 1).timestamp()), gender=1)


@pytest.fixture(scope="session")
def mind_sample(user, snapshot):
    path = pathlib.Path(__file__).parent / 'resources' / 'test_sample.mind'
    serialized_user = user.SerializeToString()
    serialized_snapshot = snapshot.SerializeToString()
    with open(path, 'wb') as f:
        f.write(struct.pack('I', len(serialized_user)))
        f.write(serialized_user)
        f.write(struct.pack('I', len(serialized_snapshot)))
        f.write(serialized_snapshot)
    yield path
