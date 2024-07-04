from typing import Type
from langrade.infrastructure.document_retriever.parsers.base import BaseParser
from langrade.infrastructure.document_retriever.parsers.word_parser import (
    WordParser,
)  # noqa: E501
from langrade.infrastructure.document_retriever.parsers.excel_parser import (
    ExcelParser,
)  # noqa: E501
from langrade.infrastructure.document_retriever.parsers.pdf_parser import (
    PDFParser,
)  # noqa: E501
from langrade.infrastructure.document_retriever.parsers.csv_parser import (
    CSVParser,
)  # noqa: E501


class DocumentParser:
    def parse(self, file_path: str, file_type: str):
        parser_class: Type[BaseParser]
        if file_type == "word":
            parser_class = WordParser
        elif file_type == "excel":
            parser_class = ExcelParser
        elif file_type == "pdf":
            parser_class = PDFParser
        elif file_type == "csv":
            parser_class = CSVParser
        else:
            raise ValueError("Unsupported file type")

        parser = parser_class()
        return parser.parse(file_path)
