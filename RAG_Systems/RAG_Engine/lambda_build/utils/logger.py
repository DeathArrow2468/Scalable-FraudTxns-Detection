import logging
from pathlib import Path

def setup_logger():
    Path("logs").mkdir(exist_ok=True)
    logger = logging.getLogger("Retriever3")

    if logger.handlers: return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter( "%(asctime)s | %(levelname)s | %(message)s")

    file_handler = logging.FileHandler("logs/extraction.log")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger