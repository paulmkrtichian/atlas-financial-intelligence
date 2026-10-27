from finance.calculations import (
    revenue_growth,
    operating_margin,
    net_profit_margin,
    current_ratio,
    return_on_assets,
    return_on_equity,
    free_cash_flow
)


def analyze_private_company(data, fiscal_year):
    """
    Analyze imported private-company financial statements.

    data: Validated Pandas DataFrame from importer.py
    fiscal_year: Year to analyze
    """

    fiscal_year = int(fiscal_year)

    # Find current-year financial information
    current_rows = data[
        data["fiscal_year"] == fiscal_year
    ]

    # Find previous-year financial information
    previous_rows = data[
        data["fiscal_year"] == fiscal_year - 1
    ]

    if current_rows.empty:
        raise ValueError(
            f"No financial data found for FY {fiscal_year}."
        )

    if previous_rows.empty:
        raise ValueError(
            f"FY {fiscal_year - 1} is required "
            "to calculate growth, ROA, and ROE."
        )

    current = current_rows.iloc[0]
    previous = previous_rows.iloc[0]

    # Extract financial values
    revenue = current["revenue"]
    previous_revenue = previous["revenue"]

    operating_income = current["operating_income"]
    net_income = current["net_income"]

    current_assets = current["current_assets"]
    current_liabilities = current["current_liabilities"]

    total_assets = current["total_assets"]
    previous_assets = previous["total_assets"]

    equity = current["shareholders_equity"]
    previous_equity = previous["shareholders_equity"]

    operating_cash_flow = current["operating_cash_flow"]
    capital_expenditures = current["capital_expenditures"]

    # Calculate metrics using our existing functions
    results = {
        "fiscal_year": fiscal_year,

        "revenue": float(revenue),
        "net_income": float(net_income),

        "revenue_growth": revenue_growth(
            revenue,
            previous_revenue
        ),

        "operating_margin": operating_margin(
            operating_income,
            revenue
        ),

        "net_profit_margin": net_profit_margin(
            net_income,
            revenue
        ),

        "current_ratio": current_ratio(
            current_assets,
            current_liabilities
        ),

        "return_on_assets": return_on_assets(
            net_income,
            previous_assets,
            total_assets
        ),

        "return_on_equity": return_on_equity(
            net_income,
            previous_equity,
            equity
        ),

        "free_cash_flow": free_cash_flow(
            operating_cash_flow,
            capital_expenditures
        )
    }

    return results