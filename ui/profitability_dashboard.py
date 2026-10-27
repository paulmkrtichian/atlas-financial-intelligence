import streamlit as st
import requests

from finance.profitability import analyze_profitability


@st.cache_data(ttl=3600)
def load_profitability(ticker, fiscal_year):
    return analyze_profitability(ticker, fiscal_year)


def render_profitability_dashboard():

    st.divider()

    st.header("💰 Profitability & Cash Flow")

    st.write(
        "Analyze company profitability and cash generation "
        "using SEC financial statements."
    )

    with st.form("profitability_form"):

        ticker = st.text_input(
            "Company Ticker",
            value="MSFT",
            key="profitability_ticker"
        )

        fiscal_year = st.number_input(
            "Fiscal Year",
            min_value=2010,
            max_value=2026,
            value=2024,
            step=1,
            key="profitability_year"
        )

        submitted = st.form_submit_button(
            "Analyze Profitability"
        )

    if submitted:

        with st.spinner("Retrieving financial data..."):

            try:

                result = load_profitability(
                    ticker.strip().upper(),
                    int(fiscal_year)
                )

                st.success("Profitability analysis completed!")

                st.subheader(
                    f"{result['company']} — FY {result['fiscal_year']}"
                )

                st.caption(
                    f"Fiscal year ending: {result['period_end']}"
                )

                # Profitability metrics
                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Net Profit Margin",
                    f"{result['net_profit_margin']:.2f}%"
                )

                col2.metric(
                    "Return on Assets",
                    f"{result['return_on_assets']:.2f}%"
                )

                col3.metric(
                    "Return on Equity",
                    f"{result['return_on_equity']:.2f}%"
                )

                # Free cash flow
                st.divider()

                st.subheader("Free Cash Flow")

                operating_cf = result["operating_cash_flow"]
                capex = result["capital_expenditures"]
                fcf = result["free_cash_flow"]

                st.metric(
                    "Free Cash Flow (USD billions)",
                    f"{fcf / 1e9:,.2f}"
                )

                st.write(
                    "Free Cash Flow = Operating Cash Flow "
                    "− Capital Expenditures"
                )

                # Cash flow breakdown
                st.table({
                    "Metric": [
                        "Operating Cash Flow",
                        "Capital Expenditures",
                        "Free Cash Flow"
                    ],
                    "USD Billions": [
                        round(operating_cf / 1e9, 2),
                        round(capex / 1e9, 2),
                        round(fcf / 1e9, 2)
                    ]
                })

                # Source information
                st.subheader("SEC Reporting Details")

                source_rows = []

                for name, fact in result["sources"].items():

                    source_rows.append({
                        "Metric": name.replace("_", " ").title(),
                        "Reporting Date": fact["end"],
                        "SEC Tag": fact["tag"]
                    })

                st.dataframe(
                    source_rows,
                    hide_index=True,
                    use_container_width=True
                )

                st.link_button(
                    "View Official SEC Data",
                    "https://data.sec.gov/api/xbrl/companyfacts/"
                    f"CIK{result['cik']}.json"
                )

                st.caption(
                    "Calculations use SEC-reported financial facts. "
                    "ROA and ROE use average beginning and ending "
                    "balance sheet values. FCF equals operating cash "
                    "flow minus property, plant and equipment purchases "
                    "under the selected SEC tag. Definitions and "
                    "reporting periods may vary by company."
                )

            except requests.exceptions.RequestException as error:

                st.error(f"SEC connection failed: {error}")

            except (ValueError, KeyError, TypeError) as error:

                st.error(
                    f"Profitability analysis failed: {error}"
                )