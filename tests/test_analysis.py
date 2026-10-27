import pytest

import finance.analysis as analysis


def make_fact(value, end="2024-06-30"):
    return {
        "value": value,
        "end": end
    }


def test_company_analysis(monkeypatch):

    current = {
        "revenue": make_fact(200),
        "operating_income": make_fact(50),
        "net_income": make_fact(30),
        "total_assets": make_fact(300),
        "current_assets": make_fact(80),
        "current_liabilities": make_fact(40)
    }

    previous = {
        "revenue": make_fact(160, "2023-06-30")
    }

    monkeypatch.setattr(
        analysis,
        "get_company_by_ticker",
        lambda ticker: {
            "name": "Test Company",
            "ticker": "TEST",
            "cik": "0000000001"
        }
    )

    monkeypatch.setattr(
        analysis,
        "get_company_facts",
        lambda cik: {}
    )

    monkeypatch.setattr(
        analysis,
        "extract_financial_statements",
        lambda data, year: {
            "metrics": current if year == 2024 else previous
        }
    )

    result = analysis.analyze_company("TEST", 2024)

    assert result["revenue_growth"] == pytest.approx(25)
    assert result["operating_margin"] == pytest.approx(25)
    assert result["current_ratio"] == pytest.approx(2)


def test_missing_financial_data(monkeypatch):

    monkeypatch.setattr(
        analysis,
        "get_company_by_ticker",
        lambda ticker: {
            "name": "Test Company",
            "ticker": "TEST",
            "cik": "0000000001"
        }
    )

    monkeypatch.setattr(
        analysis,
        "get_company_facts",
        lambda cik: {}
    )

    monkeypatch.setattr(
        analysis,
        "extract_financial_statements",
        lambda data, year: {
            "metrics": {
                "revenue": None,
                "operating_income": None,
                "net_income": None,
                "total_assets": None,
                "current_assets": None,
                "current_liabilities": None
            }
        }
    )

    with pytest.raises(ValueError):
        analysis.analyze_company("TEST", 2024)


def test_inconsistent_reporting_dates(monkeypatch):

    current = {
        "revenue": make_fact(200),
        "operating_income": make_fact(50, "2023-06-30"),
        "net_income": make_fact(30),
        "total_assets": make_fact(300),
        "current_assets": make_fact(80),
        "current_liabilities": make_fact(40)
    }

    previous = {
        "revenue": make_fact(160, "2023-06-30")
    }

    monkeypatch.setattr(
        analysis,
        "get_company_by_ticker",
        lambda ticker: {
            "name": "Test Company",
            "ticker": "TEST",
            "cik": "0000000001"
        }
    )

    monkeypatch.setattr(
        analysis,
        "get_company_facts",
        lambda cik: {}
    )

    monkeypatch.setattr(
        analysis,
        "extract_financial_statements",
        lambda data, year: {
            "metrics": current if year == 2024 else previous
        }
    )

    with pytest.raises(ValueError):
        analysis.analyze_company("TEST", 2024)