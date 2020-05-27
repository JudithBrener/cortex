import sys
from urllib.parse import urlparse
import click

from .parsers_manager import run_parser, consume_from_rabbitmq


@click.group()
def cli():
    pass


@cli.command('parse')
@click.argument('parser_name', type=str)
@click.argument('raw_data', type=str)
def cli_parse(parser_name, raw_data):
    """
    Receives parser name and some raw data and prints the result.
    """
    run_parser(parser_name, raw_data)


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
    except Exception as error:
        print(f'ERROR: {error}')
        sys.exit(1)
