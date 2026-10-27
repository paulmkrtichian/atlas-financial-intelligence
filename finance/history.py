from datetime import date

from finance.tickers import get_company_by_ticker
from finance.sec_client import get_company_facts
from finance.statements import extract_financial_statements

from finance.calculations import (
    revenue_growth,
    operating_margin,
    current_ratio
)


def analyze_history(ticker, end_year=2024, years=5):
    """
    Analyze multiple fiscal years of company financial data.

    Retrieves SEC data once and processes each requested year.
    """

    if not isinstance(years, int) or not 2 <= years <= 10:
        raise ValueError("Choose between 2 and 10 years.")

    # Identify company
    company = get_company_by_ticker(ticker)

    # Download financial facts ONCE
    data = get_company_facts(company["cik"])

    start_year = end_year - years + 1

    history = []
    previous_revenue = None

    for year in range(start_year, end_year + 1):

        # Extract financial information for this year
        statements = extract_financial_statements(
            data, year
        )

        metrics = statements["metrics"]

        # Revenue and operating income are required
        for name in ["revenue", "operating_income"]:

            if metrics.get(name) is None:
                raise ValueError(
                    f"Missing {name} for fiscal year {year}."
                )

        revenue_fact = metrics["revenue"]
        operating_fact = metrics["operating_income"]

        period_end = revenue_fact["end"]

        # Verify fiscal year
        if date.fromisoformat(period_end).year != year:
            raise ValueError(
                f"Incorrect reporting year for FY {year}."
            )

        # Validate full-year income statement periods
        for name in ["revenue", "operating_income"]:

            fact = metrics[name]

            if fact["end"] != period_end:
                raise ValueError(
                    f"Inconsistent {name} period in FY {year}."
                )

            if not fact.get("start"):
                raise ValueError(
                    f"Missing annual period start for {name}."
                )

            duration = (
                date.fromisoformat(fact["end"])
                - date.fromisoformat(fact["start"])
            ).days

            if not 330 <= duration <= 380:
                raise ValueError(
                    f"{name} is not a full-year value in FY {year}."
                )

        revenue = revenue_fact["value"]
        operating_income = operating_fact["value"]

        # Calculate annual revenue growth
        if previous_revenue is None:
            growth = None
        else:
            growth = revenue_growth(
                revenue,
                previous_revenue
            )

        margin = operating_margin(
            operating_income,
            revenue
        )

        # Current ratio is unavailable for some companies
        assets_fact = metrics.get("current_assets")
        liabilities_fact = metrics.get("current_liabilities")

        liquidity = None

        if assets_fact and liabilities_fact:

            if (
                assets_fact["end"] != period_end
                or liabilities_fact["end"] != period_end
            ):
                raise ValueError(
                    f"Inconsistent balance sheet dates in FY {year}."
                )

            if liabilities_fact["value"] > 0:
                liquidity = current_ratio(
                    assets_fact["value"],
                    liabilities_fact["value"]
                )

        # Save this fiscal year's results
        history.append({
            "year": year,
            "period_end": period_end,
            "revenue": revenue,
            "operating_income": operating_income,
            "revenue_growth": growth,
            "operating_margin": margin,
            "current_ratio": liquidity,
            "revenue_source": revenue_fact,
            "operating_income_source": operating_fact
        })

        previous_revenue = revenue

    return {
        "company": company["name"],
        "ticker": company["ticker"],
        "cik": company["cik"],
        "history": history
    }