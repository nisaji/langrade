from langchain_openai import ChatOpenAI
from .grader import DocumentGrader


class DocumentGraderFactory:
    @staticmethod
    def create(
        api_key: str, model: str = "gpt-3.5-turbo-0125", reasoning: bool = True
    ) -> DocumentGrader:
        llm = ChatOpenAI(api_key=api_key, model=model)
        return DocumentGrader(llm, reasoning)
