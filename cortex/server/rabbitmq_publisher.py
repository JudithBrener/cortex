import pika


def get_rabbitmq_publish_method(host, port):
    def publish_to_mq(message):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        channel = connection.channel()
        channel.exchange_declare(exchange='cortex.snapshots', exchange_type='fanout')
        channel.basic_publish(exchange='cortex.snapshots', routing_key='', body=message)
        connection.close()

    return publish_to_mq
