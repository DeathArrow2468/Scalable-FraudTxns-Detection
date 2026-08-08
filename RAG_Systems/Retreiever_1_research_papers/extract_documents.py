from pathlib import Path

from utils.logger import setup_logger
from utils.models import Document, DocumentMetadata
from utils.metadata import build_metadata
from utils.pdf_extractor import PDFExtractor
from utils.markdown_extractor import MarkdownExtractor
from utils.json_writer import JSONWriter

RAW_FOLDER = Path("markdown")
OUTPUT_FOLDER = Path("extracted")

logger = setup_logger()

def process_document(file_path):
    logger.info(f"Processing {file_path.name}")

    if file_path.suffix.lower() == ".pdf": 
        pages = PDFExtractor.extract(file_path)

    elif file_path.suffix.lower() == ".md":
        pages = MarkdownExtractor.extract(file_path)

    else:
        logger.warning(f"Skipping unsupported file {file_path}")
        return

    meta = build_metadata(file_path, len(pages))
    metadata = DocumentMetadata(**meta)

    document = Document(
        metadata=metadata,
        pages=pages
    )

    output = OUTPUT_FOLDER / file_path.relative_to(RAW_FOLDER).parent / f"{file_path.stem}.json"
    JSONWriter.save(document, output)

    logger.info(f"Saved {output}")

def main():
    for file in RAW_FOLDER.rglob("*"):
        if file.suffix.lower() not in [".pdf", ".md"]: continue

        try:
            process_document(file)

        except Exception as e:
            logger.exception(f"Failed {file}: {e}")


if __name__ == "__main__":
    main()

