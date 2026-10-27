import json

from ai.engine import ask_atlas, stream_atlas
from agents.evidence_validator import validate_research_report
from finance.private_analysis import analyze_private_company
from finance.calculations import operating_margin


def extract_financial_evidence(data, fiscal_year):
    """
    Calculate financial changes using actual company data.

    Returns structured evidence without asking AI
    to perform arithmetic.
    """

    fiscal_year = int(fiscal_year)

    # Reuse Atlas's verified financial calculations
    analysis = analyze_private_company(
        data,
        fiscal_year
    )

    current = data.loc[
        data["fiscal_year"] == fiscal_year
    ].iloc[0]

    previous = data.loc[
        data["fiscal_year"] == fiscal_year - 1
    ].iloc[0]

    # Compare operating margins between years
    previous_margin = operating_margin(
        previous["operating_income"],
        previous["revenue"]
    )

    current_margin = analysis["operating_margin"]

    margin_change = current_margin - previous_margin

    # Calculate last year's free cash flow
    previous_fcf = (
        previous["operating_cash_flow"]
        - previous["capital_expenditures"]
    )

    current_fcf = analysis["free_cash_flow"]

    previous_net_margin = (
        previous["net_income"] / previous["revenue"]
    ) * 100

    current_net_margin = analysis["net_profit_margin"]

    evidence = {
        "fiscal_year": fiscal_year,
        "comparison_year": fiscal_year - 1,

        "revenue_current": float(current["revenue"]),
        "revenue_previous": float(previous["revenue"]),

        "revenue_growth_pct": round(
            analysis["revenue_growth"], 2
        ),

        "operating_margin_current_pct": round(
            current_margin, 2
        ),

        "operating_margin_previous_pct": round(
            previous_margin, 2
        ),

        "operating_margin_change_pp": round(
            margin_change, 2
        ),

        "net_profit_margin_pct": round(
            analysis["net_profit_margin"], 2
        ),

        "free_cash_flow_current": float(current_fcf),
        "free_cash_flow_previous": float(previous_fcf),

        "free_cash_flow_change": float(
            current_fcf - previous_fcf
        ),

        "current_ratio": round(
            analysis["current_ratio"], 2
        ),

        "return_on_assets_pct": round(
            analysis["return_on_assets"], 2
        ),

        "return_on_equity_pct": round(
            analysis["return_on_equity"], 2
        ),
                "net_profit_margin_previous_pct": round(
            previous_net_margin, 2
        ),

        "net_profit_margin_change_pp": round(
            current_net_margin - previous_net_margin, 2
        ),
                "total_assets_current": float(
            current["total_assets"]
        ),

        "total_assets_previous": float(
            previous["total_assets"]
        ),

        "shareholders_equity_current": float(
            current["shareholders_equity"]
        ),

        "shareholders_equity_previous": float(
            previous["shareholders_equity"]
        ),

        "operating_cash_flow_current": float(
            current["operating_cash_flow"]
        ),

        "capital_expenditures_current": float(
            current["capital_expenditures"]
        ),

        "available_data": [
            "Revenue",
            "Operating income",
            "Net income",
            "Total assets",
            "Shareholders equity",
            "Current assets",
            "Current liabilities",
            "Operating cash flow",
            "Capital expenditures"
        ],

        "unavailable_data": [
            "Gross profit",
            "Cost of goods sold",
            "Detailed operating expenses",
            "Debt balances",
            "Industry benchmarks",
            "Competitor data",
            "Pricing and customer-level data"
        ]
    }

    return evidence


def generate_financial_research(
    data,
    company_name,
    fiscal_year,
    on_chunk=None
):
    """
    Generate an AI-assisted financial research report
    grounded in calculated financial evidence.
    """

    if not company_name.strip():
        raise ValueError("Company name is required.")

    # Step 1: Calculate financial evidence
    evidence = extract_financial_evidence(
        data,
        fiscal_year
    )

    # Step 2: Convert evidence into readable JSON
    financial_context = json.dumps(
        evidence,
        indent=2
    )

    # Step 3: Give Atlas explicit research instructions
    prompt = f"""
You are Atlas Financial Research Intelligence.

Your task is to analyze company financial performance
and identify important findings for a financial analyst.

COMPANY:
{company_name}

VERIFIED FINANCIAL EVIDENCE:
{financial_context}

IMPORTANT RULES:

1. Use only the supplied numerical financial data.
2. Never invent financial figures.
3. Do not perform new arithmetic. Use the supplied
   calculated values.
4. Separate verified observations from hypotheses.
5. Do not present possible explanations as facts.
6. Identify information that is missing.
7. Recommend financial analyses or business
   questions worth investigating.
8. Do not make unsupported investment recommendations.
9. Use USD for monetary amounts.
10. Explain financial conclusions clearly.
11. Never invent industry benchmarks or competitor data.
12. Do not claim a financial ratio is healthy, strong,
    or weak without a relevant comparison.
13. Only describe a business model when supported
    by the supplied company information.
14. Do not claim a metric was unchanged unless
    both reporting periods were provided.
15. If evidence is insufficient, explicitly state
    that the conclusion cannot be established.
16. Never use hypothetical benchmarks as evidence
    for actual company performance.

10. Explain financial conclusions clearly.

DATA AVAILABILITY RULES:

- The available_data and unavailable_data lists are authoritative.
- Never describe a field in available_data as missing.
- Never invent an industry benchmark.
- Do not describe a financial ratio as healthy or superior
  without relevant comparative evidence.
- Use underlying balance-sheet values when discussing ROA or ROE.
- Distinguish missing detailed working-capital components
  from the current assets and liabilities that are provided.
- Propose scenarios only as hypothetical exercises, not forecasts.
- Avoid claims about specific business models without evidence.


Produce a report using the following structure:

## Executive Summary
Identify the most important financial developments.

## Key Financial Findings
Discuss revenue growth, margins, profitability,
liquidity, and cash-flow changes.

Use actual figures from the supplied evidence.

## Potential Business Drivers
Discuss possible explanations worth investigating.

Clearly label every explanation as a hypothesis
unless directly supported by evidence.

## Financial Modeling Opportunities
Suggest 2-3 scenarios that could help evaluate
future business performance.

Do not invent assumptions as if they were forecasts.

## Recommended Research Actions
Identify specific additional financial information,
management questions, or market research that would
help explain the results.

## Limitations
Describe what cannot be concluded from the
available financial information.

Generate a concise financial research brief.

Use these sections:

Generate a concise financial research brief.

## Potential Business Drivers
Identify at most 3 hypotheses, one sentence each.

## Financial Modeling Opportunities
Suggest 2 scenarios with explicit assumptions.

## Recommended Research Actions
Provide 3 specific research questions or next steps.

## Limitations
Identify the 2 most important evidence gaps.

Do not repeat the Python-calculated financial findings.
Do not include an introduction or conclusion.
Keep the entire response under 150 words.
"""


    # Step 4: Generate an interpretation with Qwen
    if on_chunk is None:
        # Regular generation (used by existing tests)
        response = ask_atlas(prompt)

        if isinstance(response, str):
            report = response
        else:
            report = "".join(response)

    else:
        # Stream the interpretation progressively
        chunks = []

        for chunk in stream_atlas(prompt):
            chunks.append(chunk)
            on_chunk("".join(chunks))

        report = "".join(chunks)

    # Step 5: Validate the completed report
    validation_issues = validate_research_report(
        report,
        evidence
    )

    return {
        "company": company_name,
        "fiscal_year": int(fiscal_year),
        "evidence": evidence,
        "report": report,
        "validation_issues": validation_issues,
        "validation_warning_count": len(validation_issues)
    }
    # Our existing engine may return either complete
    # text or a generator of text chunks.
    if isinstance(response, str):
        report = response
    else:
        report = "".join(response)

    # Automatically review the generated research report
    validation_issues = validate_research_report(
        report,
        evidence
    )

    return {
        "company": company_name,
        "fiscal_year": int(fiscal_year),
        "evidence": evidence,
        "report": report,
        "validation_issues": validation_issues,
        "validation_warning_count": len(validation_issues)
    }