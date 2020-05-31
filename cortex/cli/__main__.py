import logging
import sys
import traceback
import click
import requests

log = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command('get-users')
@click.option('-h', '--host', default='127.0.0.1', help='API Server Host.')
@click.option('-p', '--port', default=5000, help='API Server port.')
def get_users(host, port):
    """
    Returns the list of all the supported users, including their IDs and names only.
    """
    print(requests.get(f'http://{host}:{port}/users').json())


@cli.command('get-user')
@click.option('-h', '--host', default='127.0.0.1', help='API Server Host.')
@click.option('-p', '--port', default=5000, help='API Server port.')
@click.argument('user_id', type=int)
def get_user(host, port, user_id):
    """
   Returns the specified user's details: ID, name, birthday and gender.
    """
    print(requests.get(f'http://{host}:{port}/users/{user_id}').json())


@cli.command('get-snapshots')
@click.option('-h', '--host', default='127.0.0.1', help='API Server Host.')
@click.option('-p', '--port', default=5000, help='API Server port.')
@click.argument('user_id', type=int)
def get_snapshots(host, port, user_id):
    """
    Returns the list of the specified user's snapshot IDs and datetimes only.
    """
    print(requests.get(f'http://{host}:{port}/users/{user_id}/snapshots').json())


@cli.command('get-snapshot')
@click.option('-h', '--host', default='127.0.0.1', help='API Server Host.')
@click.option('-p', '--port', default=5000, help='API Server port.')
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=str)
def get_snapshot(host, port, user_id, snapshot_id):
    """
    Returns the specified snapshot's details: ID, datetime, and the available results' names only.
    """
    print(requests.get(f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}').json())


@cli.command('get-result')
@click.option('-h', '--host', default='127.0.0.1', help='API Server Host.')
@click.option('-p', '--port', default=5000, help='API Server port.')
@click.option('-s', '--save', default=None, help='Provide Path to save the result to that path.')
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=str)
@click.argument('result_name', type=str)
def get_result(host, port, user_id, snapshot_id, result_name, save):
    """
    Returns the specified snapshot's result. Use -s/--save flag to save it to a file.
    """
    result = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{result_name}').json()
    print(result)
    if save:
        with open(save, 'w') as f:
            f.write(result)


if __name__ == '__main__':
    try:
        cli()
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)
