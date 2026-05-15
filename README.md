# 💀 On-Chain Obituary

> Paste a dead crypto project. Get its autopsy.

On-Chain Obituary is an AI-powered forensic tool that analyses dead or rugged crypto projects. Give it a token contract address and it pulls on-chain transaction data, GitHub activity, and price history — then an LLM agent writes a brutal, darkly funny autopsy report.

**Built for Activate AI Fellows Summer 2026 by [Gopichand Challa](https://github.com/gopichandchalla16)**

---

## 🔬 What It Does

- Fetches last 50 token transactions via Etherscan API
- Pulls 90-day price history from CoinGecko
- Checks GitHub commit activity
- Runs a LangChain + Groq LLaMA agent that writes a structured forensic autopsy

## 🧾 Autopsy Report Includes

- **Cause of Death** — one brutal sentence
- **Time of Death** — when activity flatlined
- **Warning Signs** — red flags visible 30 days before collapse
- **Autopsy Findings** — what actually killed it
- **Final Verdict** — ruthless, honest
- **Lessons for the Living** — what builders should learn

---

## 🚀 Quick Start

```bash
git clone https://github.com/gopichandchalla16/onchain-obituary
cd onchain-obituary
pip install -r requirements.txt
```

Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key
ETHERSCAN_API_KEY=your_etherscan_api_key
GITHUB_TOKEN=your_github_token
```

Run:
```bash
streamlit run app.py
```

---

## 🌐 Deploy on HuggingFace Spaces

1. Create a new Streamlit Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Push this repo
3. Add secrets: `GROQ_API_KEY`, `ETHERSCAN_API_KEY`, `GITHUB_TOKEN`

---

## 🛠 Tech Stack

- **LLM:** Groq LLaMA 3 70B via LangChain
- **On-chain data:** Etherscan API
- **Price data:** CoinGecko API
- **GitHub data:** GitHub REST API
- **UI:** Streamlit
- **Deploy:** HuggingFace Spaces

---

## ⚠️ Example Projects to Try

- Terra Luna (LUNA)
- Squid Game Token (SQUID)
- Iron Finance (TITAN)
- Frosties NFT

---

*On-Chain Obituary — because the data always told the truth. Nobody was listening.*
