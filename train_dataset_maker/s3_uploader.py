import boto3

BUCKET_NAME = "fraud-txns-detection"
LOCAL_FILE = "training_vectors.jsonl"
S3_KEY = "train/training_vectors.jsonl"

client = boto3.client("s3")

def upload():
    client.upload_file(LOCAL_FILE, BUCKET_NAME, S3_KEY)
    print("S3 Upload success")
