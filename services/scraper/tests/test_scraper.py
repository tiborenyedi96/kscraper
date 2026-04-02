import pytest
import requests
from unittest.mock import patch, MagicMock
from scraper import scrape

CONFIG = {
    "url": "http://example.com",
    "pagination": "{url}?page={page}",
    "limiter": 3,
    "fields": {
        "title": {"tag": "a", "attribute": "href"},
        "price": {"tag": "p", "text": True, "remove": "$"},
    },
}

HTML_PAGE = b"""
<html>
  <a href="http://item1.com">Item 1</a>
  <p>$10.00</p>
</html>
"""


def make_response(status_code=200, content=HTML_PAGE):
    mock = MagicMock()
    mock.status_code = status_code
    mock.content = content
    return mock


@patch("scraper.requests.get")
def test_scrape_returns_items(mock_get):
    mock_get.return_value = make_response()
    result = scrape({**CONFIG, "limiter": 1})
    assert result == [{"title": "http://item1.com", "price": "10.00"}]


@patch("scraper.requests.get")
def test_scrape_stops_on_non_200(mock_get):
    mock_get.return_value = make_response(status_code=404)
    result = scrape(CONFIG)
    assert result == []
    mock_get.assert_called_once()


@patch("scraper.requests.get")
def test_scrape_multi_page(mock_get):
    mock_get.side_effect = [
        make_response(200),
        make_response(200),
        make_response(404),
    ]
    result = scrape(CONFIG)
    assert len(result) == 2


@patch("scraper.requests.get")
def test_scrape_network_error_propagates(mock_get):
    mock_get.side_effect = requests.ConnectionError("unreachable")
    with pytest.raises(requests.ConnectionError):
        scrape(CONFIG)


@patch("scraper.requests.get")
def test_scrape_uses_pagination_url(mock_get):
    mock_get.return_value = make_response(404)
    scrape({**CONFIG, "limiter": 3})
    mock_get.assert_called_once_with("http://example.com?page=1")
