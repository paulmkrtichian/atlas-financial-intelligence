import pandas as pd
import pytest

from finance.private_analysis import analyze_private_company


SAMPLE_DATA = pd.DataFrame({
    "fiscal_year": [2024, 2025],
    "revenue": [100, 120],
    "operating_income": [20, 30],
    "net_income": [10, 18],
    "total_assets": [150, 180],
    "shareholders_equity": [80, 100],
    "current_assets": [40, 60],
    "current_liabilities": [20, 30],
    "operating_cash_flow": [15, 25],
    "capital_expenditures": [5, 8]
})


def test_private_company_growth():

    result = analyze_private_company(
        SAMPLE_DATA, 2025
    )

    assert result["revenue_growth"] == pytest.approx(20)


def test_private_company_profitability():

    result = analyze_private_company(
        SAMPLE_DATA, 2025
    )

    assert result["operating_margin"] == pytest.approx(25)
    assert result["net_profit_margin"] == pytest.approx(15)

    assert result["return_on_assets"] == pytest.approx(
        18 / 165 * 100
    )


def test_private_company_cash_flow():

    result = analyze_private_company(
        SAMPLE_DATA, 2025
    )

    assert result["free_cash_flow"] == pytest.approx(17)


def test_missing_previous_year():

    with pytest.raises(ValueError):
        analyze_private_company(
            SAMPLE_DATA, 2024
        )