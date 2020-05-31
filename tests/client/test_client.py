import pathlib

import pytest

from cortex.client.reader import Reader


@pytest.fixture
def reader(mind_sample):
    return Reader(pathlib.Path(mind_sample).open('rb'))


def test_read_user(reader, user):
    read_user = reader.user
    assert read_user.SerializeToString() == user.SerializeToString()


def test_read_snapshot(reader, snapshot):
    for read_snapshot in reader:
        assert read_snapshot.SerializeToString() == snapshot.SerializeToString()

