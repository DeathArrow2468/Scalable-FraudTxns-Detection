from pathlib import Path

from utils.logger import setup_logger
from utils.pdf_processor import PDFProcessor
from utils.prompt_builder import PromptBuilder
from utils.ollama_client import OllamaClient
from utils.markdown_writer import MarkdownWriter
PAGES_PER_BATCH = 8

BASE_DIR = Path(__file__).resolve().parent

RAW_FOLDER = BASE_DIR / "raw_papers"

OUTPUT_FOLDER = BASE_DIR / "markdown"

logger = setup_logger()

ollama = OllamaClient()


def process(file_path):

    logger.info(f"Processing {file_path.name}")

    paper = PDFProcessor.process(file_path)

    batches = batch_pages(paper.pages)

    logger.info(f"{len(batches)} batches created")

    intermediate_markdowns = []

    for i, batch in enumerate(batches, start=1):

        logger.info(
            f"Processing batch {i}/{len(batches)}"
        )

        prompt = PromptBuilder.build_chunk(batch)

        markdown = ollama.generate(prompt)

        intermediate_markdowns.append(markdown)

    logger.info("Merging markdowns")

    merge_prompt = PromptBuilder.build_merge(
        intermediate_markdowns
    )

    final_markdown = ollama.generate(
        merge_prompt
    )

    output = OUTPUT_FOLDER / f"{file_path.stem}.md"

    MarkdownWriter.save(
        final_markdown,
        output
    )

    logger.info(f"Saved {output}")

def batch_pages(pages):

    batches = []

    for i in range(0, len(pages), PAGES_PER_BATCH):

        batches.append(
            pages[i:i + PAGES_PER_BATCH]
        )

    return batches

def main():

    processed = 0

    failed = 0

    for file in RAW_FOLDER.glob("*.pdf"):

        try:

            process(file)

            processed += 1

        except Exception as e:

            failed += 1

            logger.exception(e)

    logger.info(f"Processed : {processed}")

    logger.info(f"Failed : {failed}")


if __name__ == "__main__":

    main()