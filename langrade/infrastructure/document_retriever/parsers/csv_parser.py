import csv
from langrade.infrastructure.document_retriever.parsers.base import BaseParser


class CSVParser(BaseParser):
    def parse(self, file_path: str) -> str:
        content = []
        with open(file_path, "r", newline="", encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                content.append(", ".join(row))
        return "\n".join(content)
