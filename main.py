import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.chat_models import AzureChatOpenAI
from tools.dbt_generator import generate_dbt_from_excel

# Load environment variables
load_dotenv()

EYQ_INCUBATOR_ENDPOINT = os.getenv("EYQ_INCUBATOR_ENDPOINT")
EYQ_INCUBATOR_KEY = os.getenv("EYQ_INCUBATOR_KEY")
EYQ_API_VERSION = os.getenv("EYQ_API_VERSION")

llm = AzureChatOpenAI(
    openai_api_base=EYQ_INCUBATOR_ENDPOINT,
    openai_api_key=EYQ_INCUBATOR_KEY,
    openai_api_version=EYQ_API_VERSION,
    deployment_name="gpt-4.1",
    model_name="gpt-4",
    temperature=0
)

tools = [
    Tool(
        name="GenerateDBTModel",
        func=generate_dbt_from_excel,
        description="Use this tool to generate DBT model SQL and schema.yml from an Excel-based S2T mapping file"
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

response = agent.run("Generate DBT model from CTMS_S2T_Detailed_Mapping.xlsx")
print(response)
