import json
import sys
import traceback
from urllib.parse import urlparse

import click
import pika
import pymongo

from cortex.saver import log
from cortex.saver.mongo import MongoCortexDao
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
    saver = create_saver(database)
    saver.save(topic, data_path.read())


@cli.command("run-saver")
@click.argument("database")
@click.argument('message_queue_url', type=str)
def run_saver(database, message_queue_url):
    saver = create_saver(database)
    parse_url = urlparse(message_queue_url)
    if not parse_url.scheme:
        raise ValueError("message queue URL is invalid")
    if parse_url.scheme == 'rabbitmq':
        consume_from_rabbitmq(parse_url.hostname, parse_url.port, saver)
    else:
        raise NotImplementedError('not supporting message queue of type ' + parse_url.scheme)


def consume_from_rabbitmq(hostname, port, saver):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    channel = connection.channel()
    channel.exchange_declare(exchange='cortex.parsers', exchange_type='topic')
    queue = channel.queue_declare("", exclusive=True).method.queue
    channel.queue_bind(exchange="cortex.parsers", queue=queue, routing_key='#')

    def on_message_callback(topic, method, properties, body):
        saver.save(topic, json.loads(body))

    channel.basic_consume(queue=queue, auto_ack=True, on_message_callback=on_message_callback)
    channel.start_consuming()


def create_saver(db_url):
    parsed_db_url = urlparse(db_url)
    if not parsed_db_url.scheme:
        raise ValueError("Database URL is invalid")
    if parsed_db_url.scheme == 'mongodb':
        with pymongo.MongoClient(host=parsed_db_url.hostname, port=parsed_db_url.port) as mongo_client:
            db = MongoCortexDao(mongo_client)
    else:
        raise NotImplementedError('not supporting message queue of type ' + parsed_db_url.scheme)
    saver = Saver(db)
    return saver


if __name__ == '__main__':
    try:
        cli()
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)
