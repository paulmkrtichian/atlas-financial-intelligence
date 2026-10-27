import streamlit as st

from ai.engine import ask_atlas
from ui.company_dashboard import render_company_dashboard
from ui.history_dashboard import render_history_dashboard
from ui.profitability_dashboard import render_profitability_dashboard
from ui.comparison_dashboard import render_comparison_dashboard
from ui.mapping_dashboard import render_mapping_dashboard
# Application settings
st.set_page_config(
    page_title="Atlas AI V3",
    page_icon="🧠",
    layout="wide"
)


# Main header
st.title("🧠 Atlas AI")

st.caption(
    "Personal Intelligence | Finance | Research | Automation"
)


# Main navigation
assistant_tab, finance_tab, automation_tab = st.tabs([
    "🧠 Assistant",
    "📊 Finance",
    "⚙️ Automation"
])


# PERSONAL ASSISTANT
with assistant_tab:

    st.header("Personal AI Assistant")

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
                    st.error(f"AI connection error: {error}")

        else:
            st.warning("Please enter a question.")


# FINANCIAL INTELLIGENCE
with finance_tab:
    render_history_dashboard()
    render_company_dashboard()
    render_profitability_dashboard()
    render_comparison_dashboard()
    render_mapping_dashboard()

# AUTOMATION
with automation_tab:

    st.header("⚙️ Automation Center")

    st.info("AI-powered workflows coming soon.")