import os
import time
import requests
from collections import Counter
from datetime import datetime
from dotenv import load_dotenv
 
load_dotenv()
 
ETHERSCAN_KEY = os.environ.get("ETHERSCAN_API_KEY")
 
 
def _unix_to_date(ts):
    try:
        return datetime.utcfromtimestamp(int(ts)).strftime("%Y-%m-%d")
    except Exception:
        return "unknown"
 
 
def get_tx_summary(contract_address):
    if not contract_address or not contract_address.startswith("0x"):
        return "Invalid contract address — must start with 0x."
    if not ETHERSCAN_KEY:
        return "Etherscan API key not configured — skipping on-chain data."
 
    url = "https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "tokentx",
        "contractaddress": contract_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": ETHERSCAN_KEY,
        "offset": 100,
        "page": 1,
    }
 
    try:
        r = requests.get(url, params=params, timeout=12)
        r.raise_for_status()
        data = r.json()
 
        if data.get("status") != "1" or not data.get("result"):
            return (
                "No Ethereum token transfer records found for this contract. "
                "Note: If this is a Terra, BSC, Solana, or other non-Ethereum token, "
                "Etherscan only covers the Ethereum mainnet — "
                "the LLM will still analyse based on price and GitHub data."
            )
 
        txs = data["result"]
        sample = txs[:100]
 
        senders = [t["from"].lower() for t in sample]
        receivers = [t["to"].lower() for t in sample]
        unique_wallets = len(set(senders + receivers))
 
        last_ts = _unix_to_date(txs[0]["timeStamp"])
        first_ts = _unix_to_date(txs[-1]["timeStamp"])
 
        sender_counts = Counter(senders)
        top_sender, top_count = sender_counts.most_common(1)[0]
        top_pct = round((top_count / len(sample)) * 100, 1)
        short_addr = top_sender[:10] + "..."
 
        if top_pct > 30:
            concentration_note = (
                short_addr + " initiated " + str(top_pct)
                + "% of sampled txs — HIGH concentration, likely a dev or bot wallet."
            )
        else:
            concentration_note = (
                short_addr + " initiated " + str(top_pct)
                + "% of sampled txs — concentration looks normal."
            )
 
        to_contract = sum(
            1 for t in sample if t["to"].lower() == contract_address.lower()
        )
        from_contract = sum(
            1 for t in sample if t["from"].lower() == contract_address.lower()
        )
 
        return (
            "Sampled " + str(len(sample)) + " most recent Ethereum token transfers. "
            + "Unique wallets involved: " + str(unique_wallets) + ". "
            + "Oldest tx in sample: " + first_ts + ". "
            + "Most recent tx: " + last_ts + ". "
            + concentration_note
            + " Transfers TO contract (sell-side proxy): " + str(to_contract) + ". "
            + "Transfers FROM contract (buy-side proxy): " + str(from_contract) + "."
        )
 
    except requests.exceptions.Timeout:
        return "Etherscan request timed out — on-chain data unavailable for this run."
    except requests.exceptions.RequestException as e:
        return "Etherscan request failed: " + str(e)
    except Exception as e:
        return "Could not process on-chain data: " + str(e)
 
 
def get_price_summary(token_id):
    if not token_id or not token_id.strip():
        return "No CoinGecko token ID provided — skipping price history."
 
    token_id = token_id.strip().lower()
 
    def _fetch(days):
        url = (
            "https://api.coingecko.com/api/v3/coins/"
            + token_id
            + "/market_chart"
        )
        params = {"vs_currency": "usd", "days": str(days)}
        return requests.get(url, params=params, timeout=15)
 
    try:
        r = _fetch(365)
 
        if r.status_code == 404:
            return (
                "Token ID '" + token_id + "' not found on CoinGecko. "
                "It may be delisted or the ID may be misspelled. "
                "Check the CoinGecko URL: coingecko.com/en/coins/" + token_id
            )
 
        if r.status_code == 429:
            time.sleep(10)
            r = _fetch(365)
 
        if r.status_code == 429:
            time.sleep(30)
            r = _fetch(90)
 
        if r.status_code == 429:
            return (
                "CoinGecko free-tier rate limit reached. "
                "Price data skipped for this run — "
                "the autopsy will rely on on-chain and GitHub evidence. "
                "Try again in 60 seconds for price data."
            )
 
        r.raise_for_status()
        data = r.json()
        prices = [p[1] for p in data.get("prices", [])]
 
        if not prices:
            return (
                "CoinGecko returned no price data for '" + token_id + "'. "
                "Token may be fully delisted."
            )
 
        peak = max(prices)
        trough = min(prices)
        current = prices[-1]
        start = prices[0]
        total_pts = len(prices)
 
        drop_from_peak = (
            round(((peak - current) / peak) * 100, 1) if peak > 0 else 0
        )
 
        if start > 0:
            pct_change = round(((current - start) / start) * 100, 1)
            if pct_change >= 0:
                change_str = "+" + str(pct_change) + "% from period start"
            else:
                change_str = str(pct_change) + "% from period start"
        else:
            change_str = "change from start unavailable"
 
        peak_idx = prices.index(peak)
        if peak_idx < total_pts * 0.33:
            peak_position = "early in the period"
        elif peak_idx < total_pts * 0.66:
            peak_position = "mid-period"
        else:
            peak_position = "late in the period"
 
        return (
            str(total_pts) + " price data points retrieved. "
            + "Opening price: $" + str(round(start, 8)) + ". "
            + "Peak price: $" + str(round(peak, 6))
            + " (reached " + peak_position + "). "
            + "All-time low in window: $" + str(round(trough, 10)) + ". "
            + "Last recorded price: $" + str(round(current, 8)) + ". "
            + "Drop from peak: " + str(drop_from_peak) + "%. "
            + change_str + "."
        )
 
    except requests.exceptions.Timeout:
        return "CoinGecko request timed out — price data unavailable for this run."
    except requests.exceptions.RequestException as e:
        return "CoinGecko request failed: " + str(e)
    except Exception as e:
        return "Could not process price data: " + str(e)
