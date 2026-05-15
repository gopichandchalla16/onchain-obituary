import requests
import os
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_KEY = os.environ.get("ETHERSCAN_API_KEY")


def get_tx_summary(contract_address):
    if not ETHERSCAN_KEY:
        return "Etherscan API key not set — skipping on-chain data."
    url = "https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "tokentx",
        "contractaddress": contract_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": ETHERSCAN_KEY,
        "offset": 50,
        "page": 1,
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if data.get("status") != "1" or not data.get("result"):
            return "No transaction data found for this contract."
        txs = data["result"][:50]
        unique_wallets = len(set([t["from"] for t in txs] + [t["to"] for t in txs]))
        last_tx = txs[0]["timeStamp"]
        first_tx = txs[-1]["timeStamp"]
        return (
            f"Last 50 transactions found. Unique wallets: {unique_wallets}. "
            f"Most recent tx timestamp: {last_tx}. Oldest in sample: {first_tx}."
        )
    except Exception as e:
        return f"Could not fetch on-chain data: {str(e)}"


def get_price_summary(token_id):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{token_id.lower()}/market_chart"
        params = {"vs_currency": "usd", "days": "90"}
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        prices = [p[1] for p in data.get("prices", [])]
        if not prices:
            return "No price data — token likely delisted."
        peak = max(prices)
        current = prices[-1]
        drop = round(((peak - current) / peak) * 100, 1) if peak > 0 else 0
        return f"Peak: ${peak:.6f}. Last recorded: ${current:.6f}. Drop from peak: {drop}%."
    except Exception:
        return "Price data unavailable — token likely delisted or not on CoinGecko."
