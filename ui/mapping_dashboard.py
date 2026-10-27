import streamlit as st

from finance.importer import (
    read_raw_financial_file,
    REQUIRED_COLUMNS
)

from finance.column_mapping import (
    map_financial_columns,
    suggest_financial_mapping
)

from finance.private_analysis import analyze_private_company


def render_mapping_dashboard():

    st.divider()

    st.header("📂 Financial Statement Import")

    st.write(
        "Upload a company's financial statements in Excel "
        "or CSV format. Atlas will recognize familiar accounting "
        "columns, let you verify the mappings, and calculate "
        "financial performance."
    )

    uploaded_file = st.file_uploader(
        "Upload Financial Data",
        type=["csv", "xlsx"],
        key="mapping_file"
    )

    if uploaded_file is None:
        return

    try:
        raw_data = read_raw_financial_file(
            uploaded_file
        )
    except (ValueError, TypeError, Exception) as error:
        st.error(f"File could not be read: {error}")
        return

    st.subheader("Original Financial Data")
    st.dataframe(raw_data, hide_index=True)

        # Automatically suggest known accounting column names
    suggestions = suggest_financial_mapping(raw_data.columns)

    st.subheader("Suggested Financial Mappings")

    st.write(
        f"Recognized {len(suggestions)} of "
        f"{len(REQUIRED_COLUMNS)} financial columns."
    )

    # Show all suggested matches
    preview = [
        {
            "Atlas Metric": metric.replace("_", " ").title(),
            "Source Column": suggestions.get(metric, "Needs review")
        }
        for metric in REQUIRED_COLUMNS
    ]

    st.dataframe(
        preview,
        hide_index=True,
        use_container_width=True
    )

    # Only show dropdowns when requested or needed
    review = st.toggle(
        "Review or edit column matches",
        value=len(suggestions) < len(REQUIRED_COLUMNS)
    )

    options = ["-- Select column --"] + list(raw_data.columns)
    mapping = suggestions.copy()

    with st.form("financial_mapping_form"):

        if review:
            st.subheader("Edit Financial Mappings")

            for metric in REQUIRED_COLUMNS:

                suggested_column = suggestions.get(metric)

                default_index = (
                    options.index(suggested_column)
                    if suggested_column in options
                    else 0
                )

                selected = st.selectbox(
                    metric.replace("_", " ").title(),
                    options=options,
                    index=default_index,
                    key=f"mapping_{metric}"
                )

                if selected == "-- Select column --":
                    mapping.pop(metric, None)
                else:
                    mapping[metric] = selected

        # Always show the reporting units
        unit = st.selectbox(
            "Financial Statement Units",
            options=[
                "-- Select reporting units --",
                "USD",
                "USD thousands",
                "USD millions"
            ]
        )

        # Always show the confirmation checkbox
        confirmed = st.checkbox(
            "I verified the column matches and financial units."
        )

        # Always create the submit button
        submitted = st.form_submit_button(
            "Analyze Financial Statements"
        )

    if submitted:

        try:
            if not confirmed:
                raise ValueError(
                    "Please verify the mappings and units first."
                )

            if unit == "-- Select reporting units --":
                raise ValueError(
                    "Please select the spreadsheet's financial units."
                )

            standardized = map_financial_columns(
                raw_data,
                mapping,
                unit
            )
            st.session_state["atlas_research_data"] = standardized.copy()
            st.session_state.pop("atlas_model_handoff", None)
            st.session_state["atlas_research_source"] = uploaded_file.name
            st.session_state.pop("atlas_latest_research", None)
            st.success("Financial columns mapped successfully!")
           

                        # Professional financial statement display
            st.subheader("Financial Statements")

            st.caption("All figures in USD millions")

            # Place fiscal years across the top
            financial_table = (
                standardized
                .set_index("fiscal_year")
                .T
            )

            # Convert actual USD to USD millions
            financial_table = financial_table / 1_000_000

            # Improve accounting labels
            financial_table.index = [
                name.replace("_", " ").title()
                for name in financial_table.index
            ]

            # Improve fiscal-year headers
            financial_table.columns = [
                f"FY {year}"
                for year in financial_table.columns
            ]

            financial_table.index.name = "Financial Metric"

            # Display a formatted financial statement
            st.dataframe(
                financial_table.style.format("{:,.2f}"),
                use_container_width=True
            )

            # Preserve the original data for verification
            with st.expander("View Full Standardized Data"):
                st.dataframe(
                    standardized,
                    hide_index=True,
                    use_container_width=True
                )

            # Automatically analyze the latest imported year
            year = int(
                standardized["fiscal_year"].max()
            )

            result = analyze_private_company(
                standardized,
                year
            )

            st.subheader(f"Financial Analysis — FY {year}")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Revenue Growth",
                f"{result['revenue_growth']:.2f}%"
            )

            col2.metric(
                "Operating Margin",
                f"{result['operating_margin']:.2f}%"
            )

            col3.metric(
                "Net Profit Margin",
                f"{result['net_profit_margin']:.2f}%"
            )

            st.metric(
                "Free Cash Flow (USD millions)",
                f"{result['free_cash_flow']/1e6:.2f}"
            )

            st.caption(
                "The latest fiscal year was selected automatically. "
                "Verify column definitions, accounting periods, "
                "currency, and units before relying on these results."
            )

        except (ValueError, KeyError, TypeError) as error:
            st.error(f"Financial analysis failed: {error}")