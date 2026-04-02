from parser import ScraperConfig
from bs4 import BeautifulSoup
import requests


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
