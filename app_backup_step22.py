import streamlit as st

from ai.engine import ask_atlas
from finance.tickers import get_company_by_ticker
from ui.company_dashboard import render_company_dashboard
from finance.calculations import (
    revenue_growth,
    operating_margin,
    current_ratio
)
import requests

from finance.sec_client import get_company_facts
from finance.statements import extract_financial_statements
@st.cache_data(ttl=3600)
def load_company_facts(cik):
    return get_company_facts(cik)
# Configure the application
st.set_page_config(
    page_title="Atlas AI V3",
    page_icon="🧠",
    layout="wide"
)


# Application header
st.title("🧠 Atlas AI")

st.caption(
    "Personal Intelligence | Finance | Research | Automation"
)


# Create navigation tabs
assistant_tab, finance_tab, automation_tab = st.tabs([
    "🧠 Assistant",
    "📊 Finance",
    "⚙️ Automation"
])


# PERSONAL ASSISTANT
with assistant_tab:

    st.header("Personal AI Assistant")

    st.write(
        "Ask Atlas questions, explore ideas, "
        "and manage your personal projects."
    )

    question = st.text_input(
        "What would you like to ask Atlas?",
        placeholder="Ask me anything..."
    )

    if st.button("Ask Atlas"):

        if question.strip():

            with st.spinner("Atlas is thinking..."):

                try:
                    answer = ask_atlas(question)

                    st.markdown(answer)

                except Exception as error:
                    st.error(f"Error: {error}")

        else:
            st.warning("Please enter a question.")


# FINANCIAL INTELLIGENCE
with finance_tab:

    st.header("📊 Financial Intelligence")

    st.write(
        "Analyze company performance using "
        "verified Python calculations."
    )

    st.subheader("Financial Statement Inputs")

    with st.form("financial_form"):

        current_revenue = st.number_input(
            "Current Year Revenue (USD millions)",
            value=1200.0
        )

        previous_revenue = st.number_input(
            "Previous Year Revenue (USD millions)",
            value=1000.0
        )

        operating_income = st.number_input(
            "Operating Income (USD millions)",
            value=250.0
        )

        current_assets = st.number_input(
            "Current Assets (USD millions)",
            value=500.0
        )

        current_liabilities = st.number_input(
            "Current Liabilities (USD millions)",
            value=250.0
        )

        analyze = st.form_submit_button(
            "Analyze Company"
        )

    if analyze:

        try:

            growth = revenue_growth(
                current_revenue,
                previous_revenue
            )

            margin = operating_margin(
                operating_income,
                current_revenue
            )

            liquidity = current_ratio(
                current_assets,
                current_liabilities
            )

            st.divider()

            st.subheader("Financial Analysis Results")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Revenue Growth",
                f"{growth:.2f}%"
            )

            col2.metric(
                "Operating Margin",
                f"{margin:.2f}%"
            )

            col3.metric(
                "Current Ratio",
                f"{liquidity:.2f}"
            )

        except ValueError as error:

            st.error(str(error))

    # REAL COMPANY ANALYSIS
    st.divider()

    st.header("SEC Company Analysis")

    st.write(
        "Analyze Apple's reported financial data "
        "directly from SEC filings."
    )

    if st.button("Analyze Apple (SEC)"):

        with st.spinner("Retrieving SEC financial data..."):

            try:
                # Retrieve Apple financial information
                data = load_company_facts(320193)

                # Extract two fiscal years
                fy2024 = extract_financial_statements(
                    data, 2024
                )

                fy2023 = extract_financial_statements(
                    data, 2023
                )

                current = fy2024["metrics"]
                previous = fy2023["metrics"]

                # Verify required data is available
                required = [
                    current["revenue"],
                    current["operating_income"],
                    current["current_assets"],
                    current["current_liabilities"],
                    previous["revenue"]
                ]

                if any(item is None for item in required):
                    raise ValueError(
                        "Missing financial data. "
                        "Analysis cannot be completed."
                    )

                # Verify actual fiscal-year ending dates
                for item in required[:4]:
                    if item["end"] != "2024-09-28":
                        raise ValueError(
                            "Inconsistent 2024 reporting period."
                        )

                if previous["revenue"]["end"] != "2023-09-30":
                    raise ValueError(
                        "Inconsistent 2023 reporting period."
                    )

                # Extract reported values
                revenue_2024 = current["revenue"]["value"]
                revenue_2023 = previous["revenue"]["value"]

                op_income = current["operating_income"]["value"]

                assets = current["current_assets"]["value"]
                liabilities = current["current_liabilities"]["value"]

                # Perform verified Python calculations
                growth = revenue_growth(
                    revenue_2024, revenue_2023
                )

                margin = operating_margin(
                    op_income, revenue_2024
                )

                liquidity = current_ratio(
                    assets, liabilities
                )

                # Display results
                st.success("SEC data retrieved successfully!")

                st.subheader("Apple Inc. — FY 2024")

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Revenue Growth",
                    f"{growth:.2f}%"
                )

                col2.metric(
                    "Operating Margin",
                    f"{margin:.2f}%"
                )

                col3.metric(
                    "Current Ratio",
                    f"{liquidity:.2f}"
                )

                st.subheader("Reported Financial Data")

                st.table({
                    "Metric": [
                        "2024 Revenue",
                        "2023 Revenue",
                        "2024 Operating Income",
                        "2024 Current Assets",
                        "2024 Current Liabilities"
                    ],
                    "USD Billions": [
                        round(revenue_2024 / 1e9, 2),
                        round(revenue_2023 / 1e9, 2),
                        round(op_income / 1e9, 2),
                        round(assets / 1e9, 2),
                        round(liabilities / 1e9, 2)
                    ]
                })

                st.caption(
                    "Fiscal 2024 ended September 28, 2024. "
                    "Fiscal 2023 ended September 30, 2023."
                )

                st.link_button(
                    "View Source: SEC Company Facts",
                    "https://data.sec.gov/api/xbrl/"
                    "companyfacts/CIK0000320193.json"
                )

            except requests.exceptions.RequestException as error:
                st.error(f"SEC connection failed: {error}")

            except (ValueError, KeyError, TypeError) as error:
                st.error(f"Analysis could not be completed: {error}")


    # DYNAMIC COMPANY LOOKUP
    st.divider()

    st.header("🔎 Company Lookup")

    ticker_input = st.text_input(
        "Stock Ticker",
        value="MSFT"
    )

    if st.button("Find Company"):
        try:
            company = get_company_by_ticker(ticker_input)
            st.write(company)
        except ValueError as error:
            st.warning(str(error))

    #NEW DYNAMIC DASHBOARD
    render_company_dashboard()
    
#AUTOMATION
with automation_tab:

    st.header("Automation Center")

    st.write(
        "Create workflows that help Atlas perform "
        "tasks automatically."
    )

    st.info("Automation tools coming soon.")