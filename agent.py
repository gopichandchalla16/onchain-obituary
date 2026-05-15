import os
from dotenv import load_dotenv
from mistralai import Mistral
from prompts import AUTOPSY_PROMPT

load_dotenv()


def run_autopsy(contract_address, project_name, tx_summary, github_summary, price_summary):
    mistral_key = os.environ.get("MISTRAL_API_KEY")
    if not mistral_key:
        raise ValueError(
            "MISTRAL_API_KEY is not set. Please add it in HuggingFace Space Settings → Variables and Secrets."
        )

    client = Mistral(api_key=mistral_key)

    filled_prompt = AUTOPSY_PROMPT.format(
        contract_address=contract_address,
        project_name=project_name,
        tx_summary=tx_summary,
        github_summary=github_summary,
        price_summary=price_summary,
    )

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {"role": "user", "content": filled_prompt}
        ],
    )
    return response.choices[0].message.content
