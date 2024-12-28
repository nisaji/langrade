from typing import List, Union
import numpy as np
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from .embeddings import VertexAIEmbeddings


class Retriever:
    def __init__(self, documents: List[Document], embeddings: VertexAIEmbeddings):
        self.documents = documents
        self.embeddings = embeddings
        self.doc_embeddings = None
        self._compute_embeddings()

    def _compute_embeddings(self):
        texts = [doc.page_content for doc in self.documents]
        self.doc_embeddings = self.embeddings.embed_documents(texts)

    def _cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def get_relevant_documents(self, query: str, k: int = 4) -> List[Document]:
        query_embedding = self.embeddings.embed_query(query)

        similarities = [
            self._cosine_similarity(query_embedding, doc_emb)
            for doc_emb in self.doc_embeddings
        ]

        top_k_idx = np.argsort(similarities)[-k:][::-1]
        return [self.documents[i] for i in top_k_idx]


def create_retriever(
    urls: list[str],
    credentials: Union[str, dict],
    embedding_model: str = "multilingual-e5-large",
):
    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, chunk_overlap=0
    )
    doc_splits = text_splitter.split_documents(docs_list)

    embeddings = VertexAIEmbeddings(credentials)
    return Retriever(doc_splits, embeddings)
