import json
from dataclasses import asdict
from pathlib import Path

from utils.chunk_models import ChunkCollection

class EmbeddingWriter:
    @staticmethod
    def save(collection: ChunkCollection, output_path: Path):
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(asdict(collection), f, indent=4, ensure_ascii=False)