from pathlib import Path
import json

from utils.logger import setup_logger

from utils.chunk_models import Chunk, ChunkMetadata, ChunkCollection

from utils.titan_embedder import TitanEmbedder
from utils.embeddings_writer import EmbeddingWriter

BASE_DIR = Path(__file__).resolve().parent
INPUT_FOLDER = BASE_DIR / "chunks"
OUTPUT_FOLDER = BASE_DIR / "embeddings"

logger = setup_logger()
embedder = TitanEmbedder()

def load_chunk_collection(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = []

    for chunk in data['chunks']:
        metadata = ChunkMetadata(**chunk["metadata"])
        chunks.append(
            Chunk(
                metadata=metadata,
                text=chunk["text"],
                embedding=chunk.get("embedding"),
                embedding_text=chunk.get("embedding_text")
            )
        )

    return ChunkCollection(document_uuid=data["document_uuid"], chunks=chunks)

def build_embedding_text(chunk: Chunk):

    return f"""
        Authority: {chunk.metadata.authority}

        Document: {chunk.metadata.document_title}

        Chapter:
        {chunk.metadata.chapter}
        {chunk.metadata.chapter_title}

        Section:
        {chunk.metadata.section}

        Heading:
        {chunk.metadata.heading}

        Content:

        {chunk.text}
        """.strip()

def process_document(file_path):
    logger.info(f"Embedding {file_path.name}")
    collection = load_chunk_collection(file_path)
    total = len(collection.chunks)

    for i, chunk in enumerate(collection.chunks, start=1):

        logger.info(f"Embedding Chunk {i}/{total}")

        chunk.embedding_text = build_embedding_text(chunk)

        chunk.embedding = embedder.embed(chunk.embedding_text)

    relative_parent = file_path.relative_to(INPUT_FOLDER).parent

    output_file = OUTPUT_FOLDER / relative_parent / file_path.name

    EmbeddingWriter.save(collection, output_file)

    logger.info(f"Saved embeddings -> {output_file}")


def main():
    processed = 0
    failed = 0

    logger.info("========== Embedding Started ==========")
    for file in INPUT_FOLDER.rglob("*.json"):

        try:

            process_document(file)

            processed += 1

        except Exception as e:

            failed += 1

            logger.exception(e)

    logger.info("========== Embedding Finished ==========")

    logger.info(f"Processed : {processed}")

    logger.info(f"Failed : {failed}")

if __name__ == "__main__":
    main()