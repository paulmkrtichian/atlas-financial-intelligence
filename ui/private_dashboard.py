import streamlit as st

from finance.importer import import_financial_statements
from finance.private_analysis import analyze_private_company


def render_private_dashboard():

    st.divider()

    st.header("Private Company Analysis")

    st.write(
        "Upload standardized financial statements "
        "to calculate company performance."
    )

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel Financial Statements",
        type=["csv", "xlsx"],
        key="private_company_upload"
    )

    if uploaded_file is None:
        st.info("Upload a financial statement to begin.")
        return

    try:
        data = import_financial_statements(uploaded_file)

    except Exception as error:
        st.error(f"File import failed: {error}")
        return

    st.success(
        f"Imported {len(data)} fiscal years successfully!"
    )

    st.subheader("Imported Financial Data")

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )

    available_years = sorted(
        data["fiscal_year"].tolist(),
        reverse=True
    )

    selected_year = st.selectbox(
        "Fiscal Year to Analyze",
        options=available_years
    )

    if st.button("Analyze Private Company"):

        try:
            result = analyze_private_company(
                data,
                selected_year
            )

        except ValueError as error:
            st.error(f"Analysis failed: {error}")
            return

        st.success("Financial analysis completed!")

        st.subheader(
            f"Financial Performance — FY {selected_year}"
        )

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

        col4, col5, col6 = st.columns(3)

        col4.metric(
            "Current Ratio",
            f"{result['current_ratio']:.2f}"
        )

        col5.metric(
            "Return on Assets",
            f"{result['return_on_assets']:.2f}%"
        )

        col6.metric(
            "Return on Equity",
            f"{result['return_on_equity']:.2f}%"
        )

        st.divider()

        st.subheader("Free Cash Flow")

        st.metric(
            "Free Cash Flow (USD millions)",
            f"{result['free_cash_flow'] / 1e6:,.2f}"
        )

        st.caption(
            "Imported figures are assumed to use USD "
            "in actual dollar amounts, consistent reporting "
            "periods, and nonnegative capital expenditures. "
            "Review the source statements before relying "
            "on the analysis."
        )