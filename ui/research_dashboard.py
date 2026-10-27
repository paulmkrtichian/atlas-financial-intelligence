from pathlib import Path

import streamlit as st
from agents.financial_findings import build_financial_findings
from agents.research_intelligence import (
    extract_financial_evidence,
    generate_financial_research
)


def render_research_dashboard():

    st.title("Research Intelligence")

    st.caption(
        "AI-assisted financial research grounded in "
        "verified financial calculations."
    )

    # Retrieve data from the Financial Statement Import page
    data = st.session_state.get("atlas_research_data")

    if data is None:
        st.info(
            "No financial statements are loaded. "
            "Open Private Companies, upload your financial "
            "statements, and analyze them first."
        )
        return

    source = st.session_state.get(
        "atlas_research_source",
        "Imported Company"
    )

    st.success(f"Financial data loaded: {source}")

    # Determine which years have a preceding year
    years = sorted(
        set(int(year) for year in data["fiscal_year"]),
        reverse=True
    )

    available_years = [
        year for year in years
        if year - 1 in years
    ]

    if not available_years:
        st.warning(
            "At least two consecutive fiscal years "
            "are required for research analysis."
        )
        return

    default_company_name = (
        Path(source).stem.replace("_", " ").title()
    )

    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input(
            "Company Name",
            value=default_company_name
        )

    with col2:
        fiscal_year = st.selectbox(
            "Fiscal Year",
            options=available_years
        )

    st.divider()

    # VERIFIED FINANCIAL EVIDENCE
    st.subheader("Verified Financial Evidence")

    try:
        evidence = extract_financial_evidence(
            data,
            fiscal_year
        )

    except (ValueError, KeyError, TypeError) as error:
        st.error(f"Financial evidence error: {error}")
        return

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Revenue Growth",
        f"{evidence['revenue_growth_pct']:.2f}%"
    )

    col2.metric(
        "Operating Margin",
        f"{evidence['operating_margin_current_pct']:.2f}%",
        delta=(
            f"{evidence['operating_margin_change_pp']:+.2f} pp"
        )
    )

    col3.metric(
        "Current Ratio",
        f"{evidence['current_ratio']:.2f}"
    )

    col4, col5 = st.columns(2)

    col4.metric(
        "Free Cash Flow",
        f"${evidence['free_cash_flow_current'] / 1e6:,.2f}M"
    )

    col5.metric(
        "Change in Free Cash Flow",
        f"${evidence['free_cash_flow_change'] / 1e6:+,.2f}M"
    )

    with st.expander("View Detailed Financial Evidence"):
        st.json(evidence)

    st.divider()

    # AI FINANCIAL RESEARCH
    st.subheader("AI Financial Research")

    st.write(
        "Generate a structured report identifying important "
        "financial developments, possible business drivers, "
        "modeling opportunities, and further research needs."
    )

    if st.button(
        "Generate AI Research Report",
        type="primary"
    ):

        if not company_name.strip():
            st.error("Please enter a company name.")

        else:
            with st.spinner(
                "Atlas is analyzing the financial evidence..."
            ):

                try:
                    live_report = st.empty()

                    def show_progress(text):
                        live_report.markdown(
                            text.replace("$", r"\$") + " ▌"
                        )

                    result = generate_financial_research(
                        data,
                        company_name,
                        fiscal_year,
                        on_chunk=show_progress
                    )

                    live_report.empty()
                    result = generate_financial_research(
                        data,
                        company_name,
                        fiscal_year
                    )

                    st.session_state["atlas_latest_research"] = {
                        "result": result,
                        "source": source,
                        "company": company_name,
                        "year": fiscal_year
                    }

                except Exception as error:
                    st.error(
                        f"Research generation failed: {error}"
                    )

    saved = st.session_state.get("atlas_latest_research")

    if saved is not None:

        # Only display a report for the current selection
        if (
            saved["source"] == source
            and saved["company"] == company_name
            and saved["year"] == fiscal_year
        ):

            result = saved["result"]

            st.divider()
            st.subheader("Atlas Research Report")

            st.caption(
                "AI-assisted interpretation. Financial "
                "hypotheses require independent verification."
            )

                        # Python-calculated financial findings
            st.subheader("Calculated Financial Findings")

            findings = build_financial_findings(
                result["evidence"]
            )

            for item in findings:
                st.markdown(
                    f"**{item['metric']}** — {item['finding']}"
                )

            st.divider()

            st.subheader("AI Financial Interpretation")
            # Escape currency symbols so Streamlit
            # does not interpret them as LaTeX math.
            display_report = result["report"].replace(
                "$", r"\$"
            )

            st.markdown(display_report)

            # Financial evidence validation results
            st.divider()

            st.subheader("Evidence Review")

            issues = result.get("validation_issues", [])

            if issues:

                st.warning(
                    f"{len(issues)} potential research issue(s) "
                    "identified. Review before relying on this report."
                )

                for number, issue in enumerate(issues, start=1):

                    with st.expander(
                        f"{number}. {issue['code']}"
                    ):

                        st.write(issue["message"])

                        st.caption("Flagged statement:")

                        st.markdown(
                            f"> {issue['excerpt']}"
                        )

            else:

                st.info(
                    "No issues were detected by the current "
                    "automated checks. This does not mean "
                    "the entire report has been verified."
                )

            report_text = (
                f"# {company_name} — FY {fiscal_year}\n\n"
                f"{result['report']}"
            )

            st.download_button(
                "Download Research Report",
                data=report_text,
                file_name="atlas_research_report.md",
                mime="text/markdown"
            )

            # RESEARCH-TO-SCENARIO INTEGRATION
            st.divider()

            st.subheader("Explore This Research in a Financial Model")

            st.write(
                "Select a modeling question based on the "
                "financial research above."
            )

            st.selectbox(
                "What would you like to investigate?",
                options=[
                    "Revenue growth sensitivity",
                    "Operating margin sustainability",
                    "Combined revenue and margin sensitivity"
                ],
                key="atlas_model_focus"
            )

            def send_to_scenarios():

                st.session_state["atlas_model_handoff"] = {
                    "source": source,
                    "company": company_name,
                    "fiscal_year": int(fiscal_year),
                    "focus": st.session_state["atlas_model_focus"],
                    "historical_growth_pct": float(
                        result["evidence"]["revenue_growth_pct"]
                    ),
                    "historical_margin_pct": float(
                        result["evidence"][
                            "operating_margin_current_pct"
                        ]
                    ),
                    "ai_interpretation": result["report"]
                }

                st.session_state["atlas_page"] = "Scenario Modeling"

            st.button(
                "Explore in Scenario Modeling",
                type="primary",
                on_click=send_to_scenarios
            )


    st.caption(
        "Financial evidence comes from imported statements. "
        "AI-generated explanations are hypotheses unless "
        "supported by additional sources. "
        "Review findings before making business decisions."
    )