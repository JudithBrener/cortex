import sys
from urllib.parse import urlparse

import click
import pymongo

from cortex.saver import log
from cortex.saver.mongo import MongoDB
from cortex.saver.saver import Saver


@click.group()
def cli():
    pass


@cli.command("save")
@click.option(
    "-d",
    "--database",
    default="mongodb://localhost:27017/",
    help="Database URL",
)
@click.argument("topic")
@click.argument("data_path", type=click.File("rb"))
def save(database, topic, data_path):
    db_url = urlparse(database)
    if not db_url.scheme:
        raise ValueError("Database URL is invalid")
    if db_url.scheme == 'mongodb':
        with pymongo.MongoClient(host=db_url.hostname, port=db_url.port) as mongo_client:
            db = MongoDB(mongo_client)
    else:
        raise NotImplementedError('not supporting message queue of type ' + parse_url.scheme)
    saver = Saver(db)
    saver.save(topic, data_path.read())


if __name__ == '__main__':
    try:
        cli()
    except Exception as e:
        log.error(e)
        sys.exit(1)
