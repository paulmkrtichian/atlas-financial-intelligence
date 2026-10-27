import pytest
import finance.comparison as comparison


def setup_fake_companies(monkeypatch):

    companies = {
        "MSFT": {
            "name": "Microsoft",
            "cik": "0000789019",
            "end": "2024-06-30",
            "growth": 15.67
        },
        "AAPL": {
            "name": "Apple",
            "cik": "0000320193",
            "end": "2024-09-28",
            "growth": 2.02
        }
    }

    def fake_analysis(ticker, year):
        company = companies[ticker]

        return {
            "company": company["name"],
            "ticker": ticker,
            "cik": company["cik"],
            "period_end": company["end"],
            "revenue_growth": company["growth"],
            "operating_margin": 30,
            "current_ratio": 1.5
        }

    def fake_profitability(ticker, year):
        company = companies[ticker]

        return {
            "cik": company["cik"],
            "period_end": company["end"],
            "net_profit_margin": 20,
            "return_on_assets": 10,
            "return_on_equity": 25,
            "free_cash_flow": 100_000_000_000
        }

    monkeypatch.setattr(
        comparison,
        "analyze_company",
        fake_analysis
    )

    monkeypatch.setattr(
        comparison,
        "analyze_profitability",
        fake_profitability
    )


def test_two_company_comparison(monkeypatch):

    setup_fake_companies(monkeypatch)

    result = comparison.compare_companies(
        "MSFT", "AAPL", 2024
    )

    assert len(result["companies"]) == 2

    assert result["companies"][0]["ticker"] == "MSFT"
    assert result["companies"][1]["ticker"] == "AAPL"

    assert result["companies"][0]["revenue_growth"] == pytest.approx(15.67)

    assert result["companies"][1]["revenue_growth"] == pytest.approx(2.02)


def test_lowercase_tickers(monkeypatch):

    setup_fake_companies(monkeypatch)

    result = comparison.compare_companies(
        "msft", "aapl", 2024
    )

    assert result["companies"][0]["ticker"] == "MSFT"


def test_duplicate_companies():

    with pytest.raises(ValueError):
        comparison.compare_companies(
            "AAPL", "AAPL", 2024
        )


def test_empty_ticker():

    with pytest.raises(ValueError):
        comparison.compare_companies(
            "", "MSFT", 2024
        )