import re


def validate_research_report(report, evidence):
    """
    Find selected unsupported claims in an AI research report.

    Returns a list of warnings for human review.
    This is not a complete financial fact-checker.
    """

    issues = []

    capex_available = (
        evidence.get("capital_expenditures_current") is not None
        or "Capital expenditures" in evidence.get(
            "available_data", []
        )
    )

    has_benchmarks = bool(
        evidence.get("industry_benchmarks")
    )

    has_previous_current_ratio = (
        evidence.get("current_ratio_previous") is not None
    )
    liabilities_available = (
        evidence.get("current_liabilities_current") is not None
        or "Current liabilities" in evidence.get(
            "available_data", []
        )
    )
    for line in report.splitlines():

        text = line.strip()

        if not text:
            continue

        lower = text.lower()
        # CHECK: Claims that current liabilities are unavailable
        liabilities_missing_claim = re.search(
            r"\bcurrent liabilities\b.{0,80}"
            r"\b(unavailable|missing|not available|not provided)\b"
            r"|\b(without|lack|lacks|lacking|no)\b"
            r".{0,50}\bcurrent liabilities\b",
            lower
        )

        if liabilities_available and liabilities_missing_claim:
            issues.append({
                "code": "LIABILITIES_CONTRADICTION",
                "message": (
                    "Report may incorrectly claim that current "
                    "liabilities are unavailable."
                ),
                "excerpt": text
            })
        # CHECK 1: Capital expenditures incorrectly called missing
        capex_mentioned = re.search(
            r"\b(capital expenditures|capex|capital spending)\b",
            lower
        )

        missing_claim = re.search(
            r"\b(unavailable|missing|not provided|not available)\b",
            lower
        )

        capex_explicitly_available = re.search(
            r"\b(capital expenditures|capex)\s+"
            r"(?:are|is|were)\s+(?:available|provided)\b",
            lower
        )

        if (
            capex_available
            and capex_mentioned
            and missing_claim
            and not capex_explicitly_available
        ):
            issues.append({
                "code": "CAPEX_CONTRADICTION",
                "message": (
                    "Report may incorrectly describe available "
                    "capital expenditure data as missing."
                ),
                "excerpt": text
            })

        # CHECK 2: Unsupported industry benchmark comparisons
        benchmark_comparison = re.search(
            r"\b(outperform\w*|exceed\w*|beat\w*|"
            r"above|below|superior to)\b"
            r".{0,100}"
            r"\b(benchmarks?|industry averages?|peer averages?)\b",
            lower
        )

        if benchmark_comparison and not has_benchmarks:
            issues.append({
                "code": "UNSUPPORTED_BENCHMARK",
                "message": (
                    "Report makes a comparative benchmark claim "
                    "without supplied benchmark evidence."
                ),
                "excerpt": text
            })

        # CHECK 3: Hypotheses presented as established causes
        causal_claim = re.search(
            r"\b(indicates?|indicating|reflects?|reflecting|"
            r"demonstrates?|demonstrating|proves?|confirms?)\b"
            r".{0,120}"
            r"\b(operational efficiency|cost efficiency|"
            r"cost optimization|pricing power|productivity gains)\b",
            lower
        )

        uncertainty = re.search(
            r"\b(may|might|could|possible|possibly|"
            r"potential|hypothesis|unverified)\b",
            lower
        )

        if causal_claim and not uncertainty:
            issues.append({
                "code": "UNSUPPORTED_CAUSAL_CLAIM",
                "message": (
                    "Report may present a possible business "
                    "driver as an established fact."
                ),
                "excerpt": text
            })

        # CHECK 4: Liquidity improvement claimed without history
        current_ratio_trend = re.search(
            r"\bcurrent ratio\b"
            r".{0,80}"
            r"\b(improved|increased|decreased|declined|rose|fell)\b",
            lower
        )

        if current_ratio_trend and not has_previous_current_ratio:
            issues.append({
                "code": "UNSUPPORTED_LIQUIDITY_TREND",
                "message": (
                    "Report describes a change in current ratio, "
                    "but the evidence does not include the prior ratio."
                ),
                "excerpt": text
            })

    return issues