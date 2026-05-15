import streamlit as st
from chain import get_tx_summary, get_price_summary
from github_activity import get_github_summary
from agent import run_autopsy

st.set_page_config(
    page_title="On-Chain Obituary",
    page_icon="💀",
    layout="centered",
)

st.title("💀 On-Chain Obituary")
st.caption("Paste a dead crypto project. Get its autopsy.")
st.markdown(
    "Enter the details of a rugged, dead, or collapsed crypto project. "
    "The agent pulls on-chain data, checks GitHub activity, and writes a forensic autopsy report."
)

st.divider()

with st.form("autopsy_form"):
    project_name = st.text_input(
        "Project Name",
        placeholder="e.g. Terra Luna, Squid Game Token, Iron Finance",
    )
    contract_address = st.text_input(
        "Token Contract Address (EVM)",
        placeholder="0x...",
    )
    token_id = st.text_input(
        "CoinGecko Token ID (for price history)",
        placeholder="e.g. terra-luna, iron-titanium-token",
        help="Find this in the CoinGecko URL: coingecko.com/en/coins/[token-id]",
    )
    github_url = st.text_input(
        "GitHub Repo URL (optional)",
        placeholder="https://github.com/project/repo",
    )
    submitted = st.form_submit_button("🔬 Run Autopsy", use_container_width=True)

if submitted:
    if not project_name or not contract_address:
        st.error("⚠️ Project name and contract address are required.")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.spinner("On-chain data..."):
                tx_summary = get_tx_summary(contract_address)
            st.success("On-chain data ✓")
        with col2:
            with st.spinner("Price history..."):
                price_summary = get_price_summary(token_id) if token_id else "No CoinGecko ID provided."
            st.success("Price data ✓")
        with col3:
            with st.spinner("GitHub activity..."):
                github_summary = get_github_summary(github_url) if github_url else "No GitHub repo provided."
            st.success("GitHub data ✓")

        st.divider()

        with st.spinner("🔬 Writing autopsy report..."):
            try:
                report = run_autopsy(
                    contract_address=contract_address,
                    project_name=project_name,
                    tx_summary=tx_summary,
                    github_summary=github_summary,
                    price_summary=price_summary,
                )
                st.subheader(f"📋 Official Autopsy Report: {project_name}")
                st.markdown(report)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

        st.divider()
        st.caption(
            "On-Chain Obituary — built for Activate AI Fellows 2026 by "
            "[Gopichand Challa](https://github.com/gopichandchalla16)"
        )
