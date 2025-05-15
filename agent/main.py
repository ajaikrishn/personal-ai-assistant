from agent_maneger import run_assistant,process_user_input
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from configure import *


llm = OllamaLLM(model="llama2")
prompt_template = PromptTemplate(
    input_variables=["query"],
    template=prompt
)

chat_chain = LLMChain(
    llm=llm,
    prompt=prompt_template
)

def handle_input(user_input):
    return process_user_input(user_input)  

def main():
    query = input("Enter your query: ")
    response = chat_chain.invoke(query)
    if query.lower() == "exit":
        print("Exiting the assistant.")
        return
    elif query.lower() == "fetch emails":
        run_assistant()
    elif query.lower()== query:
        print(f'ai_response: {response}')
    
   

if __name__ == "__main__":
    main()
