import json

import pandas as pd
import streamlit as st

from agents.financial_tool_agent import analyze_financial_question


def render_ai_analyst_dashboard():

    st.title("Atlas AI Financial Analyst")

    st.caption(
        "Ask financial questions. Atlas selects analytical tools, "
        "executes Python calculations, and explains the results."
    )

    data = st.session_state.get("atlas_research_data")

    if data is None:
        st.info(
            "No financial data loaded. Import and analyze "
            "a company under Private Companies first."
        )
        return

    if not isinstance(data, pd.DataFrame):
        st.error("Financial data is not in the expected format.")
        return

    source = st.session_state.get(
        "atlas_research_source",
        "Imported Company"
    )

    st.success(f"Financial data loaded: {source}")

    available_years = sorted(
        pd.to_numeric(
            data["fiscal_year"],
            errors="coerce"
        ).dropna().astype(int).unique().tolist(),
        reverse=True
    )

    if not available_years:
        st.error("No valid fiscal years found.")
        return

    year = st.selectbox(
        "Select Fiscal Year",
        available_years,
        key="atlas_analyst_year"
    )

    st.divider()

    st.subheader("Ask Atlas")

    question = st.text_area(
        "Financial Research Question",
        placeholder=(
            "Example: How much did revenue grow?"
        ),
        height=110,
        key="atlas_analyst_question"
    )

    st.caption(
        "Supported analyses: revenue growth, operating margin, "
        "net margin, and financial summary."
    )

    if st.button(
        "Analyze Question",
        type="primary",
        disabled=not question.strip()
    ):

        with st.spinner(
            "Atlas is selecting tools and analyzing financial data..."
        ):

            try:

                result = analyze_financial_question(
                    question=question,
                    financial_data=data,
                    year=year,
                    provider="local"
                )

                st.session_state["atlas_analyst_result"] = result
                st.session_state["atlas_analyst_context"] = (
                    source,
                    year,
                    question
                )

            except Exception as error:

                st.session_state.pop(
                    "atlas_analyst_result",
                    None
                )

                st.error(f"Analysis failed: {error}")

    result = st.session_state.get("atlas_analyst_result")

    context = st.session_state.get("atlas_analyst_context")

    if result is not None and context == (
        source,
        year,
        question
    ):

        st.divider()

        st.subheader("Selected Financial Tool")

        st.code(result["selected_tool"])

        st.subheader("Verified Financial Calculation")

        st.json(result["calculation"])

        st.subheader("Atlas AI Interpretation")

        st.write(result["explanation"])

        st.caption(
            "Financial calculations are performed in Python. "
            "AI-generated explanations should be reviewed "
            "against the displayed calculation."
        )

        st.download_button(
            "Download Analysis (JSON)",
            data=json.dumps(result, indent=2),
            file_name=f"atlas_analysis_{year}.json",
            mime="application/json"
        )