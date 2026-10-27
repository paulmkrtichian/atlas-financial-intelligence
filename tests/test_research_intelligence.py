import pandas as pd
import pytest

from agents import research_intelligence


SAMPLE_DATA = pd.DataFrame({
    "fiscal_year": [2024, 2025],
    "revenue": [115_000_000, 135_000_000],
    "operating_income": [25_000_000, 32_000_000],
    "net_income": [16_000_000, 21_000_000],
    "total_assets": [170_000_000, 195_000_000],
    "shareholders_equity": [90_000_000, 105_000_000],
    "current_assets": [45_000_000, 52_000_000],
    "current_liabilities": [27_000_000, 30_000_000],
    "operating_cash_flow": [23_000_000, 29_000_000],
    "capital_expenditures": [6_000_000, 8_000_000]
})


def test_revenue_growth_evidence():

    evidence = research_intelligence.extract_financial_evidence(
        SAMPLE_DATA, 2025
    )

    assert evidence["revenue_growth_pct"] == pytest.approx(
        17.39
    )


def test_operating_margin_change():

    evidence = research_intelligence.extract_financial_evidence(
        SAMPLE_DATA, 2025
    )

    assert evidence["operating_margin_change_pp"] == pytest.approx(
        1.96
    )


def test_cash_flow_change():

    evidence = research_intelligence.extract_financial_evidence(
        SAMPLE_DATA, 2025
    )

    assert evidence["free_cash_flow_change"] == pytest.approx(
        4_000_000
    )


def test_ai_receives_financial_evidence(monkeypatch):

    captured = {}

    def fake_ai(prompt):
        captured["prompt"] = prompt
        return "Mock financial research report."

    monkeypatch.setattr(
        research_intelligence,
        "ask_atlas",
        fake_ai
    )

    result = research_intelligence.generate_financial_research(
        SAMPLE_DATA,
        "Test Manufacturing Co.",
        2025
    )

    assert result["report"] == "Mock financial research report."

    assert "17.39" in captured["prompt"]
    assert "Test Manufacturing Co." in captured["prompt"]


def test_missing_previous_year():

    with pytest.raises(ValueError):
        research_intelligence.extract_financial_evidence(
            SAMPLE_DATA, 2024
        )
def test_research_report_is_validated(monkeypatch):

    def fake_ai(prompt):
        return (
            "ROE outperforms typical industry benchmarks.\n"
            "Capital expenditures are unavailable."
        )

    monkeypatch.setattr(
        research_intelligence,
        "ask_atlas",
        fake_ai
    )

    result = research_intelligence.generate_financial_research(
        SAMPLE_DATA,
        "Test Manufacturing Co.",
        2025
    )

    assert "validation_issues" in result

    codes = [
        issue["code"]
        for issue in result["validation_issues"]
    ]

    assert "UNSUPPORTED_BENCHMARK" in codes
    assert "CAPEX_CONTRADICTION" in codes

    assert result["validation_warning_count"] == len(
        result["validation_issues"]
    )