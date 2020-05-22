import json
import logging
import tempfile
import traceback
from pathlib import Path

import pybson as bson
from flask import Flask
from flask import request

log = logging.getLogger(__name__)
app = Flask(__name__)
server = None


class Server:

    def __init__(self, publish_method, data_dir=None):
        self.publish_method = publish_method
        if data_dir is None:
            path_obj = Path(tempfile.gettempdir()) / 'cortex-data'
            data_dir = str(path_obj)
        self.data_dir = data_dir
        pass

    def handle_snapshot(self, data):
        try:
            message = bson.loads(data)
            self.validate_snapshot(message)
        except Exception as e:
            log.warning("Invalid snapshot message. Exception: \n{}".format(traceback.format_exc()))
            return "Invalid snapshot message", 400
        slim_snapshot = self._get_slim_snapshot(message)
        self.publish_method(json.dumps(slim_snapshot))
        return 'OK'

    @staticmethod
    def validate_snapshot(message):
        assert message['user']['user_id'] \
               and message['snapshot']['datetime'] \
               and message['snapshot']['color_image'] \
               and message['snapshot']['depth_image']

    def _get_slim_snapshot(self, message):
        base_path = Path(self.data_dir)
        snapshot = message['snapshot']
        base_path = base_path / str(message['user']['user_id']) / str(snapshot['datetime'])
        base_path.mkdir(parents=True, exist_ok=True)
        self._save_image_to_disk(snapshot['color_image'], base_path / 'color_image.bin')
        self._save_image_to_disk(snapshot['depth_image'], base_path / 'depth_image.bin')

        return message

    @staticmethod
    def _save_image_to_disk(image, path):
        # save image to disk
        with open(path, 'w') as f:
            f.write(json.dumps(image["data"]))
        # add data_path field to image
        image["data_path"] = str(path)
        # delete data field from image
        del image["data"]
        pass


@app.route('/')
def health():
    return 'Server is up and running!'


@app.route('/snapshot', methods=['PUT'])
def put_snapshot():
    return server.handle_snapshot(request.data)


def set_server(instance):
    global server
    server = instance


def run_server(host, port, publish):
    log.info('Going to run server at host: ' + host + ' port: ' + str(port))
    set_server(Server(publish))
    Flask.run(app, host, port)
    return app
