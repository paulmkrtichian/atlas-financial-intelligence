
import pytest

from agents.financial_findings import build_financial_findings


EVIDENCE = {
    "revenue_current": 135_000_000,
    "revenue_previous": 115_000_000,
    "revenue_growth_pct": 17.39,
    "operating_margin_current_pct": 23.70,
    "operating_margin_change_pp": 1.96,
    "net_profit_margin_pct": 15.56,
    "net_profit_margin_change_pp": 1.64,
    "free_cash_flow_current": 21_000_000,
    "free_cash_flow_change": 4_000_000,
    "current_ratio": 1.73
}


def test_findings_generated():
    findings = build_financial_findings(EVIDENCE)
    assert len(findings) == 5


def test_revenue_finding():
    findings = build_financial_findings(EVIDENCE)
    revenue = findings[0]["finding"]

    assert "USD 135.00M" in revenue
    assert "17.39%" in revenue


def test_cash_flow_finding():
    findings = build_financial_findings(EVIDENCE)
    cash_flow = findings[3]["finding"]

    assert "USD 21.00M" in cash_flow
    assert "USD +4.00M" in cash_flow


def test_missing_evidence():
    incomplete = EVIDENCE.copy()
    del incomplete["revenue_current"]

    with pytest.raises(ValueError):
        build_financial_findings(incomplete)
