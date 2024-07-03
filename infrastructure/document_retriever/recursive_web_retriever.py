from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from .base import DocumentRetriever


class RecursiveWebDocumentRetriever(DocumentRetriever):
    def __init__(self, origin: str, pages: int):
        self.origin = origin
        self.pages = pages
        self.vectorstore = self._create_vectorstore()

    def _load_documents(self):
        docs = []
        for page in range(1, self.pages + 1):
            url = f"{self.origin}/page/{page}"
            docs.extend(WebBaseLoader(url).load())
        return docs

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

    def get_relevant_documents(self, question: str, top_k: int = 3):
        retriever = self.vectorstore.as_retriever()
        return retriever.get_relevant_documents(question, k=top_k)
