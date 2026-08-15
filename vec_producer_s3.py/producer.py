import json
import uuid
import time

import boto3
import pandas as pd

# ==========================
# CONFIG
# ==========================

BUCKET_NAME = "fraud-txns-detection"
CSV_KEY = "dataset/paysim_shuffled.csv"      # Change if stored inside a folder
LOCAL_FILE = "paysim_shuffled.csv"

STREAM_NAME = "fraud-txns"

ROWS_TO_SEND = 5
CHUNK_SIZE = 5          # rows read into memory at a time (t3.micro-safe)

# Delay between records (20 ms = 50 txn/sec)
DELAY = 0.02

# Only pull the columns we actually use — cuts memory further
USECOLS = [
    "step", "type", "amount",
    "nameOrig", "nameDest",
    "oldbalanceOrg", "newbalanceOrig",
    "oldbalanceDest", "newbalanceDest",
    "isFraud",
]

# ==========================

#s3 = boto3.client("s3", region_name="ap-south-1")
kinesis = boto3.client("kinesis", region_name="ap-south-1")

# print("Downloading dataset from S3...")
# s3.download_file(BUCKET_NAME, CSV_KEY, LOCAL_FILE)
# print("Download complete.\n")

print(f"Streaming up to {ROWS_TO_SEND} rows in chunks of {CHUNK_SIZE}...\n")

event_number = 0

# chunksize makes pandas read the file incrementally instead of loading
# the whole CSV into memory before we even get to .head()/slicing.
for chunk in pd.read_csv(LOCAL_FILE, usecols=USECOLS, chunksize=CHUNK_SIZE):

    if event_number >= ROWS_TO_SEND:
        break

    records = chunk.to_dict("records")

    for row in records:
        if event_number >= ROWS_TO_SEND:
            break

        event_number += 1

        txn = {
            "event_number": event_number,
            "step": int(row["step"]),
            "txn_id": str(uuid.uuid4()),

            "type": row["type"],
            "amount": float(row["amount"]),

            "nameOrig": row["nameOrig"],
            "nameDest": row["nameDest"],

            "oldbalanceOrg": float(row["oldbalanceOrg"]),
            "newbalanceOrig": float(row["newbalanceOrig"]),

            "oldbalanceDest": float(row["oldbalanceDest"]),
            "newbalanceDest": float(row["newbalanceDest"]),

            "timestamp": int(time.time() * 1000),

            "isFraud": int(row["isFraud"]),
        }

        success = False

        for attempt in range(3):
            try:
                kinesis.put_record(
                    StreamName=STREAM_NAME,
                    PartitionKey=txn["nameOrig"],
                    Data=json.dumps(txn),
                )

                if attempt > 0:
                    print(f"Transaction #{event_number} succeeded on retry {attempt + 1}")

                success = True
                break

            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(1)

        if not success:
            print(f"Skipping transaction #{event_number}")

        if event_number % 1000 == 0:
            print(f"Sent {event_number} records")

        # sleep on EVERY record, not just every 1000 (this was the bug before)
        time.sleep(DELAY)

    # free the chunk's memory explicitly before pulling the next one
    del chunk, records

print(f"\nFinished sending {event_number} records.")