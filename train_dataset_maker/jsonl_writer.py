import json
from dataclasses import asdict
from pathlib import Path

from train_dataset_maker.s3_uploader import upload


class JsonlWriter:

    def __init__(self, filename: str):
        self.file = Path(filename).open("w", encoding="utf-8")
        self.count = 0

    def write(self, feature_vector):

        json.dump(asdict(feature_vector), self.file)
        self.file.write("\n")

        self.count += 1

        # Upload every 1000 feature vectors
        if self.count % 1000 == 0:

            # Make sure everything is written to disk first
            self.file.flush()

            print(f"Generated {self.count} vectors. Uploading to S3...")

            try:
                upload()
                print("Upload Complete.")
            except Exception as e:
                print(f"S3 upload failed: {e}")

            print("Upload Complete. 2")

    def close(self):
        self.file.flush()
        self.file.close()