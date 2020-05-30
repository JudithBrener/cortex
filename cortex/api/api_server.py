import logging
from urllib.parse import urlparse

import pymongo
import datetime as dt
from flask import Flask, jsonify, abort, request, send_file

from cortex.database.mongo import MongoCortexDao

log = logging.getLogger(__name__)
app = Flask(__name__)


def run_api_server(host, port, db_url):
    log.info('Going to run api server at host: ' + host + ' port: ' + str(port))
    parsed_db_url = urlparse(db_url)
    with pymongo.MongoClient(host=parsed_db_url.hostname, port=parsed_db_url.port) as mongo_client:
        db = MongoCortexDao(mongo_client)

    @app.after_request
    def apply_caching(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    @app.route('/')
    def health():
        return 'API Server is up and running!'

    @app.route('/users')
    def get_users():
        return jsonify(db.get_users())

    @app.route('/users/<user_id>')
    def get_user(user_id):
        user = db.get_user(user_id)
        if user is None:
            abort(404)
        if 'birthday' in user:
            user['birthday'] = dt.datetime.fromtimestamp(user['birthday'])
        return jsonify(user)

    @app.route('/users/<user_id>/snapshots')
    def get_user_snapshots(user_id):
        snapshots = db.get_snapshots(user_id)
        if snapshots is None:
            abort(404)
        for snapshot in snapshots:
            if 'datetime' in snapshot:
                datetime = int(snapshot['datetime']) / 1e3  # true division, remove milliseconds
                snapshot['datetime'] = dt.datetime.fromtimestamp(datetime)
        return jsonify(snapshots)

    @app.route('/users/<user_id>/snapshots/<snapshot_id>')
    def get_snapshot(user_id, snapshot_id):
        snapshot = db.get_snapshot(user_id, snapshot_id)
        if snapshot is None:
            abort(404)
        if 'datetime' in snapshot:
            datetime = int(snapshot['datetime']) / 1e3  # true division, remove milliseconds
            snapshot['datetime'] = dt.datetime.fromtimestamp(datetime)
        return jsonify(snapshot)

    @app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>')
    def get_result(user_id, snapshot_id, result_name):
        result = db.get_snapshot_topic(user_id, snapshot_id, result_name)
        if result is None:
            abort(404)
        if result_name in ['color_image', 'depth_image']:
            return jsonify({'url_to_view_data': f'{request.url}/data'})
        return jsonify(result[result_name])

    @app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>/data')
    def get_result_data(user_id, snapshot_id, result_name):
        result = db.get_snapshot_topic(user_id, snapshot_id, result_name)
        if result is None:
            abort(404)
        if result_name not in ['color_image', 'depth_image']:
            abort(404)
        return send_file(result[result_name])

    Flask.run(app, host, port)
