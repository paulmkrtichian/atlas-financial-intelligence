import pandas as pd
import pytest

from finance.importer import import_financial_statements


SAMPLE_DATA = {
    "fiscal_year": [2023, 2024],
    "revenue": [100000000, 115000000],
    "operating_income": [20000000, 25000000],
    "net_income": [12000000, 16000000],
    "total_assets": [150000000, 170000000],
    "shareholders_equity": [80000000, 90000000],
    "current_assets": [40000000, 45000000],
    "current_liabilities": [25000000, 27000000],
    "operating_cash_flow": [18000000, 23000000],
    "capital_expenditures": [5000000, 6000000],
}


def test_csv_import(tmp_path):

    path = tmp_path / "company.csv"

    pd.DataFrame(SAMPLE_DATA).to_csv(path, index=False)

    result = import_financial_statements(path)

    assert len(result) == 2
    assert result.iloc[1]["revenue"] == 115000000


def test_excel_import(tmp_path):

    path = tmp_path / "company.xlsx"

    pd.DataFrame(SAMPLE_DATA).to_excel(path, index=False)

    result = import_financial_statements(path)

    assert len(result) == 2
    assert result.iloc[0]["fiscal_year"] == 2023


def test_missing_column(tmp_path):

    path = tmp_path / "invalid.csv"

    data = pd.DataFrame(SAMPLE_DATA).drop(
        columns=["operating_cash_flow"]
    )

    data.to_csv(path, index=False)

    with pytest.raises(ValueError):
        import_financial_statements(path)


def test_duplicate_years(tmp_path):

    path = tmp_path / "duplicate.csv"

    data = pd.DataFrame(SAMPLE_DATA)

    data["fiscal_year"] = [2024, 2024]

    data.to_csv(path, index=False)

    with pytest.raises(ValueError):
        import_financial_statements(path)