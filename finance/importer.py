from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = [
    "fiscal_year",
    "revenue",
    "operating_income",
    "net_income",
    "total_assets",
    "shareholders_equity",
    "current_assets",
    "current_liabilities",
    "operating_cash_flow",
    "capital_expenditures",
]


def import_financial_statements(file_path):
    """
    Import standardized financial statements
    from an Excel or CSV file.
    """

    # Accept both file paths and Streamlit uploads
    filename = (
        file_path.name
        if hasattr(file_path, "name")
        else str(file_path)
    )

    extension = Path(filename).suffix.lower()

    # Reset the reading position for uploaded files
    if hasattr(file_path, "seek"):
        file_path.seek(0)

    if extension == ".csv":
        data = pd.read_csv(file_path)

    elif extension == ".xlsx":
        data = pd.read_excel(file_path)

    else:
        raise ValueError(
            "Unsupported file format. Use CSV or XLSX."
        )


    # Standardize column names
    data.columns = [
        str(column).strip().lower()
        for column in data.columns
    ]

    # Check for missing financial metrics
    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing:
        raise ValueError(
            f"Missing financial columns: {missing}"
        )

    if data.empty:
        raise ValueError("The financial file is empty.")

    # Verify that every required value is numeric
    for column in REQUIRED_COLUMNS:
        data[column] = pd.to_numeric(
            data[column],
            errors="raise"
        )

    if data[REQUIRED_COLUMNS].isna().any().any():
        raise ValueError(
            "The file contains missing financial values."
        )

    # Require whole-number fiscal years
    if (data["fiscal_year"] % 1 != 0).any():
        raise ValueError("Fiscal years must be whole numbers.")

    data["fiscal_year"] = data["fiscal_year"].astype(int)

    if data["fiscal_year"].duplicated().any():
        raise ValueError("Duplicate fiscal years detected.")

    if (data["revenue"] <= 0).any():
        raise ValueError("Revenue must be positive.")

    if (data["capital_expenditures"] < 0).any():
        raise ValueError(
            "Capital expenditures must be nonnegative."
        )

    return data.sort_values(
        "fiscal_year"
    ).reset_index(drop=True)

def read_raw_financial_file(file):
    """
    Read a CSV or Excel file without requiring
    standardized financial column names.
    """

    filename = (
        file.name
        if hasattr(file, "name")
        else str(file)
    )

    extension = Path(filename).suffix.lower()

    if hasattr(file, "seek"):
        file.seek(0)

    if extension == ".csv":
        data = pd.read_csv(file)

    elif extension == ".xlsx":
        data = pd.read_excel(file)

    else:
        raise ValueError(
            "Only CSV and XLSX files are supported."
        )

    if data.empty:
        raise ValueError("The uploaded file is empty.")

    data.columns = [
        str(column).strip()
        for column in data.columns
    ]

    if data.columns.duplicated().any():
        raise ValueError(
            "Duplicate column names were detected."
        )

    return data