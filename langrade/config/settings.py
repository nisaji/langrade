from langchain_openai import ChatOpenAI


def initialize_llm(api_key, model="gpt-3.5-turbo-0125"):
    return ChatOpenAI(api_key=api_key, model=model)
