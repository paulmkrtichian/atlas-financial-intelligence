import streamlit as st
import pandas as pd
import requests

from finance.history import analyze_history


@st.cache_data(ttl=3600)
def load_history(ticker, end_year, years):
    return analyze_history(ticker, end_year, years)


def render_history_dashboard():

    st.divider()

    st.header("📈 Historical Financial Analysis")

    st.write(
        "Analyze multiple years of company financial "
        "performance using reported SEC data."
    )

    with st.form("history_form"):

        ticker = st.text_input(
            "Stock Ticker",
            value="MSFT"
        )

        end_year = st.number_input(
            "Ending Fiscal Year",
            min_value=2010,
            max_value=2026,
            value=2024,
            step=1
        )

        years = st.number_input(
            "Number of Years",
            min_value=2,
            max_value=10,
            value=5,
            step=1
        )

        submitted = st.form_submit_button(
            "Analyze Historical Performance"
        )

    if submitted:

        with st.spinner("Retrieving historical SEC data..."):

            try:

                result = load_history(
                    ticker.strip().upper(),
                    int(end_year),
                    int(years)
                )

                st.success("Historical analysis completed!")

                st.subheader(
                    f"{result['company']} — Financial History"
                )

                rows = []

                for item in result["history"]:

                    rows.append({
                        "Fiscal Year": str(item["year"]),
                        "Revenue (USD billions)": round(
                            item["revenue"] / 1e9, 2
                        ),
                        "Operating Margin (%)": round(
                            item["operating_margin"], 2
                        ),
                        "Revenue Growth (%)": (
                            round(item["revenue_growth"], 2)
                            if item["revenue_growth"] is not None
                            else None
                        ),
                        "Current Ratio": (
                            round(item["current_ratio"], 2)
                            if item["current_ratio"] is not None
                            else None
                        )
                    })

                df = pd.DataFrame(rows)

                # Revenue chart
                st.subheader("Revenue Over Time")

                st.line_chart(
                    df,
                    x="Fiscal Year",
                    y="Revenue (USD billions)"
                )

                # Operating margin chart
                st.subheader("Operating Margin Trend")

                st.line_chart(
                    df,
                    x="Fiscal Year",
                    y="Operating Margin (%)"
                )

                # Financial data table
                st.subheader("Historical Financial Data")

                st.dataframe(
                    df,
                    hide_index=True,
                    use_container_width=True
                )

                st.link_button(
                    "View SEC Source Data",
                    "https://data.sec.gov/api/xbrl/companyfacts/"
                    f"CIK{result['cik']}.json"
                )

                st.caption(
                    "Values are calculated from SEC-reported facts. "
                    "The first year's revenue growth is unavailable "
                    "because the preceding year is not included. "
                    "Reporting periods and accounting definitions "
                    "should be verified before investment use."
                )

            except requests.exceptions.RequestException as error:

                st.error(f"SEC connection failed: {error}")

            except (ValueError, KeyError, TypeError) as error:

                st.error(
                    f"Historical analysis could not be completed: {error}"
                )
                