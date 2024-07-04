from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from .base import LLMEngine


class OpenAIEngine(LLMEngine):
    def __init__(self, api_key: str, model: str):
        self.llm = ChatOpenAI(api_key=api_key, model=model)

    def generate(self, prompt: str) -> str:
        return self.llm.predict(prompt)

    def with_structured_output(self, output_parser_class):
        prompt = PromptTemplate(
            input_variables=["document", "question"],
            template="Document: {document}\n\nQuestion: {question}\n\nAnswer:",
        )
        output_parser = output_parser_class()
        return LLMChain(
            llm=self.llm,
            prompt=prompt,
            output_parser=output_parser,
            output_key="text",  # noqa: E501
        )
