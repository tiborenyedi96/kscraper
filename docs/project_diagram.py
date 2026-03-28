from diagrams import Diagram, Cluster
from diagrams.programming.language import Python
from diagrams.k8s.compute import Cronjob
from diagrams.onprem.compute import Server
from diagrams.onprem.queue import Rabbitmq
from diagrams.onprem.database import ClickHouse


def main():

    with Diagram("", show=False, filename="docs/kscraper-diagram", direction="LR"):
        with Cluster("Kubernetes"):
            with Cluster("Data Processing"):
                with Cluster("Webpages"):
                    webpage = Server("")

                with Cluster("Scraper Service"):
                    scraper = [
                        Cronjob("scraper-2"),
                        Cronjob("scraper-1"),
                    ]

                with Cluster(""):
                    rabbitmq = Rabbitmq("RabbitMQ")

                with Cluster("ETL pipeline"):
                    with Cluster("Consumer Service"):
                        consumer = [
                            Python("consumer-2"),
                            Python("consumer-1"),
                        ]

                    clickhouse = ClickHouse("Clickhouse")

        (webpage >> scraper >> rabbitmq >> consumer >> clickhouse)


if __name__ == "__main__":
    main()
