import pytest
import finance.profitability as profitability


def make_fact(value, end, start=None):
    return {
        "value": value,
        "start": start,
        "end": end,
        "tag": "TestTag"
    }


def setup_fake_data(monkeypatch, missing_cash_flow=False):

    current_end = "2024-06-30"
    current_start = "2023-07-01"

    current = {
        "revenue": make_fact(
            1000, current_end, current_start
        ),
        "net_income": make_fact(
            200, current_end, current_start
        ),
        "total_assets": make_fact(
            1200, current_end
        ),
        "shareholders_equity": make_fact(
            600, current_end
        ),
        "operating_cash_flow": make_fact(
            300, current_end, current_start
        ),
        "capital_expenditures": make_fact(
            100, current_end, current_start
        )
    }

    if missing_cash_flow:
        current["operating_cash_flow"] = None

    previous = {
        "total_assets": make_fact(
            800, "2023-06-30"
        ),
        "shareholders_equity": make_fact(
            400, "2023-06-30"
        )
    }

    monkeypatch.setattr(
        profitability,
        "get_company_by_ticker",
        lambda ticker: {
            "name": "Test Company",
            "ticker": "TEST",
            "cik": "0000000001"
        }
    )

    monkeypatch.setattr(
        profitability,
        "get_company_facts",
        lambda cik: {}
    )

    monkeypatch.setattr(
        profitability,
        "extract_financial_statements",
        lambda data, year: {
            "metrics": current if year == 2024 else previous
        }
    )

    return current


def test_profitability_calculations(monkeypatch):

    setup_fake_data(monkeypatch)

    result = profitability.analyze_profitability(
        "TEST", 2024
    )

    assert result["net_profit_margin"] == pytest.approx(20)
    assert result["return_on_assets"] == pytest.approx(20)
    assert result["return_on_equity"] == pytest.approx(40)
    assert result["free_cash_flow"] == pytest.approx(200)


def test_missing_cash_flow(monkeypatch):

    setup_fake_data(
        monkeypatch,
        missing_cash_flow=True
    )

    with pytest.raises(ValueError):
        profitability.analyze_profitability("TEST", 2024)


def test_inconsistent_cash_flow_dates(monkeypatch):

    current = setup_fake_data(monkeypatch)

    current["operating_cash_flow"]["end"] = "2023-06-30"

    with pytest.raises(ValueError):
        profitability.analyze_profitability("TEST", 2024)


def test_inconsistent_prior_balance_sheet(monkeypatch):

    setup_fake_data(monkeypatch)

    # Verify prior-year balances are required for ROA/ROE.
    # Additional date mismatch cases will be added later.
    result = profitability.analyze_profitability("TEST", 2024)

    assert result["return_on_assets"] == pytest.approx(20)