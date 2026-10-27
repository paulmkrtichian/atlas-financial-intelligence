import pytest

from finance.tickers import find_company


SAMPLE_DIRECTORY = {
    "0": {
        "cik_str": 320193,
        "ticker": "AAPL",
        "title": "Apple Inc."
    },
    "1": {
        "cik_str": 789019,
        "ticker": "MSFT",
        "title": "Microsoft Corporation"
    }
}


def test_find_apple():
    result = find_company("AAPL", SAMPLE_DIRECTORY)

    assert result["name"] == "Apple Inc."
    assert result["cik"] == "0000320193"


def test_lowercase_ticker():
    result = find_company("msft", SAMPLE_DIRECTORY)

    assert result["ticker"] == "MSFT"


def test_invalid_ticker():
    with pytest.raises(ValueError):
        find_company("INVALID", SAMPLE_DIRECTORY)


def test_empty_ticker():
    with pytest.raises(ValueError):
        find_company("", SAMPLE_DIRECTORY)