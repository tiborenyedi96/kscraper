from unittest.mock import patch, MagicMock
from shared.broker import send_messages, receive_messages


def make_channel_mock():
    channel = MagicMock()
    return channel


def make_connection_mock(channel):
    connection = MagicMock()
    connection.channel.return_value = channel
    return connection


@patch("shared.broker.pika.BlockingConnection")
@patch("shared.broker.pika.ConnectionParameters")
@patch("shared.broker.pika.PlainCredentials")
def test_send_messages_declares_queue(
    mock_creds, mock_params, mock_conn_cls, monkeypatch
):
    monkeypatch.setenv("RABBITMQ_DEFAULT_USER", "user")
    monkeypatch.setenv("RABBITMQ_DEFAULT_PASS", "pass")
    channel = make_channel_mock()
    mock_conn_cls.return_value = make_connection_mock(channel)

    send_messages(["msg1"])

    channel.queue_declare.assert_called_once_with(
        queue="kscraper", durable=True, arguments={"x-queue-type": "quorum"}
    )


@patch("shared.broker.pika.BlockingConnection")
@patch("shared.broker.pika.ConnectionParameters")
@patch("shared.broker.pika.PlainCredentials")
def test_send_messages_publishes_each_message(
    mock_creds, mock_params, mock_conn_cls, monkeypatch
):
    monkeypatch.setenv("RABBITMQ_DEFAULT_USER", "user")
    monkeypatch.setenv("RABBITMQ_DEFAULT_PASS", "pass")
    channel = make_channel_mock()
    mock_conn_cls.return_value = make_connection_mock(channel)

    send_messages(["hello", "world"])

    assert channel.basic_publish.call_count == 2
    channel.basic_publish.assert_any_call(
        exchange="", routing_key="kscraper", body="hello"
    )
    channel.basic_publish.assert_any_call(
        exchange="", routing_key="kscraper", body="world"
    )


@patch("shared.broker.pika.BlockingConnection")
@patch("shared.broker.pika.ConnectionParameters")
@patch("shared.broker.pika.PlainCredentials")
def test_send_messages_closes_connection(
    mock_creds, mock_params, mock_conn_cls, monkeypatch
):
    monkeypatch.setenv("RABBITMQ_DEFAULT_USER", "user")
    monkeypatch.setenv("RABBITMQ_DEFAULT_PASS", "pass")
    channel = make_channel_mock()
    connection = make_connection_mock(channel)
    mock_conn_cls.return_value = connection

    send_messages(["msg"])

    connection.close.assert_called_once()


@patch("shared.broker.pika.BlockingConnection")
@patch("shared.broker.pika.ConnectionParameters")
@patch("shared.broker.pika.PlainCredentials")
def test_send_messages_empty_list(mock_creds, mock_params, mock_conn_cls, monkeypatch):
    monkeypatch.setenv("RABBITMQ_DEFAULT_USER", "user")
    monkeypatch.setenv("RABBITMQ_DEFAULT_PASS", "pass")
    channel = make_channel_mock()
    mock_conn_cls.return_value = make_connection_mock(channel)

    send_messages([])

    channel.basic_publish.assert_not_called()


@patch("shared.broker.pika.BlockingConnection")
@patch("shared.broker.pika.ConnectionParameters")
@patch("shared.broker.pika.PlainCredentials")
def test_receive_messages_declares_queue(
    mock_creds, mock_params, mock_conn_cls, monkeypatch
):
    monkeypatch.setenv("RABBITMQ_DEFAULT_USER", "user")
    monkeypatch.setenv("RABBITMQ_DEFAULT_PASS", "pass")
    channel = make_channel_mock()
    channel.start_consuming.side_effect = KeyboardInterrupt
    mock_conn_cls.return_value = make_connection_mock(channel)

    receive_messages()

    channel.queue_declare.assert_called_once_with(
        queue="kscraper", durable=True, arguments={"x-queue-type": "quorum"}
    )


@patch("shared.broker.pika.BlockingConnection")
@patch("shared.broker.pika.ConnectionParameters")
@patch("shared.broker.pika.PlainCredentials")
def test_receive_messages_starts_consuming(
    mock_creds, mock_params, mock_conn_cls, monkeypatch
):
    monkeypatch.setenv("RABBITMQ_DEFAULT_USER", "user")
    monkeypatch.setenv("RABBITMQ_DEFAULT_PASS", "pass")
    channel = make_channel_mock()
    channel.start_consuming.side_effect = KeyboardInterrupt
    mock_conn_cls.return_value = make_connection_mock(channel)

    receive_messages()

    from unittest.mock import ANY

    channel.basic_consume.assert_called_once_with(
        queue="kscraper", on_message_callback=ANY, auto_ack=True
    )
    channel.start_consuming.assert_called_once()


@patch("shared.broker.pika.BlockingConnection")
@patch("shared.broker.pika.ConnectionParameters")
@patch("shared.broker.pika.PlainCredentials")
def test_receive_messages_stops_on_keyboard_interrupt(
    mock_creds, mock_params, mock_conn_cls, monkeypatch
):
    monkeypatch.setenv("RABBITMQ_DEFAULT_USER", "user")
    monkeypatch.setenv("RABBITMQ_DEFAULT_PASS", "pass")
    channel = make_channel_mock()
    channel.start_consuming.side_effect = KeyboardInterrupt
    connection = make_connection_mock(channel)
    mock_conn_cls.return_value = connection

    receive_messages()

    channel.stop_consuming.assert_called_once()
    connection.close.assert_called_once()


@patch("shared.broker.pika.BlockingConnection")
@patch("shared.broker.pika.ConnectionParameters")
@patch("shared.broker.pika.PlainCredentials")
def test_receive_messages_callback_logs_body(
    mock_creds, mock_params, mock_conn_cls, monkeypatch, caplog
):
    import logging

    monkeypatch.setenv("RABBITMQ_DEFAULT_USER", "user")
    monkeypatch.setenv("RABBITMQ_DEFAULT_PASS", "pass")

    captured_callback = None

    def fake_basic_consume(queue, on_message_callback, auto_ack):
        nonlocal captured_callback
        captured_callback = on_message_callback

    channel = make_channel_mock()
    channel.basic_consume.side_effect = fake_basic_consume
    channel.start_consuming.side_effect = KeyboardInterrupt
    mock_conn_cls.return_value = make_connection_mock(channel)

    with caplog.at_level(logging.INFO, logger="shared.broker"):
        receive_messages()
        captured_callback(None, None, None, b"test-message")

    assert "test-message" in caplog.text


@patch("shared.broker.pika.BlockingConnection")
@patch("shared.broker.pika.ConnectionParameters")
@patch("shared.broker.pika.PlainCredentials")
def test_send_messages_uses_env_credentials(
    mock_creds, mock_params, mock_conn_cls, monkeypatch
):
    monkeypatch.setenv("RABBITMQ_DEFAULT_USER", "myuser")
    monkeypatch.setenv("RABBITMQ_DEFAULT_PASS", "mypass")
    channel = make_channel_mock()
    mock_conn_cls.return_value = make_connection_mock(channel)

    send_messages(["msg"])

    mock_creds.assert_called_once_with("myuser", "mypass", erase_on_connect=True)
