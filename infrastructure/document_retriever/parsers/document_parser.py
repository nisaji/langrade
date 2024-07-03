from .word_parser import WordParser
from .excel_parser import ExcelParser
from .pdf_parser import PDFParser
from .csv_parser import CSVParser


class DocumentParser:
    def parse(self, file_path: str, file_type: str):
        if file_type == "word":
            parser = WordParser()
        elif file_type == "excel":
            parser = ExcelParser()
        elif file_type == "pdf":
            parser = PDFParser()
        elif file_type == "csv":
            parser = CSVParser()
        else:
            raise ValueError("Unsupported file type")
        return parser.parse(file_path)
