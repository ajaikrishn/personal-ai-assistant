from agent.agent_manager import run_assistant,process_user_input
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
def is_email_query(query):
    # Basic email intent check
    email_keywords = ["email", "mail", "inbox", "fetch", "read", "summarize"]
    return any(word in query.lower() for word in email_keywords)

def main():
    while True:
        query = input("Enter your query: ")
        response = chat_chain.invoke(query)
        if query.lower() == "exit":
            print("Exiting the assistant.")
            return
        elif is_email_query(query):
            print("📬 Fetching and summarizing your emails...")
            run_assistant()
        else :
            print(f"ai_response: {response['text']}") 
        
   

if __name__ == "__main__":
    main()
