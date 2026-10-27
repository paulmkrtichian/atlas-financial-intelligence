import requests

from finance.sec_client import HEADERS


TICKER_URL = "https://www.sec.gov/files/company_tickers.json"


def get_ticker_directory():
    """
    Download the SEC's ticker-to-company directory.
    """

    headers = {
        "User-Agent": HEADERS["User-Agent"],
        "Accept": "application/json"
    }

    response = requests.get(
        TICKER_URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def find_company(ticker, directory):
    """
    Find a company by its stock ticker.
    """

    ticker = ticker.strip().upper()

    if not ticker:
        raise ValueError("Please enter a stock ticker.")

    for company in directory.values():

        if company["ticker"].upper() == ticker:

            return {
                "ticker": company["ticker"],
                "name": company["title"],
                "cik": str(company["cik_str"]).zfill(10)
            }

    raise ValueError(
        f"Ticker '{ticker}' was not found in the SEC directory."
    )


def get_company_by_ticker(ticker):
    """
    Download the directory and identify a company.
    """

    directory = get_ticker_directory()

    return find_company(ticker, directory)