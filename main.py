import os
import argparse
from dotenv import load_dotenv
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from tools.dbt_generator import generate_dbt_from_excel

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate DBT model from S2T mapping Excel file using LangChain agent.")
    parser.add_argument("filename", type=str, help="Path to the S2T mapping Excel file")
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()
    EYQ_INCUBATOR_ENDPOINT = os.getenv("EYQ_INCUBATOR_ENDPOINT")
    EYQ_INCUBATOR_KEY = os.getenv("EYQ_INCUBATOR_KEY")
    EYQ_API_VERSION = os.getenv("EYQ_API_VERSION")

    # Initialize AzureChatOpenAI
    llm = AzureChatOpenAI(
        azure_endpoint=EYQ_INCUBATOR_ENDPOINT,
        api_key=EYQ_INCUBATOR_KEY,
        api_version=EYQ_API_VERSION,
        azure_deployment="gpt-4.1",
        model="gpt-4",
        temperature=0
    )

    # Define the tool
    tools = [
        Tool(
            name="PharmaDBTModel",
            func=generate_dbt_from_excel,
            description="Use this tool to generate DBT model SQL and schema.yml from an Excel-based S2T mapping file. Provide the full path or filename as input.",
            return_direct=True
        )
    ]

    # Define the prompt template with required variables
    prompt_template = PromptTemplate.from_template("""
You are PharmaDBTModelBuilder, an AI agent specialized in building clinical trial data products using DBT.

Your goal is to:
- Parse the S2T mapping file
- Generate DBT-compliant SQL transformations and schema files for clinical trial data domains.
- Create schema.yml with:
    Column descriptions
    Tests (e.g., not_null, unique)
    Tags or metadata
- Save files to a DBT model folder structure.
You are optimized for pharmaceutical clinical trial data, including domains like DM, AE, LB, and SDTM/ADaM standards.

You have access to the following tools:
{tools}

Use these tools as needed. Tool names: {tool_names}

When responding, follow this format:

Thought: [your reasoning]
Action: [tool name]
Action Input: [input to the tool]

Begin!

Question: {input}
{agent_scratchpad}
""")
    # Create the agent using LangChain's built-in ReAct agent constructor
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt_template)

    # Create the executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    # Run the agent with the provided filename
    response = agent_executor.invoke({"input": f"Generate DBT model from {args.filename}"})
    print(response)

if __name__ == "__main__":
    main()

# import os
# from dotenv import load_dotenv
# from langchain.agents import initialize_agent, Tool
# from langchain.agents.agent_types import AgentType
# from langchain_community.chat_models import AzureChatOpenAI  # Use the community version for Azure compatibility
# from tools.dbt_generator import generate_dbt_from_excel

# # Ensure your deployment_name below matches exactly what you have in your Azure OpenAI portal (case-sensitive)

# # Load environment variables
# load_dotenv()

# EYQ_INCUBATOR_ENDPOINT = os.getenv("EYQ_INCUBATOR_ENDPOINT")  # Should end with /openai/
# EYQ_INCUBATOR_KEY = os.getenv("EYQ_INCUBATOR_KEY")
# EYQ_API_VERSION = os.getenv("EYQ_API_VERSION")

# llm = AzureChatOpenAI(
#     # openai_api_base should be the base endpoint, e.g.:
#     # https://eyq-incubator.asiapac.fabric.ey.com/eyq/as/api/openai/
#     openai_api_base=EYQ_INCUBATOR_ENDPOINT,
#     openai_api_key=EYQ_INCUBATOR_KEY,
#     openai_api_version=EYQ_API_VERSION,
#     deployment_name="gpt-4.1",  # <-- Update this to match your Azure OpenAI deployment name exactly
#     model_name="gpt-4",
#     temperature=0
# )

# tools = [
#     Tool(
#         name="PharmaDBTModel",
#         func=generate_dbt_from_excel,
#         description="Use this tool to generate DBT model SQL and schema.yml from an Excel-based S2T mapping file"
#     )
# ]

# agent = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )

# response = agent.run("Generate DBT model from CTMS_S2T_Detailed_Mapping.xlsx")
# print(response)
