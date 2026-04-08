from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import save_tool

import pathlib
import yaml



load_dotenv() # Loads the API Key for the project

# Structures the output response of the AI
class AgentResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]
    

llm = ChatOpenAI(model="gpt-5.4-pro")
parser = PydanticOutputParser(pydantic_object=AgentResponse)

spec_file = "spec.txt"

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You will be given a design specification that describes the behavior of a hardware module.
            The goal is to generate the design artifacts that ultimately lead to a working hardware implementation.
            
            In the hackathon framework, the process begins with a specification file and ends with a tapeout-ready design. A simplified workflow looks like this: 
            Specification → RTL → synthesis → physical design → GDS
            
            You will focus on one stage of the flow and evaluate your approach on more complex examples.
            Use an LLM to write RTL for a given specification
            • Evaluate the RTL using the provided testbench or use an agent to generate a testbench
            • Use an LLM to write a script that runs OpenROAD flow-scripts by generating the required intermediate files
            
            Your agent capabilities include:
            ● generating RTL from a specification
            ● generating testbenches
            ● analyzing design outputs and improving the solution


            An example of the spec.txt is provided to you here (# Try to access the actual spec.txt file here for input)


            An example of the design.v output generated 


            Tools Required:
            ● iverilog
            ● OpenROAD
            ● Python


            Answer the user query and use neccessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [save_tool]

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("What can i help you research? ")
raw_response = agent_executor.invoke({"query": query}) # Need to automate this part (intead of typing into cmd terminal, want to automatically run fixes)




try:
    structured_response = parser.parse(raw_response.get("output")[0]["text"])
    print(structured_response)
except Exception as e:
    print("Error parsing response", e, "Raw Response - ", raw_response)
