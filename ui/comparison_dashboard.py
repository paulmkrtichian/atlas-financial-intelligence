import streamlit as st
import pandas as pd
import requests
import altair as alt

from finance.comparison import compare_companies


@st.cache_data(ttl=3600)
def load_comparison(ticker_a, ticker_b, fiscal_year):
    return compare_companies(
        ticker_a,
        ticker_b,
        fiscal_year
    )


def render_comparison_dashboard():

    st.divider()

    st.header("⚖️ Company Comparison")

    st.write(
        "Compare two publicly traded companies using "
        "SEC-reported financial information."
    )

    with st.form("company_comparison_form"):

        col1, col2 = st.columns(2)

        with col1:
            ticker_a = st.text_input(
                "First Company",
                value="MSFT"
            )

        with col2:
            ticker_b = st.text_input(
                "Second Company",
                value="AAPL"
            )

        fiscal_year = st.number_input(
            "Fiscal Year",
            min_value=2010,
            max_value=2026,
            value=2024,
            step=1
        )

        submitted = st.form_submit_button(
            "Compare Companies"
        )

    if submitted:

        with st.spinner("Analyzing both companies..."):

            try:

                result = load_comparison(
                    ticker_a.strip().upper(),
                    ticker_b.strip().upper(),
                    int(fiscal_year)
                )

                companies = result["companies"]

                company_a = companies[0]
                company_b = companies[1]

                st.success("Comparison completed!")

                st.subheader(
                    f"{company_a['ticker']} vs. "
                    f"{company_b['ticker']}"
                )

                # Show reporting dates
                st.write(
                    f"**{company_a['ticker']} period ending:** "
                    f"{company_a['period_end']}"
                )

                st.write(
                    f"**{company_b['ticker']} period ending:** "
                    f"{company_b['period_end']}"
                )

                if (
                    company_a["period_end"]
                    != company_b["period_end"]
                ):
                    st.warning(
                        "These companies have different fiscal "
                        "year-end dates. Their reporting periods "
                        "are not identical."
                    )

                # Comparison table
                metric_labels = {
                    "revenue_growth": "Revenue Growth (%)",
                    "operating_margin": "Operating Margin (%)",
                    "net_profit_margin": "Net Profit Margin (%)",
                    "return_on_assets": "Return on Assets (%)",
                    "return_on_equity": "Return on Equity (%)",
                    "current_ratio": "Current Ratio",
                    "free_cash_flow": "Free Cash Flow (USD billions)"
                }

                rows = []

                for metric, label in metric_labels.items():

                    value_a = company_a[metric]
                    value_b = company_b[metric]

                    if metric == "free_cash_flow":
                        value_a = value_a / 1e9
                        value_b = value_b / 1e9

                    rows.append({
                        "Metric": label,
                        company_a["ticker"]: round(value_a, 2),
                        company_b["ticker"]: round(value_b, 2)
                    })

                df = pd.DataFrame(rows)

                st.subheader("Financial Comparison")

                st.dataframe(
                    df,
                    hide_index=True,
                    use_container_width=True
                )

                # Profitability chart
                st.subheader("Profitability Comparison")

                profitability_metrics = [
                    "operating_margin",
                    "net_profit_margin",
                    "return_on_assets",
                    "return_on_equity"
                ]

                chart_rows = []

                for company in companies:

                    for metric in profitability_metrics:

                        chart_rows.append({
                            "Company": company["ticker"],
                            "Metric": metric.replace(
                                "_", " "
                            ).title(),
                            "Percentage": company[metric]
                        })

                chart_df = pd.DataFrame(chart_rows)

                chart_pivot = chart_df.pivot(
                    index="Metric",
                    columns="Company",
                    values="Percentage"
                )

                chart = alt.Chart(chart_df).mark_bar().encode(
                    x=alt.X("Metric:N", title="Financial Metric"),
                    xOffset="Company:N",
                    y=alt.Y("Percentage:Q", title="Percentage (%)"),
                    color="Company:N",
                    tooltip=["Company", "Metric", "Percentage"]
                )


                st.altair_chart(chart, use_container_width=True)

                # Cash flow comparison
                st.subheader("Free Cash Flow Comparison")

                cash_flow_df = pd.DataFrame({
                    "Company": [
                        company_a["ticker"],
                        company_b["ticker"]
                    ],
                    "Free Cash Flow (USD billions)": [
                        company_a["free_cash_flow"] / 1e9,
                        company_b["free_cash_flow"] / 1e9
                    ]
                })

                st.bar_chart(
                    cash_flow_df,
                    x="Company",
                    y="Free Cash Flow (USD billions)"
                )

                st.caption(
                    "Absolute free cash flow is affected by "
                    "company size and should not be treated as "
                    "a standalone measure of efficiency."
                )

                # SEC sources
                st.subheader("SEC Sources")

                col1, col2 = st.columns(2)

                with col1:
                    st.link_button(
                        f"{company_a['ticker']} SEC Data",
                        "https://data.sec.gov/api/xbrl/"
                        f"companyfacts/CIK{company_a['cik']}.json"
                    )

                with col2:
                    st.link_button(
                        f"{company_b['ticker']} SEC Data",
                        "https://data.sec.gov/api/xbrl/"
                        f"companyfacts/CIK{company_b['cik']}.json"
                    )

                st.caption(
                    "Financial calculations are based on "
                    "SEC-reported data. Differences in fiscal "
                    "periods, accounting classifications, and "
                    "company size affect comparability."
                )

            except requests.exceptions.RequestException as error:

                st.error(
                    f"SEC connection failed: {error}"
                )

            except (ValueError, KeyError, TypeError) as error:

                st.error(
                    f"Comparison failed: {error}"
                )