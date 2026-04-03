import logging
import os
import pika

logger = logging.getLogger(__name__)


def send_messages(messages: list[str]) -> None:
    credentials = pika.PlainCredentials(
        os.getenv("RABBITMQ_DEFAULT_USER"),
        os.getenv("RABBITMQ_DEFAULT_PASS"),
        erase_on_connect=True,
    )
    parameters = pika.ConnectionParameters(
        host="rabbitmq", virtual_host="kscraper", credentials=credentials
    )
    logger.info("Connecting to RabbitMQ to send %d message(s)", len(messages))
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(
        queue="kscraper", durable=True, arguments={"x-queue-type": "quorum"}
    )
    for message in messages:
        logger.debug("Publishing message: %s", message)
        channel.basic_publish(exchange="", routing_key="kscraper", body=message)
    logger.info("Successfully sent %d message(s)", len(messages))
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
    logger.info("Connecting to RabbitMQ to receive messages")
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(
        queue="kscraper", durable=True, arguments={"x-queue-type": "quorum"}
    )

    def callback(ch, method, properties, body):
        logger.info("Received message: %s", body.decode())

    try:
        channel.basic_consume(
            queue="kscraper", on_message_callback=callback, auto_ack=True
        )
        logger.info("Waiting for messages...")
        channel.start_consuming()
    except KeyboardInterrupt:
        logger.info("Stopping consumer")
        channel.stop_consuming()
    connection.close()
    logger.info("Connection closed")
