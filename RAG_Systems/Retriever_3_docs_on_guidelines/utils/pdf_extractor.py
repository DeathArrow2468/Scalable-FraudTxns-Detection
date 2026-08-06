import fitz
from utils.models import Page

class PDFExtractor:
    @staticmethod
    def extract(file_path):
        pages = []
        pdf = fitz.open(file_path)

        for i, page in enumerate(pdf):
            text = page.get_text("text")
            pages.append(
                Page(
                    page_number=i + 1,
                    text=text,
                    char_count=len(text)
                )
            )

        pdf.close()
        return pages