import pytest
import yaml
from parser import parse_configuration

path_prefix: str = "./services/scraper/tests/fixtures/"


def test_parser() -> None:
    assert parse_configuration(f"{path_prefix}/mock.yaml") == {
        "url": "mock-url",
        "pagination": "mock-pattern",
        "limiter": 100,
        "fields": {
            "title": {"tag": "a", "attribute": "href"},
            "price": {"tag": "p", "text": True, "remove": "$"},
            "rating": {"tag": "p", "text": True, "class": "rating"},
        },
    }


def test_yaml_not_exist() -> None:
    with pytest.raises(FileNotFoundError):
        parse_configuration("fakepath")


def test_yaml_syntax_error() -> None:
    with pytest.raises(yaml.YAMLError):
        parse_configuration(f"{path_prefix}/error.yaml")


def test_yaml_missing_url() -> None:
    with pytest.raises(KeyError):
        parse_configuration(f"{path_prefix}/missingurl.yaml")


def test_yaml_missing_limiter() -> None:
    with pytest.raises(KeyError):
        parse_configuration(f"{path_prefix}/missinglimiter.yaml")


def test_yaml_missing_fields() -> None:
    with pytest.raises(KeyError):
        parse_configuration(f"{path_prefix}/missingfields.yaml")


def test_yaml_missing_pagination() -> None:
    with pytest.raises(KeyError):
        parse_configuration(f"{path_prefix}/missingpagination.yaml")


def test_yaml_missing_multiple() -> None:
    with pytest.raises(KeyError):
        parse_configuration(f"{path_prefix}/missingmultiple.yaml")
