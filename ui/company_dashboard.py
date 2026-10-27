import streamlit as st
import requests

from finance.analysis import analyze_company


def render_company_dashboard():

    st.divider()

    st.header("📈 Dynamic Financial Analysis")

    st.write(
        "Enter a stock ticker and fiscal year to analyze "
        "a company's SEC financial statements."
    )

    with st.form("dynamic_analysis_form"):

        ticker = st.text_input(
            "Company Ticker",
            value="MSFT",
            placeholder="AAPL, MSFT, NVDA..."
        )

        fiscal_year = st.number_input(
            "Fiscal Year",
            min_value=2010,
            max_value=2026,
            value=2024,
            step=1
        )

        submitted = st.form_submit_button(
            "Analyze Financials"
        )

    if submitted:

        with st.spinner("Analyzing financial statements..."):

            try:

                result = analyze_company(
                    ticker.strip().upper(),
                    int(fiscal_year)
                )

                st.success("Financial analysis completed!")

                st.subheader(
                    f"{result['company']} — FY {result['fiscal_year']}"
                )

                st.caption(
                    f"Reporting period ending: {result['period_end']}"
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
                    "Current Ratio",
                    f"{result['current_ratio']:.2f}"
                )

                st.divider()

                st.subheader("Financial Statements")

                financial_data = []

                for metric, info in result["financials"].items():

                    if info is not None:

                        financial_data.append({
                            "Metric": metric.replace("_", " ").title(),
                            "USD Billions": round(
                                info["value"] / 1e9, 2
                            ),
                            "Period End": info["end"],
                            "SEC Tag": info["tag"]
                        })

                st.dataframe(
                    financial_data,
                    use_container_width=True,
                    hide_index=True
                )

                st.link_button(
                    "View Official SEC Financial Data",
                    "https://data.sec.gov/api/xbrl/companyfacts/"
                    f"CIK{result['cik']}.json"
                )

                st.caption(
                    "Data sourced from SEC company filings. "
                    "Calculations performed using Python. "
                    "Not investment advice."
                )

            except (
                ValueError,
                KeyError,
                TypeError
            ) as error:

                st.error(
                    f"Unable to analyze company: {error}"
                )

            except requests.exceptions.RequestException as error:

                st.error(
                    f"SEC connection failed: {error}"
                )