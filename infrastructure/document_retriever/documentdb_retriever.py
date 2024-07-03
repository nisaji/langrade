from pymongo import MongoClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from .base import DocumentRetriever


class DocumentDBRetriever(DocumentRetriever):
    def __init__(
        self, uri: str, db_name: str, collection_name: str, num_docs: int
    ):  # noqa: E501
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.num_docs = num_docs
        self.vectorstore = self._create_vectorstore()

    def _load_documents(self):
        client = MongoClient(self.uri)
        db = client[self.db_name]
        collection = db[self.collection_name]
        docs = list(collection.find().limit(self.num_docs))
        return [doc["content"] for doc in docs if "content" in doc]

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
