import datetime as dt
import pathlib
import struct

import pytest

from cortex.client.reader import Reader
from cortex.proto.cortex_pb2 import User, Pose, ColorImage, DepthImage, Feelings, Snapshot


@pytest.fixture
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


@pytest.fixture
def user():
    return User(user_id=6, username="Judith Brener", birthday=767750400, gender=1)


@pytest.fixture
def reader():
    resources_dir = pathlib.Path(__file__).resolve().parent.parent / 'resources'
    mind_sample = resources_dir / 'test_sample.mind'
    return Reader(mind_sample.open('rb'))


def test_read_user(reader, user):
    read_user = reader.user
    assert read_user.SerializeToString() == user.SerializeToString()


def test_read_snapshot(reader, snapshot):
    for read_snapshot in reader:
        assert read_snapshot.SerializeToString() == snapshot.SerializeToString()
