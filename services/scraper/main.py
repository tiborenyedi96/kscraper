import os
import logging
import pika
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from parser import ScraperConfig, parse_configuration

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).parent / "config.yaml"


# scraper
def scrape(config: ScraperConfig) -> list[dict[str, str]]:
    field_values: dict[str, list[str]] = {name: [] for name in config["fields"]}

    for i in range(1, config["limiter"] + 1):
        current_url: str = config["pagination"].format(url=config["url"], page=i)
        request = requests.get(current_url)

        if request.status_code != 200:
            break

        soup = BeautifulSoup(request.content.decode("utf-8"), features="html.parser")

        for field_name, field_def in config["fields"].items():
            selector = {k: v for k, v in field_def.items() if k == "class"}
            for item in soup.find_all(field_def["tag"], selector):
                if field_def.get("text"):
                    value = item.get_text().replace(field_def.get("remove", ""), "")
                    field_values[field_name].append(value)
                elif field_def.get("attribute"):
                    value = item.get(field_def["attribute"], "")
                    if value:
                        field_values[field_name].append(value)

    return [
        dict(zip(field_values.keys(), values)) for values in zip(*field_values.values())
    ]


# rabbitmq
def send_message() -> None:
    credentials = pika.PlainCredentials(os.getenv("RABBITMQ_DEFAULT_USER"), os.getenv("RABBITMQ_DEFAULT_PASS"), erase_on_connect=True)
    parameters = pika.ConnectionParameters(host="rabbitmq", virtual_host="kscraper", credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(
        queue="kscraper", durable=True, arguments={"x-queue-type": "quorum"}
    )
    channel.basic_publish(exchange="", routing_key="kscraper", body="Hello scraper!")
    connection.close()


# main
def main():
    try:
        config = parse_configuration(str(CONFIG_PATH))
        result = scrape(config)
        logger.info("Scraping finished, %d items collected", len(result))
        logger.debug("Result: %s", result)
    except FileNotFoundError as e:
        logger.error("Config error: %s", e)
    except requests.RequestException as e:
        logger.error("Scraping failed: %s", e)

    send_message()


if __name__ == "__main__":
    main()
