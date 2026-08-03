import json
from dataclasses import asdict
from pathlib import Path

class JsonlWriter:
    def __init__(self, filename: str):
        self.file = Path(filename).open("w", encoding="utf-8")
        self.count = 0

    def write(self, feature_vector):
        json.dump(asdict(feature_vector), self.file)
        self.file.write("\n")

        self.count += 1

        if self.count % 1000 == 0:  # Write features after every 1000 features
            self.file.flush()

    def close(self):
        self.file.flush()
        self.file.close()