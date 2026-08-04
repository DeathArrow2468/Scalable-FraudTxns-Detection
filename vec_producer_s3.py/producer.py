import json
import uuid
import time

import boto3
import pandas as pd

# ==========================
# CONFIG
# ==========================

BUCKET_NAME = "fraud-txns-detection"
CSV_KEY = "paysim_shuffled.csv"      # Change if stored inside a folder
LOCAL_FILE = "dataset/paysim_shuffled.csv"

STREAM_NAME = "fraud-txns"

ROWS_TO_SEND = 50000

# Delay between records (20 ms = 50 txn/sec)
DELAY = 0.02

# ==========================

s3 = boto3.client("s3", region_name='ap-south-1')
kinesis = boto3.client("kinesis", region_name='ap-south-1')


print("Downloading dataset from S3...")
s3.download_file(BUCKET_NAME, CSV_KEY, LOCAL_FILE)
print("Download complete.\n")

df = pd.read_csv(LOCAL_FILE).head(ROWS_TO_SEND)
records = df.to_dict("records")

print(f"Sending {len(df)} transactions...\n")

for event_number, row in enumerate(records, start=1):

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

        "isFraud": int(row["isFraud"])
    }

    success = False

    for attempt in range(3):
        try:
            kinesis.put_record(
                StreamName=STREAM_NAME,
                PartitionKey=txn["nameOrig"],
                Data=json.dumps(txn)
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

    time.sleep(DELAY)

print("\nFinished sending 50,000 records.")