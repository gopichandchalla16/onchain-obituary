import os
import requests
from dotenv import load_dotenv
from prompts import AUTOPSY_PROMPT

load_dotenv()


def run_autopsy(contract_address, project_name, tx_summary, github_summary, price_summary):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in HuggingFace Secrets.")

    filled_prompt = AUTOPSY_PROMPT.format(
        contract_address=contract_address,
        project_name=project_name,
        tx_summary=tx_summary,
        github_summary=github_summary,
        price_summary=price_summary,
    )

    response = requests.post(
        url="https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": filled_prompt}
            ],
            "temperature": 0.85,
            "max_tokens": 1024,
        },
        timeout=60,
    )

    data = response.json()
    if "choices" not in data:
        raise ValueError(f"Groq API error: {data}")
    return data["choices"][0]["message"]["content"]
