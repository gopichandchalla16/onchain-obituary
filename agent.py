import os
from dotenv import load_dotenv
import google.generativeai as genai
from prompts import AUTOPSY_PROMPT

load_dotenv()


def run_autopsy(contract_address, project_name, tx_summary, github_summary, price_summary):
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        raise ValueError(
            "GEMINI_API_KEY is not set. Please add it in HuggingFace Space Settings → Variables and Secrets."
        )

    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    filled_prompt = AUTOPSY_PROMPT.format(
        contract_address=contract_address,
        project_name=project_name,
        tx_summary=tx_summary,
        github_summary=github_summary,
        price_summary=price_summary,
    )

    response = model.generate_content(filled_prompt)
    return response.text
