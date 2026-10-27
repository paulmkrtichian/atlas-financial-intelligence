def build_financial_findings(evidence):
    """
    Build factual financial findings using
    Python-calculated evidence, not AI.
    """

    required = [
        "revenue_current",
        "revenue_previous",
        "revenue_growth_pct",
        "operating_margin_current_pct",
        "operating_margin_change_pp",
        "net_profit_margin_pct",
        "net_profit_margin_change_pp",
        "free_cash_flow_current",
        "free_cash_flow_change",
        "current_ratio"
    ]

    missing = [
        key for key in required
        if evidence.get(key) is None
    ]

    if missing:
        raise ValueError(
            f"Missing financial evidence: {missing}"
        )

    findings = [
        {
            "metric": "Revenue Growth",
            "finding": (
                f"Revenue increased from "
                f"USD {evidence['revenue_previous'] / 1e6:,.2f}M "
                f"to USD {evidence['revenue_current'] / 1e6:,.2f}M. "
                f"Year-over-year growth was "
                f"{evidence['revenue_growth_pct']:.2f}%."
            )
        },
        {
            "metric": "Operating Profitability",
            "finding": (
                f"Operating margin reached "
                f"{evidence['operating_margin_current_pct']:.2f}%, "
                f"changing by "
                f"{evidence['operating_margin_change_pp']:+.2f} "
                f"percentage points."
            )
        },
        {
            "metric": "Net Profitability",
            "finding": (
                f"Net profit margin reached "
                f"{evidence['net_profit_margin_pct']:.2f}%, "
                f"changing by "
                f"{evidence['net_profit_margin_change_pp']:+.2f} "
                f"percentage points."
            )
        },
        {
            "metric": "Free Cash Flow",
            "finding": (
                f"Free cash flow was "
                f"USD {evidence['free_cash_flow_current'] / 1e6:,.2f}M, "
                f"a change of "
                f"USD {evidence['free_cash_flow_change'] / 1e6:+,.2f}M."
            )
        },
        {
            "metric": "Liquidity",
            "finding": (
                f"The current ratio was "
                f"{evidence['current_ratio']:.2f}. "
                f"No liquidity-quality conclusion is made "
                f"without additional context."
            )
        }
    ]

    return findings