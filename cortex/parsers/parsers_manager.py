import importlib
import inspect
import pathlib

import pika


def get_available_parsers():
    available_parsers = {}
    current_directory = pathlib.Path(__file__).parent.absolute()
    root = f'{current_directory.parent.name}.{current_directory.name}'
    for path in current_directory.iterdir():
        if path.name.startswith('parser_'):
            module = importlib.import_module(f'.{path.stem}', package=root)
            for name, member in inspect.getmembers(module):
                if hasattr(member, 'field'):
                    if inspect.isfunction(member):
                        available_parsers[member.field] = member
                    if inspect.isclass(member):
                        available_parsers[member.field] = member().parse
    return available_parsers


def run_parser(parser_name, raw_data):
    parsers = get_available_parsers()
    if parser_name not in parsers:
        raise NameError(f'No parser named {parser_name}. Make sure it exists in parsers package.')
    return parsers[parser_name](raw_data)


def consume_from_rabbitmq(parser_name, host, port):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
    channel = connection.channel()
    channel.exchange_declare(exchange='cortex.snapshots', exchange_type='fanout')
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='cortex.snapshots', queue=queue_name)

    channel.exchange_declare(exchange="cortex.parsers", exchange_type="topic")

    def callback(ch, method, properties, body):
        parsed_message = run_parser(parser_name, body)
        ch.basic_publish(exchange='cortex.parsers', routing_key=parser_name, body=parsed_message)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()
