import json
from dataclasses import asdict
from pathlib import Path

class JSONWriter:
    @staticmethod
    def save(document, output_path: Path):
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(
                asdict(document),
                f,
                indent=4,
                ensure_ascii=False
            )