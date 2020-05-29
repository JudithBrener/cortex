import logging
import sys
import traceback
from urllib.parse import urlparse
import click

from .parsers_manager import run_parser, consume_from_rabbitmq

log = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command('parse')
@click.argument('parser_name', type=str)
@click.argument('raw_data_path', type=click.File())
def cli_parse(parser_name, raw_data_path):
    """
    Receives parser name and a path to some raw data and prints the result.
    """
    print(run_parser(parser_name, raw_data_path.read()))


@cli.command('run-parser')
@click.argument('parser_name', type=str)
@click.argument('message_queue_url', type=str)
def cli_run_parser(parser_name, message_queue_url):
    """
    Receives parser name and message queue url and starts consuming from it and publishing parsed results.
    """
    parse_url = urlparse(message_queue_url)
    if not parse_url.scheme:
        raise ValueError("Message queue URL is invalid. Provide scheme")
    if parse_url.scheme == 'rabbitmq':
        consume_from_rabbitmq(parser_name, parse_url.hostname, parse_url.port)
    else:
        raise NotImplementedError(f'No supporting message queue of type {parse_url.scheme}.')


if __name__ == '__main__':
    try:
        cli()
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)
