import fitz

from utils.models import Paper
from utils.models import Page


class PDFProcessor:

    @staticmethod
    def process(file_path):

        pdf = fitz.open(file_path)

        pages = []

        for i, page in enumerate(pdf):

            pages.append(
                Page(
                    page_number=i + 1,
                    text=page.get_text("text")
                )
            )

        pdf.close()

        return Paper(
            title=file_path.stem,
            pages=pages
        )