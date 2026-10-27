import json

from ai.engine import ask_atlas
from finance.comparison import compare_companies


def generate_research_report(ticker_a, ticker_b, fiscal_year):
    """
    Generate an AI financial research report using
    SEC-derived calculations.
    """

    # Step 1: Retrieve and calculate financial metrics
    comparison = compare_companies(
        ticker_a,
        ticker_b,
        fiscal_year
    )

    # Step 2: Convert financial results into JSON text
    financial_data = json.dumps(
        comparison,
        indent=2
    )

    # Step 3: Give the AI the financial results
    prompt = f"""
You are Atlas, a financial research assistant.

Analyze the following SEC-derived financial data:

{financial_data}

Instructions:
1. Use only the numerical figures provided.
2. Never invent financial data.
3. Compare revenue growth and profitability.
4. Compare free cash flow and liquidity.
5. Explain how ROE can be affected by equity levels.
6. Distinguish observations from possible explanations.
7. Acknowledge different fiscal year-end dates.
8. Do not make investment recommendations.
9. Keep the report under 400 words.

Structure your report with these sections:

## Executive Summary
## Revenue Growth
## Profitability
## Cash Flow and Liquidity
## Limitations and Further Research
"""

    # Step 4: Ask Qwen to interpret the results
    report = ask_atlas(prompt)

    return {
        "comparison": comparison,
        "report": report
    }