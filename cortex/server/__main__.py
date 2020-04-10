import sys

import click

from cortex.server import run_server


@click.group()
def cli():
    pass


def publish_to_mq(message):
    pass


def publish_to_console(message):
    print(message)


@cli.command('run-server')
@click.option('-h', '--host', default='127.0.0.1', help='Server Host.')
@click.option('-p', '--port', default=8000, help='Server port.')
@click.argument('message_queue_url', type=str)
def run(host, port, message_queue_url):
    if message_queue_url and message_queue_url.startswith('rabbitmq://'):
        publish = publish_to_mq
    else:
        publish = publish_to_console
    run_server(host, port, publish)


if __name__ == '__main__':
    try:
        cli()
    except Exception as error:
        print(f'ERROR: {error}')
        sys.exit(1)
