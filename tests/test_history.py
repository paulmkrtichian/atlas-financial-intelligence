import pytest

import finance.history as history


def fake_statements(data, year):

    revenues = {
        2022: 100,
        2023: 120,
        2024: 150
    }

    revenue = revenues[year]

    end = f"{year}-06-30"
    start = f"{year - 1}-07-01"

    def fact(value, annual=False):
        return {
            "value": value,
            "end": end,
            "start": start if annual else None
        }

    return {
        "metrics": {
            "revenue": fact(revenue, True),
            "operating_income": fact(revenue * 0.2, True),
            "current_assets": fact(80),
            "current_liabilities": fact(40)
        }
    }


def setup_fake_sec(monkeypatch):

    calls = {"downloads": 0}

    monkeypatch.setattr(
        history,
        "get_company_by_ticker",
        lambda ticker: {
            "name": "Test Company",
            "ticker": "TEST",
            "cik": "0000000001"
        }
    )

    def fake_download(cik):
        calls["downloads"] += 1
        return {}

    monkeypatch.setattr(
        history,
        "get_company_facts",
        fake_download
    )

    monkeypatch.setattr(
        history,
        "extract_financial_statements",
        fake_statements
    )

    return calls


def test_three_year_history(monkeypatch):

    setup_fake_sec(monkeypatch)

    result = history.analyze_history("TEST", 2024, 3)

    rows = result["history"]

    assert len(rows) == 3
    assert [r["year"] for r in rows] == [2022, 2023, 2024]

    assert rows[0]["revenue_growth"] is None

    assert rows[1]["revenue_growth"] == pytest.approx(20)
    assert rows[2]["revenue_growth"] == pytest.approx(25)

    assert rows[2]["operating_margin"] == pytest.approx(20)


def test_sec_downloaded_once(monkeypatch):

    calls = setup_fake_sec(monkeypatch)

    history.analyze_history("TEST", 2024, 3)

    assert calls["downloads"] == 1


def test_invalid_year_count():

    with pytest.raises(ValueError):
        history.analyze_history("TEST", 2024, 1)
        