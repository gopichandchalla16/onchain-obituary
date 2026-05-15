import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from prompts import AUTOPSY_PROMPT

load_dotenv()


def run_autopsy(contract_address, project_name, tx_summary, github_summary, price_summary):
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-70b-8192",
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
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(
        contract_address=contract_address,
        project_name=project_name,
        tx_summary=tx_summary,
        github_summary=github_summary,
        price_summary=price_summary,
    )
