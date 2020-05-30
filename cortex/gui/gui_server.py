import logging

from flask import Flask, render_template

log = logging.getLogger(__name__)
app = Flask(__name__, static_url_path='', static_folder="./gui_vue/dist", template_folder="./gui_vue/dist")


def run_gui_server(host, port, api_host, api_port):
    log.info('Going to run gui server at host: ' + host + ' port: ' + str(port))

    @app.after_request
    def apply_caching(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    @app.route('/')
    def index():
        return render_template("index.html", api_url=f"http://{api_host}:{api_port}")

    Flask.run(app, host, port)
