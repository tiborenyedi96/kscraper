from pathlib import Path

import pytest
import yaml
from parser import parse_configuration

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_parser() -> None:
    assert parse_configuration(str(FIXTURES_DIR / "mock.yaml")) == {
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
        parse_configuration(str(FIXTURES_DIR / "error.yaml"))


def test_yaml_missing_url() -> None:
    with pytest.raises(KeyError):
        parse_configuration(str(FIXTURES_DIR / "missingurl.yaml"))


def test_yaml_missing_limiter() -> None:
    with pytest.raises(KeyError):
        parse_configuration(str(FIXTURES_DIR / "missinglimiter.yaml"))


def test_yaml_missing_fields() -> None:
    with pytest.raises(KeyError):
        parse_configuration(str(FIXTURES_DIR / "missingfields.yaml"))


def test_yaml_missing_pagination() -> None:
    with pytest.raises(KeyError):
        parse_configuration(str(FIXTURES_DIR / "missingpagination.yaml"))


def test_yaml_missing_multiple() -> None:
    with pytest.raises(KeyError):
        parse_configuration(str(FIXTURES_DIR / "missingmultiple.yaml"))
