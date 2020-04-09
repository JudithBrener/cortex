import sys
from flask import Flask
import click

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@click.group()
def cli():
    pass


@cli.command()
@click.option('--host', default='127.0.0.1', help='Server Host.')
@click.option('--port', default=8000, help='Server port.')
def run_server(host, port):
    print('Going to run server at host: ' + host + ' port: ' + str(port))
    Flask.run(app, host, port)
    print('done')


if __name__ == '__main__':
    try:
        cli()
    except Exception as error:
        print(f'ERROR: {error}')
        sys.exit(1)
