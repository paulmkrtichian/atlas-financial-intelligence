import pandas as pd
import re
from finance.importer import REQUIRED_COLUMNS


UNIT_MULTIPLIERS = {
    "USD": 1,
    "USD thousands": 1_000,
    "USD millions": 1_000_000
}


def map_financial_columns(data, mapping, unit="USD"):
    """
    Convert uploaded financial columns into
    Atlas's standardized financial format.
    """

    if unit not in UNIT_MULTIPLIERS:
        raise ValueError("Unsupported financial unit.")

    # Make sure every required metric is mapped
    missing = [
        column for column in REQUIRED_COLUMNS
        if column not in mapping
    ]

    if missing:
        raise ValueError(
            f"Missing column mappings: {missing}"
        )

    selected = [
        mapping[column]
        for column in REQUIRED_COLUMNS
    ]

    # Prevent one source column from being reused
    if len(selected) != len(set(selected)):
        raise ValueError(
            "Each financial metric needs a unique source column."
        )

    for column in selected:
        if column not in data.columns:
            raise ValueError(
                f"Source column not found: {column}"
            )

    # Select and rename the source columns
    result = data[selected].copy()
    result.columns = REQUIRED_COLUMNS

    # Validate the fiscal years
    result["fiscal_year"] = pd.to_numeric(
        result["fiscal_year"],
        errors="raise"
    )

    if result["fiscal_year"].isna().any():
        raise ValueError("Missing fiscal years.")

    if (result["fiscal_year"] % 1 != 0).any():
        raise ValueError("Fiscal years must be whole numbers.")

    result["fiscal_year"] = (
        result["fiscal_year"].astype(int)
    )

    if result["fiscal_year"].duplicated().any():
        raise ValueError("Duplicate fiscal years.")

    # Convert monetary amounts into actual USD
    financial_columns = [
        column for column in REQUIRED_COLUMNS
        if column != "fiscal_year"
    ]

    for column in financial_columns:
        result[column] = pd.to_numeric(
            result[column],
            errors="raise"
        )

    if result[financial_columns].isna().any().any():
        raise ValueError("Missing financial values.")

    multiplier = UNIT_MULTIPLIERS[unit]

    result[financial_columns] = (
        result[financial_columns] * multiplier
    )

    if (result["revenue"] <= 0).any():
        raise ValueError("Revenue must be positive.")

    if (result["capital_expenditures"] < 0).any():
        raise ValueError(
            "Capital expenditures must be nonnegative."
        )

    return result.sort_values(
        "fiscal_year"
    ).reset_index(drop=True)

COLUMN_ALIASES = {
    "fiscal_year": ["Year", "FY", "Fiscal Year"],
    "revenue": ["Sales", "Total Sales", "Net Sales", "Total Revenue"],
    "operating_income": ["EBIT", "Operating Profit"],
    "net_income": ["Net Earnings", "Net Profit"],
    "total_assets": ["Assets", "Total Assets"],
    "shareholders_equity": [
        "Owner Equity", "Owners Equity",
        "Stockholders Equity", "Total Equity"
    ],
    "current_assets": ["Short Term Assets"],
    "current_liabilities": ["Short Term Liabilities"],
    "operating_cash_flow": [
        "Cash From Operations",
        "Cash Flow From Operations",
        "Operating Cash"
    ],
    "capital_expenditures": [
        "CapEx",
        "Capital Spending",
        "Property Equipment Spending"
    ]
}


def normalize_column_name(name):
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def suggest_financial_mapping(columns):
    """
    Suggest column matches using recognized accounting labels.
    Never guess unknown columns.
    """

    suggestions = {}
    used_columns = set()

    for metric in REQUIRED_COLUMNS:

        accepted_names = [
            metric,
            *COLUMN_ALIASES.get(metric, [])
        ]

        normalized_names = {
            normalize_column_name(name)
            for name in accepted_names
        }

        matches = [
            column for column in columns
            if normalize_column_name(column) in normalized_names
        ]

        if len(matches) == 1 and matches[0] not in used_columns:
            suggestions[metric] = matches[0]
            used_columns.add(matches[0])

    return suggestions