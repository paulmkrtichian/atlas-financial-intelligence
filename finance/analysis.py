from datetime import date

from finance.tickers import get_company_by_ticker
from finance.sec_client import get_company_facts
from finance.statements import extract_financial_statements
from finance.calculations import (
    revenue_growth,
    operating_margin,
    current_ratio
)


def analyze_company(ticker, fiscal_year):
    """
    Retrieve a company's annual SEC data,
    verify reporting dates, and calculate ratios.
    """

    # 1. Identify the company
    company = get_company_by_ticker(ticker)

    # 2. Download its SEC financial data
    data = get_company_facts(company["cik"])

    # 3. Extract the requested year and previous year
    current = extract_financial_statements(
        data, fiscal_year
    )["metrics"]

    previous = extract_financial_statements(
        data, fiscal_year - 1
    )["metrics"]

    # 4. Check for missing information
    required_metrics = [
        "revenue",
        "operating_income",
        "net_income",
        "total_assets",
        "current_assets",
        "current_liabilities"
    ]

    for metric in required_metrics:
        if current[metric] is None:
            raise ValueError(
                f"Missing {metric} for FY {fiscal_year}."
            )

    if previous["revenue"] is None:
        raise ValueError(
            "Previous-year revenue is unavailable."
        )

    # 5. Check that all current-year dates match
    period_end = current["revenue"]["end"]

    if date.fromisoformat(period_end).year != fiscal_year:
        raise ValueError(
            "Reporting period does not match fiscal year."
        )

    for metric in required_metrics:
        if current[metric]["end"] != period_end:
            raise ValueError(
                f"Inconsistent reporting period: {metric}"
            )

    previous_end = previous["revenue"]["end"]

    if date.fromisoformat(previous_end).year != fiscal_year - 1:
        raise ValueError(
            "Previous-year reporting period is inconsistent."
        )

    # 6. Extract numerical values
    revenue = current["revenue"]["value"]
    previous_revenue = previous["revenue"]["value"]

    operating_income = current["operating_income"]["value"]

    current_assets = current["current_assets"]["value"]
    current_liabilities = current["current_liabilities"]["value"]

    # 7. Perform financial calculations
    results = {
        "company": company["name"],
        "ticker": company["ticker"],
        "cik": company["cik"],
        "fiscal_year": fiscal_year,
        "period_end": period_end,

        "revenue_growth": revenue_growth(
            revenue, previous_revenue
        ),

        "operating_margin": operating_margin(
            operating_income, revenue
        ),

        "current_ratio": current_ratio(
            current_assets, current_liabilities
        ),

        "financials": current
    }

    return results