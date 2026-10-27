from datetime import date

from finance.tickers import get_company_by_ticker
from finance.sec_client import get_company_facts
from finance.statements import extract_financial_statements

from finance.calculations import (
    net_profit_margin,
    return_on_assets,
    return_on_equity,
    free_cash_flow
)


def require_fact(metrics, name, year):
    """
    Return a required SEC financial fact.
    """

    fact = metrics.get(name)

    if fact is None:
        raise ValueError(
            f"Missing {name} for fiscal year {year}."
        )

    return fact


def validate_annual(fact, start, end, name):
    """
    Verify a full-year financial reporting period.
    """

    if fact.get("start") != start or fact.get("end") != end:
        raise ValueError(
            f"Inconsistent reporting period for {name}."
        )

    duration = (
        date.fromisoformat(end)
        - date.fromisoformat(start)
    ).days

    if not 330 <= duration <= 380:
        raise ValueError(
            f"{name} does not cover a full fiscal year."
        )


def analyze_profitability(ticker, fiscal_year):
    """
    Analyze profitability and cash flow using SEC data.
    """

    # Identify the company
    company = get_company_by_ticker(ticker)

    # Download SEC data once
    data = get_company_facts(company["cik"])

    # Extract current and previous fiscal years
    current = extract_financial_statements(
        data, fiscal_year
    )["metrics"]

    previous = extract_financial_statements(
        data, fiscal_year - 1
    )["metrics"]

    # Current-year financial facts
    required_current = [
        "revenue",
        "net_income",
        "total_assets",
        "shareholders_equity",
        "operating_cash_flow",
        "capital_expenditures"
    ]

    facts = {
        name: require_fact(current, name, fiscal_year)
        for name in required_current
    }

    # Prior-year balance sheet facts
    previous_assets = require_fact(
        previous, "total_assets", fiscal_year - 1
    )

    previous_equity = require_fact(
        previous, "shareholders_equity", fiscal_year - 1
    )

    # Establish the fiscal-year dates
    revenue_fact = facts["revenue"]

    start = revenue_fact.get("start")
    end = revenue_fact.get("end")

    if not start or not end:
        raise ValueError("Missing fiscal-year reporting dates.")

    if date.fromisoformat(end).year != fiscal_year:
        raise ValueError("Incorrect fiscal-year ending date.")

    # Verify annual income and cash flow periods
    for name in [
        "revenue",
        "net_income",
        "operating_cash_flow",
        "capital_expenditures"
    ]:
        validate_annual(facts[name], start, end, name)

    # Verify current balance sheet dates
    for name in ["total_assets", "shareholders_equity"]:
        if facts[name]["end"] != end:
            raise ValueError(
                f"Inconsistent balance sheet date for {name}."
            )

    # Verify previous-year balance sheet dates
    prior_end = previous_assets["end"]

    if previous_equity["end"] != prior_end:
        raise ValueError("Previous balance sheet dates differ.")

    days_between = (
        date.fromisoformat(end)
        - date.fromisoformat(prior_end)
    ).days

    if not 330 <= days_between <= 380:
        raise ValueError(
            "Previous balance sheet is not one fiscal year earlier."
        )

    # Extract numerical values
    revenue = facts["revenue"]["value"]
    net_income = facts["net_income"]["value"]

    assets = facts["total_assets"]["value"]
    equity = facts["shareholders_equity"]["value"]

    operating_cash_flow = facts["operating_cash_flow"]["value"]
    capital_expenditures = facts["capital_expenditures"]["value"]

    # Perform deterministic calculations
    return {
        "company": company["name"],
        "ticker": company["ticker"],
        "cik": company["cik"],
        "fiscal_year": fiscal_year,
        "period_end": end,

        "net_profit_margin": net_profit_margin(
            net_income, revenue
        ),

        "return_on_assets": return_on_assets(
            net_income,
            previous_assets["value"],
            assets
        ),

        "return_on_equity": return_on_equity(
            net_income,
            previous_equity["value"],
            equity
        ),

        "free_cash_flow": free_cash_flow(
            operating_cash_flow,
            capital_expenditures
        ),

        "operating_cash_flow": operating_cash_flow,
        "capital_expenditures": capital_expenditures,

        "sources": {
            **facts,
            "previous_assets": previous_assets,
            "previous_equity": previous_equity
        }
    }