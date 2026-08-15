import json 
import os
import boto3
from flink_feature_engineering.config import AWS_REGION

from pyflink.datastream.functions import MapFunction

FRAUD_SQS = os.environ["FRAUD_SQS"]
NON_FRAUD_SQS = os.environ["NON_FRAUD_SQS"]
AWS_REGION = AWS_REGION

class SQSRouter(MapFunction):
    def open(self, runtime_context):
        self.sqs = boto3.client("sqs", region_name=AWS_REGION)
        print("SQS Router opened")

    def map(self, result):
        queue_url = (FRAUD_SQS if result["isFraud"] else NON_FRAUD_SQS)

        message = json.dumps(result)

        self.sqs.send_message(QueueUrl=queue_url, MessageBody=message)

        print(f"SQS -> "
            f"{'FRAUD' if result['isFraud'] else 'NON-FRAUD'} | "
            f"TXN={result['txn_id']} | "
            f"score={result['score']:.6f}"
        )

        return result

