import PyPDF2
from langrade.infrastructure.document_retriever.parsers.base import BaseParser


class PDFParser(BaseParser):
    def parse(self, file_path: str) -> str:
        content = []
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                content.append(page.extract_text())
        return "\n".join(content)
