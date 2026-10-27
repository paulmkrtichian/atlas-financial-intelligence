from agents.evidence_validator import validate_research_report


EVIDENCE = {
    "capital_expenditures_current": 8_000_000,
    "available_data": [
        "Revenue",
        "Operating income",
        "Capital expenditures"
    ],
    "industry_benchmarks": None,
    "current_ratio": 1.73
}


def test_detects_missing_capex_contradiction():

    report = (
        "Gross profit, capital expenditures, "
        "and debt details are unavailable."
    )

    issues = validate_research_report(report, EVIDENCE)

    codes = [issue["code"] for issue in issues]

    assert "CAPEX_CONTRADICTION" in codes


def test_detects_unsupported_benchmark():

    report = (
        "ROE of 21.54% outperforms typical industry benchmarks."
    )

    issues = validate_research_report(report, EVIDENCE)

    codes = [issue["code"] for issue in issues]

    assert "UNSUPPORTED_BENCHMARK" in codes


def test_detects_unsupported_causal_claim():

    report = (
        "Improved margins indicate operational efficiency gains."
    )

    issues = validate_research_report(report, EVIDENCE)

    codes = [issue["code"] for issue in issues]

    assert "UNSUPPORTED_CAUSAL_CLAIM" in codes


def test_detects_unsupported_liquidity_trend():

    report = (
        "The current ratio improved slightly to 1.73."
    )

    issues = validate_research_report(report, EVIDENCE)

    codes = [issue["code"] for issue in issues]

    assert "UNSUPPORTED_LIQUIDITY_TREND" in codes


def test_accepts_supported_observations():

    report = """
Revenue grew by 17.39%.
Operating margin rose to 23.70%.

Potential explanations include pricing changes
or cost optimization, but neither is verified.

Capital expenditures were $8 million.
"""

    issues = validate_research_report(report, EVIDENCE)

    assert issues == []

def test_detects_missing_liabilities_contradiction():

    evidence = {
        "available_data": [
            "Revenue",
            "Current liabilities"
        ]
    }

    report = (
        "The current ratio cannot be interpreted "
        "without current liabilities."
    )

    issues = validate_research_report(
        report,
        evidence
    )

    codes = [issue["code"] for issue in issues]

    assert "LIABILITIES_CONTRADICTION" in codes