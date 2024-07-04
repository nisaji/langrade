from abc import ABC, abstractmethod


class DocumentRetriever(ABC):
    @abstractmethod
    def get_relevant_documents(self, question: str, top_k: int = 3):
        pass
