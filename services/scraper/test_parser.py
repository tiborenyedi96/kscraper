import pytest
import yaml
from parser import parse_configuration

def test_parser() -> None:
    assert parse_configuration("./services/scraper/mock.yaml") == {
        "url": "mock-url",
        "pagination": "mock-pattern",
        "limiter": 100,
        "fields": {
            "title": {
                "tag": "a",
                "attribute": "href"
            },
            "price": {
                "tag": "p",
                "text": True,
                "remove": "$"
            },
            "rating": {
                "tag": "p",
                "text": True,
                "class": "rating"
            }
        }
    }

def test_yaml_not_exist() -> None:
    with pytest.raises(FileNotFoundError):
        parse_configuration("fakepath")

def test_yaml_syntax_error() -> None:
    with pytest.raises(yaml.YAMLError):
        parse_configuration("./services/scraper/error.yaml")