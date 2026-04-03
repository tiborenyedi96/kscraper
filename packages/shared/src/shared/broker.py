import os
import pika


def send_messages(messages: list[str]) -> None:
    credentials = pika.PlainCredentials(
        os.getenv("RABBITMQ_DEFAULT_USER"),
        os.getenv("RABBITMQ_DEFAULT_PASS"),
        erase_on_connect=True,
    )
    parameters = pika.ConnectionParameters(
        host="rabbitmq", virtual_host="kscraper", credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(
        queue="kscraper", durable=True, arguments={"x-queue-type": "quorum"}
    )
    for message in messages:
        channel.basic_publish(exchange="", routing_key="kscraper", body=message)
    connection.close()


def receive_messages():
    credentials = pika.PlainCredentials(
        os.getenv("RABBITMQ_DEFAULT_USER"),
        os.getenv("RABBITMQ_DEFAULT_PASS"),
        erase_on_connect=True,
    )
    parameters = pika.ConnectionParameters(
        host="rabbitmq", virtual_host="kscraper", credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(
        queue="kscraper", durable=True, arguments={"x-queue-type": "quorum"}
    )

    def callback(ch, method, properties, body):
        print(body)

    try:
        channel.basic_consume(
            queue="kscraper", on_message_callback=callback, auto_ack=True
        )
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()
