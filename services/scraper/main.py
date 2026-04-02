import logging
import requests
import pika

from scraper import scrape
from parser import parse_configuration
from shared.broker import send_messages
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).parent / "config.yaml"


def main():
    try:
        config = parse_configuration(str(CONFIG_PATH))
        result = scrape(config)
        logger.info("Scraping finished, %d items collected", len(result))
        logger.debug("Result: %s", result)
        send_messages([str(item) for item in result])
    except FileNotFoundError as e:
        logger.error("Config error: %s", e)
    except requests.RequestException as e:
        logger.error("Scraping failed: %s", e)
    except pika.exceptions.AMQPError as e:
        logger.error("RabbitMQ error: %s", e)


if __name__ == "__main__":
    main()
