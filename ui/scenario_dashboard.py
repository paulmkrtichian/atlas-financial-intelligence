
import pandas as pd
import streamlit as st

from finance.scenarios import project_scenario


def render_scenario_dashboard():

    st.title("Scenario Intelligence")

    st.caption(
        "Model alternative financial outcomes using "
        "transparent, adjustable assumptions."
    )

    data = st.session_state.get("atlas_research_data")

    if data is None:
        st.info(
            "No company data loaded. Open Private Companies, "
            "import financial statements, and analyze them first."
        )
        return

    source = st.session_state.get(
        "atlas_research_source",
        "Imported Company"
    )

    st.success(f"Financial data loaded: {source}")

    available_years = sorted(
        data["fiscal_year"].astype(int).unique().tolist(),
        reverse=True
    )

    base_year = st.selectbox(
        "Historical Base Year",
        options=available_years
    )

    selected = data.loc[
        data["fiscal_year"].astype(int) == base_year
    ]

    base_revenue = float(selected.iloc[0]["revenue"])

    st.metric(
        "Base-Year Revenue",
        f"USD {base_revenue / 1e6:,.2f}M"
    )


    # RESEARCH INTELLIGENCE HANDOFF
    handoff = st.session_state.get("atlas_model_handoff")

    if handoff is not None:

        if handoff["source"] == source:

            st.divider()
            st.subheader("Research-Driven Modeling")

            st.info(
                f"Research focus: {handoff['focus']}"
            )

            if handoff["fiscal_year"] != base_year:

                st.warning(
                    "The selected modeling year differs from "
                    "the research report year. Select "
                    f"{handoff['fiscal_year']} to use "
                    "the matching historical reference."
                )

            else:

                col1, col2 = st.columns(2)

                col1.metric(
                    "Historical Revenue Growth",
                    f"{handoff['historical_growth_pct']:.2f}%"
                )

                col2.metric(
                    "Historical Operating Margin",
                    f"{handoff['historical_margin_pct']:.2f}%"
                )

                with st.expander(
                    "Review Supporting AI Research"
                ):

                    display_text = handoff[
                        "ai_interpretation"
                    ].replace("$", r"\$")

                    st.markdown(display_text)

                st.caption(
                    "The figures above are historical reference "
                    "points, not projected outcomes. Adjust the "
                    "Downside, Base, and Upside assumptions below "
                    "to investigate different scenarios."
                )


    st.caption(
        "Figures are modeled in actual USD and displayed "
        "in USD millions. Assumptions are illustrative."
    )

    st.divider()
    st.subheader("Scenario Assumptions")

    defaults = [
        ("Downside", 3.0, 18.0),
        ("Base", 8.0, 23.0),
        ("Upside", 13.0, 27.0)
    ]

    columns = st.columns(3)
    projections = []

    for column, (name, growth_default, margin_default) in zip(
        columns, defaults
    ):

        with column:
            with st.container(border=True):

                st.subheader(name)

                growth = st.number_input(
                    "Annual Revenue Growth (%)",
                    min_value=-99.0,
                    max_value=100.0,
                    value=growth_default,
                    step=0.5,
                    key=f"{name}_growth"
                )

                margin = st.number_input(
                    "Operating Margin (%)",
                    min_value=-100.0,
                    max_value=100.0,
                    value=margin_default,
                    step=0.5,
                    key=f"{name}_margin"
                )

                forecast = project_scenario(
                    financial_data=data,
                    base_year=base_year,
                    revenue_growth_pct=growth,
                    operating_margin_pct=margin,
                    years=3,
                    scenario_name=name
                )

                projections.append(forecast)

    results = pd.concat(
        projections,
        ignore_index=True
    )

    st.divider()
    st.subheader("Projected Revenue")

    revenue_chart = results.pivot(
        index="fiscal_year",
        columns="scenario",
        values="revenue"
    ) / 1e6

    st.line_chart(revenue_chart)

    st.subheader("Projected Operating Income")

    income_chart = results.pivot(
        index="fiscal_year",
        columns="scenario",
        values="operating_income"
    ) / 1e6

    st.line_chart(income_chart)

    st.divider()
    st.subheader("Final-Year Comparison")

    final_year = base_year + 3

    final_results = results.loc[
        results["fiscal_year"] == final_year
    ]

    columns = st.columns(3)

    for column, name in zip(
        columns,
        ["Downside", "Base", "Upside"]
    ):

        row = final_results.loc[
            final_results["scenario"] == name
        ].iloc[0]

        with column:
            with st.container(border=True):

                st.markdown(f"**{name}**")

                st.metric(
                    "Revenue",
                    f"USD {row['revenue'] / 1e6:,.2f}M"
                )

                st.metric(
                    "Operating Income",
                    f"USD {row['operating_income'] / 1e6:,.2f}M"
                )

    with st.expander("View Detailed Scenario Data"):

        display = results.copy()

        display["Revenue (USD M)"] = (
            display["revenue"] / 1e6
        ).round(2)

        display["Operating Income (USD M)"] = (
            display["operating_income"] / 1e6
        ).round(2)

        display = display.rename(columns={
            "scenario": "Scenario",
            "fiscal_year": "Fiscal Year",
            "operating_margin_pct": "Operating Margin (%)"
        })

        st.dataframe(
            display[[
                "Scenario",
                "Fiscal Year",
                "Revenue (USD M)",
                "Operating Margin (%)",
                "Operating Income (USD M)"
            ]],
            hide_index=True,
            use_container_width=True
        )

    st.download_button(
        "Download Scenario Data (CSV)",
        data=results.to_csv(index=False),
        file_name=f"atlas_scenarios_{base_year}.csv",
        mime="text/csv"
    )

    st.caption(
        "Scenario outputs are hypothetical, not forecasts "
        "validated by management or market research. "
        "Growth and operating margins remain constant "
        "within each scenario. Revenue is assumed to "
        "compound annually."
    )
