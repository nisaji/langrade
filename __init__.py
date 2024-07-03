from .config.settings import initialize_llm
from .application.document_grader import DocumentGrader
from .infrastructure.document_retriever.web_retriever import (
    WebDocumentRetriever,
)  # noqa: E501
from .infrastructure.document_retriever.recursive_web_retriever import (
    RecursiveWebDocumentRetriever,
)
from .infrastructure.document_retriever.documentdb_retriever import (
    DocumentDBRetriever,
)  # noqa: E501
from .infrastructure.document_retriever.parsers.document_parser import (
    DocumentParser,
)  # noqa: E501


def document_grader(reasoning=True):
    llm = initialize_llm()
    return DocumentGrader(llm, reasoning)


def web_document_retriever(urls):
    return WebDocumentRetriever(urls)


def recursive_web_document_retriever(origin, pages):
    return RecursiveWebDocumentRetriever(origin, pages)


def documentdb_retriever(uri, db_name, collection_name, num_docs):
    return DocumentDBRetriever(uri, db_name, collection_name, num_docs)


def document_parser():
    return DocumentParser()
