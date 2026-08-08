from utils.models import Page

class MarkdownExtractor:
    @staticmethod
    def extract(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        return [
            Page(
                page_number=1,
                text=text,
                char_count=len(text)
            )
        ]