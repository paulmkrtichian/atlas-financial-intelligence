import pandas as pd
import pytest

from agents.financial_tool_agent import execute_financial_tool


@pytest.fixture
def sample_data():

    return pd.DataFrame({
        "fiscal_year": [2024, 2025],
        "revenue": [115_000_000, 135_000_000],
        "operating_income": [25_000_000, 32_000_000],
        "net_income": [16_000_000, 21_000_000]
    })


def test_revenue_growth(sample_data):

    result = execute_financial_tool(
        "revenue_growth",
        sample_data,
        2025
    )

    assert result["revenue_growth_pct"] == pytest.approx(
        17.3913043478
    )


def test_operating_margin(sample_data):

    result = execute_financial_tool(
        "operating_margin",
        sample_data,
        2025
    )

    assert result["operating_margin_pct"] == pytest.approx(
        23.7037037037
    )


def test_net_margin(sample_data):

    result = execute_financial_tool(
        "net_margin",
        sample_data,
        2025
    )

    assert result["net_margin_pct"] == pytest.approx(
        15.5555555556
    )


def test_financial_summary(sample_data):

    result = execute_financial_tool(
        "financial_summary",
        sample_data,
        2025
    )

    assert result["revenue"] == 135_000_000
    assert result["operating_income"] == 32_000_000
    assert result["net_income"] == 21_000_000


def test_missing_previous_year(sample_data):

    with pytest.raises(ValueError):

        execute_financial_tool(
            "revenue_growth",
            sample_data,
            2024
        )


def test_unsupported_tool(sample_data):

    with pytest.raises(ValueError):

        execute_financial_tool(
            "invented_tool",
            sample_data,
            2025
        )