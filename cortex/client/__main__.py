import sys
import click

from .client import upload_sample


@click.group()
def cli():
    pass


@cli.command('upload_sample')
@click.option('-h', '--host', default='127.0.0.1', help='Server Host.')
@click.option('-p', '--port', default=8000, help='Server port.')
@click.argument('path', type=str)
def upload(host, port, path):
    upload_sample(host, port, path)


if __name__ == '__main__':
    try:
        cli()
    except Exception as error:
        print(f'ERROR: {error}')
        sys.exit(1)
