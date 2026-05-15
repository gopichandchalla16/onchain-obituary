import os
from dotenv import load_dotenv
from google import genai
from prompts import AUTOPSY_PROMPT

load_dotenv()


def run_autopsy(contract_address, project_name, tx_summary, github_summary, price_summary):
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        raise ValueError(
            "GEMINI_API_KEY is not set. Please add it in HuggingFace Space Settings → Variables and Secrets."
        )

    client = genai.Client(api_key=gemini_key)

    filled_prompt = AUTOPSY_PROMPT.format(
        contract_address=contract_address,
        project_name=project_name,
        tx_summary=tx_summary,
        github_summary=github_summary,
        price_summary=price_summary,
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=filled_prompt,
    )
    return response.text
