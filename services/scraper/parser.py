from typing import Any, TypedDict

import yaml


class ScraperConfig(TypedDict):
    url: str
    pagination: str
    limiter: int
    fields: dict[str, Any]


def parse_configuration(filepath: str) -> ScraperConfig:
    try:
        with open(filepath, "r") as file:
            data = yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Yaml file is invalid: {filepath}") from e

    try:
        output: ScraperConfig = {
            "url": data["site"]["url"],
            "pagination": data["site"]["pagination"]["pattern"],
            "limiter": data["site"]["pagination"]["limiter"],
            "fields": data["site"]["fields"],
        }
    except (KeyError, TypeError) as e:
        raise KeyError(
            "Configuration is missing one or more required fields. (required fields: site, url, pagination, limiter, fields)"
        ) from e
    return output
