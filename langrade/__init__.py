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
from .infrastructure.llm.factory import create_llm_engine


def document_grader(
    api_key: str,
    engine_type: str = "openai",
    model: str = "gpt-3.5-turbo-0125",
    reasoning: bool = True,
):
    llm_engine = create_llm_engine(engine_type, api_key, model)
    return DocumentGrader(llm_engine, reasoning)


def web_document_retriever(urls, api_key: str):
    return WebDocumentRetriever(urls, api_key)


def recursive_web_document_retriever(origin, pages, api_key: str):
    return RecursiveWebDocumentRetriever(origin, pages, api_key)


def documentdb_retriever(
    uri, db_name, collection_name, num_docs, api_key: str
):  # noqa: E501
    return DocumentDBRetriever(
        uri, db_name, collection_name, num_docs, api_key
    )  # noqa: E501


def document_parser():
    return DocumentParser()
