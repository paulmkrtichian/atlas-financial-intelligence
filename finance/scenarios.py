
import math

import pandas as pd


def project_scenario(
    financial_data,
    base_year,
    revenue_growth_pct,
    operating_margin_pct,
    years=3,
    scenario_name="Base"
):
    """
    Project revenue and operating income using
    constant annual assumptions.

    Financial inputs and outputs are in actual USD.
    """

    if not isinstance(financial_data, pd.DataFrame):
        raise ValueError("Financial data must be a DataFrame.")

    required_columns = {"fiscal_year", "revenue"}

    if not required_columns.issubset(financial_data.columns):
        raise ValueError("Missing fiscal year or revenue column.")

    if not isinstance(years, int) or not 1 <= years <= 10:
        raise ValueError("Years must be between 1 and 10.")

    growth = float(revenue_growth_pct)
    margin = float(operating_margin_pct)

    if not math.isfinite(growth) or not math.isfinite(margin):
        raise ValueError("Assumptions must be finite numbers.")

    if growth <= -100:
        raise ValueError("Revenue growth must exceed -100%.")

    if not -100 <= margin <= 100:
        raise ValueError("Operating margin must be between -100% and 100%.")

    year_values = pd.to_numeric(
        financial_data["fiscal_year"],
        errors="coerce"
    )

    selected = financial_data.loc[
        year_values == int(base_year)
    ]

    if len(selected) != 1:
        raise ValueError(
            "Exactly one record is required for the base fiscal year."
        )

    base_revenue = float(selected.iloc[0]["revenue"])

    if not math.isfinite(base_revenue) or base_revenue <= 0:
        raise ValueError("Base revenue must be positive and finite.")

    projections = []

    for offset in range(1, years + 1):

        projected_year = int(base_year) + offset

        projected_revenue = (
            base_revenue * (1 + growth / 100) ** offset
        )

        projected_operating_income = (
            projected_revenue * margin / 100
        )

        projections.append({
            "scenario": scenario_name,
            "fiscal_year": projected_year,
            "revenue": projected_revenue,
            "operating_margin_pct": margin,
            "operating_income": projected_operating_income
        })

    return pd.DataFrame(projections)
