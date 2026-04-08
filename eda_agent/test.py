import yaml
import os

from dotenv import load_dotenv


from openai import OpenAI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# Path constants
INPUT_YAML_PATH = "./github_files/p1.yaml"
ENV_FILE_NAME = "my_api_key.env"



def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def generate_rtl(spec):
    module_name = list(spec.keys())[0]
    details = spec[module_name]

    print(f'details {details}')

    # Call something with the AGENTS.md file






def main():

    load_dotenv(ENV_FILE_NAME) # Loads the API Key for the project

    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in .env file")
        exit(1)

    print(os.getenv("OPENAI_API_KEY"))

    llm = ChatOpenAI(model="gpt-4o") # Wasn't working with 5.4 pro


    # Load the input .yaml file for 
    spec = load_yaml(INPUT_YAML_PATH)

    module_name = list(spec.keys())[0]
    print(module_name)
    print(spec.keys())

    rtl = generate_rtl(spec)

    clock = spec[module_name]["clock_period"]
    print(f'clock {clock}')

    # Format Solution Directory like what is talked about in README.md in provided Github
    os.makedirs("../solutions/p1/", exist_ok=True)

    with open("../solutions/p1/design.v", "w") as f:
        f.write(rtl)

    print("Done!")

if __name__ == "__main__":
    main()
