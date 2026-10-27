from datetime import date


# Financial metrics and their SEC accounting tags
FINANCIAL_TAGS = {
    "revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
        "SalesRevenueNet",
    ],
    "operating_income": [
        "OperatingIncomeLoss",
    ],
    "net_income": [
        "NetIncomeLoss",
    ],
    "total_assets": [
        "Assets",
    ],
    "current_assets": [
        "AssetsCurrent",
    ],
    "current_liabilities": [
        "LiabilitiesCurrent",
    ],
        "shareholders_equity": [
        "StockholdersEquity",
    ],

    "operating_cash_flow": [
        "NetCashProvidedByUsedInOperatingActivities",
    ],

    "capital_expenditures": [
    "PaymentsToAcquirePropertyPlantAndEquipment",
    "PaymentsToAcquireProductiveAssets",
    ],

    
}


def get_annual_fact(company_facts, tags, fiscal_year):
    """
    Find a financial value reported for a specific fiscal year.

    Only accepts:
    - Original annual 10-K filings
    - USD values
    - Facts matching the requested fiscal year
    - Full-year income statement values
    """

    gaap = company_facts.get("facts", {}).get("us-gaap", {})

    for tag in tags:

        if tag not in gaap:
            continue

        entries = gaap[tag].get("units", {}).get("USD", [])

        matches = []

        for entry in entries:

            if entry.get("form") != "10-K":
                continue

            if entry.get("fp") != "FY":
                continue
            # Verify the actual reporting period
            period_end = date.fromisoformat(entry["end"])

            if period_end.year != fiscal_year:
                continue
            if entry.get("end") is None:
                continue

            # Duration facts must cover approximately one year.
            # Balance sheet facts have no start date.
            if "start" in entry:

                start = date.fromisoformat(entry["start"])
                end = date.fromisoformat(entry["end"])

                duration = (end - start).days

                if not 330 <= duration <= 380:
                    continue

            matches.append(entry)

        if matches:

            # Prefer the most recently filed matching fact.
            selected = max(
                matches,
                key=lambda item: item.get("filed", "")
            )

            return {
                "value": selected["val"],
                "tag": tag,
                "start": selected.get("start"),
                "end": selected["end"],
                "filed": selected.get("filed"),
                "accession": selected.get("accn"),
            }

    return None


def extract_financial_statements(company_facts, fiscal_year):
    """
    Extract key financial figures for a fiscal year.
    """

    results = {
        "company": company_facts.get("entityName"),
        "fiscal_year": fiscal_year,
        "metrics": {}
    }

    for metric, tags in FINANCIAL_TAGS.items():

        results["metrics"][metric] = get_annual_fact(
            company_facts,
            tags,
            fiscal_year
        )

    return results