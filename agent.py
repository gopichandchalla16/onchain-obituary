import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from prompts import AUTOPSY_PROMPT

load_dotenv()


def run_autopsy(contract_address, project_name, tx_summary, github_summary, price_summary):
    groq_key = os.environ.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    if not groq_key:
        raise ValueError(
            "GROQ_API_KEY is not set. Please add it in HuggingFace Space Settings → Variables and Secrets."
        )

    llm = ChatGroq(
        api_key=groq_key,
        model="llama3-70b-8192",
        temperature=0.85,
    )
    prompt = PromptTemplate(
        input_variables=[
            "contract_address",
            "project_name",
            "tx_summary",
            "github_summary",
            "price_summary",
        ],
        template=AUTOPSY_PROMPT,
    )
    chain = prompt | llm
    result = chain.invoke({
        "contract_address": contract_address,
        "project_name": project_name,
        "tx_summary": tx_summary,
        "github_summary": github_summary,
        "price_summary": price_summary,
    })
    return result.content
