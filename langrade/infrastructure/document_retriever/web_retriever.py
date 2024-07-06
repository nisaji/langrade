from typing import List, Union
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from langrade.domain.models import KnowledgeInput
from .base import DocumentRetriever


class WebDocumentRetriever(DocumentRetriever):
    def __init__(self, urls: List[str], api_key: str):
        self.urls = urls
        self.api_key = api_key
        self.vectorstore = self._create_vectorstore()

    def _load_documents(self):
        docs = [WebBaseLoader(url).load() for url in self.urls]
        return [item for sublist in docs for item in sublist]

    def _create_vectorstore(self):
        docs_list = self._load_documents()
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=250, chunk_overlap=0
        )
        doc_splits = text_splitter.split_documents(docs_list)
        return Chroma.from_documents(
            documents=doc_splits,
            collection_name="rag-chroma",
            embedding=OpenAIEmbeddings(),
        )

    def get_relevant_documents(
        self, question: Union[str, KnowledgeInput], top_k: int = 3
    ):
        if isinstance(question, KnowledgeInput):
            question_content = question.get_content()
        else:
            question_content = question

        retriever = self.vectorstore.as_retriever()
        return retriever.get_relevant_documents(question_content, k=top_k)
