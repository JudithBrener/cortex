import sys
from urllib.parse import urlparse

import click

from cortex.server import run_server
from cortex.server import log


@click.group()
def cli():
    pass


def publish_to_mq(message):
    pass


@cli.command('run-server')
@click.option('-h', '--host', default='127.0.0.1', help='Server Host.')
@click.option('-p', '--port', default=8000, help='Server port.')
@click.argument('message_queue_url', type=str)
def run(host, port, message_queue_url):
    parse_url = urlparse(message_queue_url)
    if not parse_url.scheme:
        raise ValueError("message queue URL is invalid")
    if parse_url.scheme == 'rabbitmq':
        publish = publish_to_mq
    else:
        raise NotImplementedError('not supporting message queue of type ' + parse_url.scheme)
    run_server(host, port, publish)


if __name__ == '__main__':
    try:
        cli()
    except Exception as e:
        log.error(e)
        sys.exit(1)
