from pathlib import Path

from utils.logger import setup_logger
from utils.pdf_processor import PDFProcessor
from utils.prompt_builder import PromptBuilder
from utils.ollama_client import OllamaClient
from utils.markdown_writer import MarkdownWriter


BASE_DIR = Path(__file__).resolve().parent

RAW_FOLDER = BASE_DIR / "raw_papers"

OUTPUT_FOLDER = BASE_DIR / "markdown"

logger = setup_logger()

ollama = OllamaClient()


def process(file_path):

    logger.info(f"Processing {file_path.name}")

    paper = PDFProcessor.process(file_path)

    prompt = PromptBuilder.build(paper)

    markdown = ollama.generate(prompt)

    output = OUTPUT_FOLDER / f"{file_path.stem}.md"

    MarkdownWriter.save(
        markdown,
        output
    )

    logger.info(f"Saved {output}")


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