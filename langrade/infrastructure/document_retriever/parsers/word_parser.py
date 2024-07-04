from docx import Document
from langrade.infrastructure.document_retriever.parsers.base import BaseParser


class WordParser(BaseParser):
    def parse(self, file_path: str) -> str:
        doc = Document(file_path)
        content = []
        for para in doc.paragraphs:
            content.append(para.text)
        return "\n".join(content)
