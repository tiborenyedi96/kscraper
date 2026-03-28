from diagrams import Diagram
from diagrams.onprem.queue import Rabbitmq as rabbitmq
from diagrams.programming.language import Python as scraper
from diagrams.onprem.database import ClickHouse as clickhouse


def main():
    with Diagram("kscraper", show=False, outformat="png", filename="docs/kscraper"):
        (
            scraper("scraper service")
            >> rabbitmq("queue service")
            >> clickhouse("clickhouse database")
        )


if __name__ == "__main__":
    main()
