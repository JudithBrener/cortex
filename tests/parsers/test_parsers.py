import inspect
import json
import pathlib
import shutil

import pytest

from cortex.parsers.parsers_manager import get_available_parsers, run_parser


@pytest.fixture()
def raw_data(tmp_path):
    resources_dir = pathlib.Path(__file__).resolve().parent.parent / 'resources'
    color_image_path = resources_dir / 'color_image.bin'
    depth_image_path = resources_dir / 'depth_image.bin'

    test_color_image = tmp_path / 'color_image.bin'
    test_depth_image = tmp_path / 'depth_image.bin'

    shutil.copy(str(color_image_path), str(test_color_image))
    shutil.copy(str(depth_image_path), str(test_depth_image))

    raw_json = {
        "user": {
            "user_id": "42",
            "username": "Dan Gittik",
            "birthday": 699746400,
            "gender": "MALE"
        },
        "snapshot": {
            "datetime": "1575446887339",
            "pose": {
                "translation": {
                    "x": 0.4873843491077423,
                    "y": 0.007090016733855009,
                    "z": -1.1306129693984985
                },
                "rotation": {
                    "x": -0.10888676356214629,
                    "y": -0.26755994585035286,
                    "z": -0.021271118915446748,
                    "w": 0.9571326384559261
                }
            },
            "color_image": {
                "width": 1920,
                "height": 1080,
                "data_path": str(test_color_image)
            },
            "depth_image": {
                "width": 224,
                "height": 172,
                "data_path": str(test_depth_image)
            },
            "feelings": {
                "hunger": 0.0,
                "thirst": 0.0,
                "exhaustion": 0.0,
                "happiness": 0.0
            }
        }
    }
    return json.dumps(raw_json)


def test_get_available_parsers():
    parsers = get_available_parsers()
    assert 'color_image' in parsers
    assert 'depth_image' in parsers
    assert 'feelings' in parsers
    assert 'pose' in parsers

    for parser in parsers:
        assert inspect.isfunction(parsers[parser])


def test_run_parser(raw_data):
    parsers = get_available_parsers()
    for parser in parsers:
        results = run_parser(parser, raw_data)
        assert results is not None
        results_json = json.loads(results)
        assert 'user' in results_json
        assert parser in results_json
        assert 'datetime' in results_json
