import os
import requests
from dotenv import load_dotenv
from prompts import AUTOPSY_PROMPT
 
load_dotenv()
 
 
def run_autopsy(contract_address, project_name, tx_summary, github_summary, price_summary):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set. Add it to HuggingFace Secrets or your .env file.")
 
    filled_prompt = AUTOPSY_PROMPT.format(
        contract_address=contract_address,
        project_name=project_name,
        tx_summary=tx_summary,
        github_summary=github_summary,
        price_summary=price_summary,
    )
 
    try:
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
                "max_tokens": 1200,
            },
            timeout=60,
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise ValueError("Groq API timed out. Try again.")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Network error calling Groq API: {str(e)}")
 
    data = response.json()
    if "choices" not in data:
        raise ValueError(f"Groq API returned unexpected response: {data}")
 
    return data["choices"][0]["message"]["content"]
