import json
import tempfile
from pathlib import Path

import bson
from flask import Flask
from flask import request

app = Flask(__name__)
server = None


class Server:

    def __init__(self, publish_method, data_dir=None):
        self.publish_method = publish_method
        if data_dir is None:
            path_obj = Path(tempfile.gettempdir()) / 'tmp' / 'cortex-data'
            data_dir = str(path_obj)
        self.data_dir = data_dir
        pass

    def handle_snapshot(self, data):
        snapshot = bson.loads(data)
        slim_snapshot = self._get_slim_snapshot(snapshot)
        self.publish_method(json.dumps(slim_snapshot))

    def _get_slim_snapshot(self, message):
        base_path = Path(self.data_dir)
        snapshot = message['snapshot']
        base_path = base_path / str(message['user']['user_id']) / str(snapshot['datetime'])
        base_path.mkdir(parents=True, exist_ok=True)
        color_image_path = base_path / 'color_image.bin'
        depth_image_path = base_path / 'depth_image.bin'
        self._save_image_to_disk(snapshot['color_image'], color_image_path)
        self._save_image_to_disk(snapshot['depth_image'], depth_image_path)

        return message

    def _save_image_to_disk(self, image, path):
        # save image to disk
        with open(path, 'w') as f:
            f.write(json.dumps(image["data"]))
        # add path field to image
        image["data_path"] = str(path)
        # delete data field from image
        del image["data"]
        pass


@app.route('/')
def health():
    return 'Server is up and running!'


@app.route('/snapshot', methods=['PUT'])
def put_snapshot():
    data = request.data
    print(data)
    print(request.content_type)
    server.handle_snapshot(data)
    return 'OK'


def set_server(instance):
    global server
    server = instance


def run_server(host, port, publish):
    print('Going to run server at host: ' + host + ' port: ' + str(port))
    set_server(Server(publish))
    Flask.run(app, host, port)
    return app
