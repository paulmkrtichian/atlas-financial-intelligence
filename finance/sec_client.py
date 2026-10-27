import requests


BASE_URL = "https://data.sec.gov/api/xbrl/companyfacts"

HEADERS = {
    "User-Agent": "AtlasAI Research paulmkr22@gmail.com",
    "Accept-Encoding": "gzip, deflate",
    "Host": "data.sec.gov"
}


def get_company_facts(cik):
    """
    Retrieve reported financial data from the SEC.
    """

    cik = str(cik).zfill(10)

    url = f"{BASE_URL}/CIK{cik}.json"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    return response.json()