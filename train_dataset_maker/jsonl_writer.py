import json
from dataclasses import asdict
from pathlib import Path


class JsonlWriter:

    def __init__(self, filename: str):
        self.file = Path(filename).open("w", encoding="utf-8")
        self.count = 0

        print(f"Opened JSONL file: {filename}")

    def write(self, feature_vector):

        print("JsonlWriter.write() called")

        data = asdict(feature_vector)

        json.dump(data, self.file)
        self.file.write("\n")

        # Flush EVERY write while debugging
        self.file.flush()

        self.count += 1

        print(f"Successfully wrote record #{self.count}")

    def close(self):
        print("Closing JSONL writer...")
        self.file.flush()
        self.file.close()