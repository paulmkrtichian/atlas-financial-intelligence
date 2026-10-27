from finance.analysis import analyze_company
from finance.profitability import analyze_profitability


def compare_companies(ticker_a, ticker_b, fiscal_year):
    """
    Compare two companies using SEC financial data.
    """

    # Standardize ticker inputs
    ticker_a = ticker_a.strip().upper()
    ticker_b = ticker_b.strip().upper()

    if not ticker_a or not ticker_b:
        raise ValueError("Both company tickers are required.")

    if ticker_a == ticker_b:
        raise ValueError(
            "Please select two different companies."
        )

    results = []

    # Analyze each company
    for ticker in [ticker_a, ticker_b]:

        financial = analyze_company(
            ticker, fiscal_year
        )

        profitability = analyze_profitability(
            ticker, fiscal_year
        )

        # Verify both analyses refer to the same company
        if financial["cik"] != profitability["cik"]:
            raise ValueError(
                f"Company identifier mismatch for {ticker}."
            )

        # Verify both analyses use the same reporting period
        if financial["period_end"] != profitability["period_end"]:
            raise ValueError(
                f"Reporting period mismatch for {ticker}."
            )

        # Combine the financial metrics
        company_result = {
            "company": financial["company"],
            "ticker": financial["ticker"],
            "cik": financial["cik"],
            "fiscal_year": fiscal_year,
            "period_end": financial["period_end"],

            "revenue_growth": financial["revenue_growth"],
            "operating_margin": financial["operating_margin"],
            "current_ratio": financial["current_ratio"],

            "net_profit_margin": profitability["net_profit_margin"],
            "return_on_assets": profitability["return_on_assets"],
            "return_on_equity": profitability["return_on_equity"],
            "free_cash_flow": profitability["free_cash_flow"]
        }

        results.append(company_result)

    return {
        "fiscal_year": fiscal_year,
        "companies": results
    }