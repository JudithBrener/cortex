import logging
import sys
import traceback
import click

from cortex.api import run_api_server

log = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', default='127.0.0.1', help='API Server Host.')
@click.option('-p', '--port', default=5000, help='API Server port.')
@click.option('-d', '--database', default='mongodb://localhost:27017', help="URL including scheme of the Database.")
def run_api(host, port, db_url):
    """
    Receives hostname and port to run the API Server and database url for the API.
    """
    run_api_server(host, port, db_url)


if __name__ == '__main__':
    try:
        cli()
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)
