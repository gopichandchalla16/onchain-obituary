import streamlit as st
from chain import get_tx_summary, get_price_summary
from github_activity import get_github_summary
from agent import run_autopsy
 
st.set_page_config(
    page_title="On-Chain Obituary",
    page_icon="💀",
    layout="centered",
)
 
# ── Header ──────────────────────────────────────────────────────────────────
st.title("💀 On-Chain Obituary")
st.caption("Paste a dead crypto project. Get its autopsy.")
st.markdown(
    "Enter the details of a rugged, dead, or collapsed crypto project. "
    "The agent pulls on-chain transactions, 365-day price history, and GitHub commit data — "
    "then writes a forensic autopsy report."
)
 
with st.expander("ℹ️ How to find the inputs"):
    st.markdown(
        """
**Token Contract Address** — The EVM contract address (starts with `0x`).
Find it on Etherscan, CoinGecko, or DexScreener.
 
**CoinGecko Token ID** — The slug in the CoinGecko URL.
Example: `https://coingecko.com/en/coins/terra-luna` → ID is `terra-luna`
 
**GitHub Repo URL** — The team's main GitHub repository (optional but improves analysis).
Example: `https://github.com/terra-money/core`
 
**Projects to try:**
| Project | Contract | CoinGecko ID |
|---|---|---|
| Iron Finance (TITAN) | `0xaaa5b9e6c589642f98a1cda99b9d024b8407285a` | `iron-titanium-token` |
| Squid Game Token | `0x87230146E138d3F296a9a77e497A2A83012e9Bc5` | `squid-game` |
| SafeMoon | `0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3` | `safemoon` |
        """
    )
 
st.divider()
 
# ── Input Form ───────────────────────────────────────────────────────────────
with st.form("autopsy_form"):
    project_name = st.text_input(
        "Project Name *",
        placeholder="e.g. Terra Luna, Squid Game Token, Iron Finance",
    )
    contract_address = st.text_input(
        "Token Contract Address (EVM) *",
        placeholder="0x...",
    )
    token_id = st.text_input(
        "CoinGecko Token ID",
        placeholder="e.g. terra-luna, iron-titanium-token, safemoon",
        help="Find this in the CoinGecko URL: coingecko.com/en/coins/[token-id]",
    )
    github_url = st.text_input(
        "GitHub Repo URL (optional)",
        placeholder="https://github.com/project/repo",
    )
    submitted = st.form_submit_button("🔬 Run Autopsy", use_container_width=True)
 
# ── Execution ────────────────────────────────────────────────────────────────
if submitted:
    if not project_name.strip():
        st.error("⚠️ Project name is required.")
        st.stop()
    if not contract_address.strip() or not contract_address.strip().startswith("0x"):
        st.error("⚠️ A valid EVM contract address (starting with 0x) is required.")
        st.stop()
 
    st.divider()
    st.markdown("### 🔍 Gathering Evidence")
 
    col1, col2, col3 = st.columns(3)
 
    with col1:
        with st.spinner("On-chain data…"):
            tx_summary = get_tx_summary(contract_address.strip())
        if "error" in tx_summary.lower() or "unavailable" in tx_summary.lower():
            st.warning("On-chain ⚠️")
        else:
            st.success("On-chain ✓")
 
    with col2:
        with st.spinner("Price history…"):
            price_summary = (
                get_price_summary(token_id.strip())
                if token_id.strip()
                else "No CoinGecko token ID provided — skipping price history."
            )
        if "unavailable" in price_summary.lower() or "not found" in price_summary.lower():
            st.warning("Price ⚠️")
        else:
            st.success("Price ✓")
 
    with col3:
        with st.spinner("GitHub activity…"):
            github_summary = (
                get_github_summary(github_url.strip())
                if github_url.strip()
                else "No GitHub repository provided."
            )
        if "unavailable" in github_summary.lower() or "not found" in github_summary.lower():
            st.warning("GitHub ⚠️")
        else:
            st.success("GitHub ✓")
 
    # Show raw evidence in an expander for transparency
    with st.expander("📂 Raw Evidence Collected"):
        st.markdown(f"**On-chain:** {tx_summary}")
        st.markdown(f"**Price:** {price_summary}")
        st.markdown(f"**GitHub:** {github_summary}")
 
    st.divider()
 
    # Warn if no real data was retrieved
    all_empty = all([
        "not set" in tx_summary or "no transaction" in tx_summary.lower() or "invalid" in tx_summary.lower(),
        "no coingecko" in price_summary.lower() or "not provided" in price_summary.lower(),
        "not provided" in github_summary.lower(),
    ])
    if all_empty:
        st.warning(
            "⚠️ No data sources returned results. "
            "The report below will be based on the project name and contract address alone — "
            "accuracy will be limited. Check your API keys and inputs."
        )
 
    # Generate autopsy
    with st.spinner("🔬 Writing autopsy report…"):
        try:
            report = run_autopsy(
                contract_address=contract_address.strip(),
                project_name=project_name.strip(),
                tx_summary=tx_summary,
                github_summary=github_summary,
                price_summary=price_summary,
            )
            st.subheader(f"📋 Autopsy Report")
            st.markdown(report)
 
        except ValueError as e:
            st.error(f"❌ {str(e)}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
 
    st.divider()
    st.caption(
        "On-Chain Obituary — because the data always told the truth. Nobody was listening. | "
        "Built for Activate AI Fellows 2026 by "
        "[Gopichand Challa](https://github.com/gopichandchalla16)"
    )
