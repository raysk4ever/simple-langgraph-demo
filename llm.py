from dotenv import load_dotenv
load_dotenv()
# from ollama import Client
# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from langchain_openai import OpenAI

llm = ChatOllama(
    # base_url=="http://localhost:11434",
    # model="phi:latest",
    model="qwen3:8b",
    temperature=0
)

# import os
# key = os.environ.get('OPENAI_API_KEY')
# llm = OpenAI(api_key=key)


def call_llm(messages: list) -> str:
    try:
        print("Calling LLM...")
        print("messages:", messages)
        # ollama api call
        prompt = """
        You are a helpful AI assistant. Respond to the following messages:
        {messages}
        """.format(messages=messages)
        response = llm.generate(model="qwen3:8b", prompt=prompt)
        return response
    except Exception as e:
        print("Error calling LLM:", str(e))
        return "Error: Unable to get response from LLM."