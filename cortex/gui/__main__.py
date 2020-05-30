import logging
import sys
import traceback

import click

from cortex.gui.gui_server import run_gui_server

log = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', default='127.0.0.1', help='Server Host.')
@click.option('-p', '--port', default=8080, help='Server port.')
@click.option('-H', '--api-host', default='127.0.0.1', help='API Host.')
@click.option('-P', '--api-port', default=5000, help='API port.')
def run(host, port, api_host, api_port):
    run_gui_server(host, port, api_host, api_port)


if __name__ == '__main__':
    try:
        cli()
    except Exception as e:
        log.error(traceback.format_exc())
        sys.exit(1)
