import json
import re

import pandas as pd

from ai.model_router import generate_ai_response


AVAILABLE_TOOLS = {
    "revenue_growth": "Calculate year-over-year revenue growth.",
    "operating_margin": "Calculate operating income as a percentage of revenue.",
    "net_margin": "Calculate net income as a percentage of revenue.",
    "financial_summary": "Summarize revenue, operating income, and net income.",
}


def select_financial_tool(question, provider="local"):
    """
    Ask AI to choose a financial analysis tool.
    """

    prompt = f"""
You are a financial analysis tool selector.

Available tools:
{json.dumps(AVAILABLE_TOOLS, indent=2)}

Choose the single most appropriate tool for the question.

Return ONLY valid JSON in this format:

{{
    "tool": "tool_name"
}}

Question:
{question}
"""

    response = generate_ai_response(
        prompt,
        provider=provider
    )

    match = re.search(r"\{.*?\}", response, re.DOTALL)

    if not match:
        raise ValueError("AI did not return a valid tool selection.")

    selection = json.loads(match.group())

    tool = selection.get("tool")

    if tool not in AVAILABLE_TOOLS:
        raise ValueError(f"Unsupported financial tool: {tool}")

    return tool


def execute_financial_tool(tool, financial_data, year):
    """
    Execute a verified financial calculation.
    """

    if not isinstance(financial_data, pd.DataFrame):
        raise ValueError("Financial data must be a DataFrame.")

    required_columns = {"fiscal_year", "revenue"}

    if tool == "operating_margin":
        required_columns.add("operating_income")

    elif tool == "net_margin":
        required_columns.add("net_income")

    elif tool == "financial_summary":
        required_columns.update(
            {"operating_income", "net_income"}
        )

    if not required_columns.issubset(financial_data.columns):
        missing = required_columns - set(financial_data.columns)
        raise ValueError(f"Missing financial columns: {missing}")

    selected = financial_data.loc[
        pd.to_numeric(
            financial_data["fiscal_year"],
            errors="coerce"
        ) == int(year)
    ]

    if len(selected) != 1:
        raise ValueError(
            "Exactly one financial record is required for the selected year."
        )

    row = selected.iloc[0]

    revenue = float(row["revenue"])

    if revenue <= 0:
        raise ValueError("Revenue must be positive.")

    if tool == "operating_margin":

        operating_income = float(row["operating_income"])

        return {
            "tool": tool,
            "fiscal_year": year,
            "operating_margin_pct": (
                operating_income / revenue
            ) * 100
        }

    if tool == "net_margin":

        net_income = float(row["net_income"])

        return {
            "tool": tool,
            "fiscal_year": year,
            "net_margin_pct": (
                net_income / revenue
            ) * 100
        }

    if tool == "financial_summary":

        return {
            "tool": tool,
            "fiscal_year": year,
            "revenue": revenue,
            "operating_income": float(row["operating_income"]),
            "net_income": float(row["net_income"])
        }

    if tool == "revenue_growth":

        previous = financial_data.loc[
            pd.to_numeric(
                financial_data["fiscal_year"],
                errors="coerce"
            ) == int(year) - 1
        ]

        if len(previous) != 1:
            raise ValueError(
                "Previous fiscal year data is required."
            )

        previous_revenue = float(
            previous.iloc[0]["revenue"]
        )

        if previous_revenue <= 0:
            raise ValueError(
                "Previous-year revenue must be positive."
            )

        return {
            "tool": tool,
            "fiscal_year": year,
            "revenue_growth_pct": (
                (revenue / previous_revenue) - 1
            ) * 100
        }

    raise ValueError(f"Unknown financial tool: {tool}")


def analyze_financial_question(
    question,
    financial_data,
    year,
    provider="local"
):
    """
    Select tool, execute calculation, and explain result.
    """

    selected_tool = select_financial_tool(
        question,
        provider=provider
    )

    result = execute_financial_tool(
        selected_tool,
        financial_data,
        year
    )

    explanation_prompt = f"""
You are Atlas Financial Intelligence.

A verified Python financial calculation has been completed.

User question:
{question}

Calculation result:
{json.dumps(result, indent=2)}

Explain the result clearly and concisely.

Rules:
- Use only the provided financial figures.
- Do not invent industry comparisons.
- Distinguish financial observations from interpretations.
- Do not change the calculated values.
"""

    explanation = generate_ai_response(
        explanation_prompt,
        provider=provider
    )

    return {
        "selected_tool": selected_tool,
        "calculation": result,
        "explanation": explanation
    }