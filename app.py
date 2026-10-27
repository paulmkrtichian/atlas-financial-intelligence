import streamlit as st

from ai.engine import ask_atlas
from ui.scenario_dashboard import render_scenario_dashboard
from ui.company_dashboard import render_company_dashboard
from ui.history_dashboard import render_history_dashboard
from ui.profitability_dashboard import render_profitability_dashboard
from ui.comparison_dashboard import render_comparison_dashboard
from ui.mapping_dashboard import render_mapping_dashboard
from ui.research_dashboard import render_research_dashboard
from ui.ai_analyst_dashboard import render_ai_analyst_dashboard
# --------------------------------------------------
# APPLICATION SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="Atlas | Financial Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# VISUAL STYLING
# --------------------------------------------------

st.markdown("""
<style>

.block-container {
    max-width: 1280px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    letter-spacing: -0.025em;
}

div[data-testid="stMetric"] {
    background: #172338;
    border: 1px solid #293C58;
    border-radius: 14px;
    padding: 18px;
}

.atlas-hero {
    background: linear-gradient(
        120deg,
        #14243D,
        #101A2E
    );
    border: 1px solid #293C58;
    border-radius: 18px;
    padding: 38px;
    margin-bottom: 24px;
}

.atlas-eyebrow {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 2px;
    color: #87B8FF;
}

.atlas-hero h1 {
    color: #F3F7FE;
    font-size: 42px;
    line-height: 1.15;
    margin-top: 12px;
}

.atlas-hero p {
    color: #ACBCD2;
    font-size: 16px;
    line-height: 1.6;
    max-width: 660px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

PAGES = [
    "Overview",
    "Public Markets",
    "Private Companies",
    "Research Intelligence",
    "AI Financial Analyst",
    "Scenario Modeling",
    "Automation"
]


def navigate_to(page):
    st.session_state.atlas_page = page


if st.session_state.get("atlas_page") not in PAGES:
    st.session_state["atlas_page"] = "Overview"


with st.sidebar:

    st.title("ATLAS")

    st.caption("FINANCIAL INTELLIGENCE · V3")

    st.divider()

    st.radio(
        "Workspace Navigation",
        PAGES,
        key="atlas_page",
        label_visibility="collapsed"
    )

    st.divider()

    st.caption("LOCAL-FIRST RESEARCH PLATFORM")

    st.caption(
        "SEC financial data · Private financial imports · "
        "AI-assisted analysis"
    )


page = st.session_state.atlas_page


# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

if page == "Overview":

    st.markdown("""
    <div class="atlas-hero">
        <div class="atlas-eyebrow">
            ATLAS / RESEARCH WORKSPACE
        </div>
        <h1>Financial intelligence,<br>
        without the clutter.</h1>
        <p>
            Analyze public and private companies,
            explore historical financial performance,
            and generate AI-assisted research
            from a single workspace.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Explore Atlas")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):

            st.subheader("Public Markets")

            st.write(
                "SEC financial statements, historical trends, "
                "profitability ratios, and company comparisons."
            )

            st.button(
                "Open Public Markets",
                on_click=navigate_to,
                args=("Public Markets",),
                use_container_width=True
            )

    with col2:
        with st.container(border=True):

            st.subheader("Private Companies")

            st.write(
                "Import Excel and CSV financial statements, "
                "standardize columns, and analyze performance."
            )

            st.button(
                "Open Private Companies",
                on_click=navigate_to,
                args=("Private Companies",),
                use_container_width=True
            )

    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):

            st.subheader("AI Assistant")

            st.write(
                "Interact with your local AI model "
                "for explanations and research support."
            )

            st.button(
                "Open AI Assistant",
                on_click=navigate_to,
                args=("AI Assistant",),
                use_container_width=True
            )

    with col4:
        with st.container(border=True):

            st.subheader("Automation")

            st.write(
                "A future workspace for financial "
                "research and productivity workflows."
            )

            st.caption("Development planned")


# --------------------------------------------------
# SCENARIO MODELING
# --------------------------------------------------

elif page == "Scenario Modeling":

    render_scenario_dashboard()

# --------------------------------------------------
# AI ASSISTANT
# --------------------------------------------------

elif page == "AI Assistant":

    st.title("Atlas Assistant")

    st.caption(
        "Your local AI workspace for financial research, "
        "learning, and personal productivity."
    )

    # Initialize conversation history
    if "atlas_messages" not in st.session_state:
        st.session_state.atlas_messages = []

    # Clear conversation button
    if st.button("Clear Conversation"):

        st.session_state.atlas_messages = []
        st.rerun()

    st.divider()

    # Display previous messages
    for message in st.session_state.atlas_messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Modern chat input
    question = st.chat_input("Ask Atlas anything...")

    if question:

        # Show and save the user's message
        with st.chat_message("user"):
            st.markdown(question)

        # Include recent conversation context
        recent_messages = st.session_state.atlas_messages[-6:]

        context = "\n\n".join(
            f"{message['role'].upper()}: "
            f"{message['content'][:1000]}"
            for message in recent_messages
        )

        prompt = (
            "Use the conversation history as context "
            "for answering the latest question.\n\n"
            f"Conversation history:\n{context}\n\n"
            f"Latest user question:\n{question}"
        )

        st.session_state.atlas_messages.append({
            "role": "user",
            "content": question
        })

        # Generate Atlas's response
        with st.chat_message("assistant"):

            try:

                answer = st.write_stream(
                    ask_atlas(prompt)
                )

                st.session_state.atlas_messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:

                st.error(
                    f"Unable to generate response: {error}"
                )

# --------------------------------------------------
# PUBLIC MARKETS
# --------------------------------------------------

elif page == "Public Markets":

    st.title("Public Markets")

    st.caption(
        "SEC-powered research, financial statements, "
        "historical analysis, and company comparisons."
    )

    company_tab, history_tab, profit_tab, comparison_tab = (
        st.tabs([
            "Company Analysis",
            "Historical Trends",
            "Profitability",
            "Compare Companies"
        ])
    )

    with company_tab:
        render_company_dashboard()

    with history_tab:
        render_history_dashboard()

    with profit_tab:
        render_profitability_dashboard()

    with comparison_tab:
        render_comparison_dashboard()


# --------------------------------------------------
# PRIVATE COMPANIES
# --------------------------------------------------

elif page == "Private Companies":

    st.title("Private Companies")

    st.caption(
        "Import, standardize, and analyze financial "
        "statements from Excel and CSV files."
    )

    render_mapping_dashboard()


# --------------------------------------------------
# RESEARCH INTELLIGENCE
# --------------------------------------------------

elif page == "Research Intelligence":

    render_research_dashboard()

# --------------------------------------------------
# AI FINANCIAL ANALYST
# --------------------------------------------------

elif page == "AI Financial Analyst":
    render_ai_analyst_dashboard()

# --------------------------------------------------
# AUTOMATION
# --------------------------------------------------

elif page == "Automation":

    st.title("Automation Center")

    st.caption("Workflow development workspace.")

    st.info(
        "Automation capabilities are planned "
        "for a future Atlas V3 milestone."
    )