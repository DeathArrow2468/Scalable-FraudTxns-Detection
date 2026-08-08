from pathlib import Path
import json

from utils.logger import setup_logger
from utils.models import Document, DocumentMetadata, Page
from utils.chunker import Chunker
from utils.chunk_writer import ChunkWriter


BASE_DIR = Path(__file__).resolve().parent
INPUT_FOLDER = BASE_DIR / "extracted"
OUTPUT_FOLDER = BASE_DIR / "chunks"

logger = setup_logger()

def load_document(file_path: Path) -> Document:
    """
    Load an extracted document JSON into a Document dataclass.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    metadata = DocumentMetadata(**data["metadata"])

    pages = [Page(**page)for page in data["pages"]]

    return Document(metadata=metadata, pages=pages)


def process_document(file_path: Path):

    logger.info(f"Processing {file_path.name}")

    document = load_document(file_path)

    chunk_collection = Chunker.chunk(document)

    relative_parent = file_path.relative_to(INPUT_FOLDER).parent

    output_file = (OUTPUT_FOLDER / relative_parent / file_path.name)

    ChunkWriter.save(chunk_collection, output_file)

    logger.info(
        f"Saved {len(chunk_collection.chunks)} chunks -> {output_file}"
    )


def main():
    logger.info("========== Chunking Started ==========")

    processed = 0
    failed = 0
    for file in INPUT_FOLDER.rglob("*.json"):
        try:
            process_document(file)
            processed += 1

        except Exception as e:
            failed += 1
            logger.exception(f"Failed {file}: {e}")

    logger.info("========== Chunking Finished ==========")
    logger.info(f"Processed : {processed}")
    logger.info(f"Failed    : {failed}")

if __name__ == "__main__":
    main()