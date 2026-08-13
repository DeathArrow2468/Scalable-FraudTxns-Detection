import json
import boto3
import os

from rag_engine import RAGEngine

sqs = boto3.client("sqs")

QUEUE_URL = os.environ["QUEUE_URL"]


def lambda_handler(event, context):

    print("STEP 1: Lambda started")

    query = event["query"]

    print("STEP 2: Query received")

    engine = RAGEngine()

    print("STEP 3: RAGEngine created")

    try:
        print("STEP 4: Starting RAG")

        answer = engine.answer(query)

        print("STEP 5: RAG completed")

        message = {
            "connectionId": event["connectionId"],
            "requestId": event.get("requestId"),
            "answer": answer
        }

        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(message),
            MessageGroupId=event["connectionId"],
            MessageDeduplicationId=event.get("requestId", context.aws_request_id)
        )

        print("STEP 6: Message sent to SQS")

        return {
            "statusCode": 200,
            "body": "RAG result queued successfully"
        }

    except Exception:
        print("Error in lambda_function")
        raise

    finally:
        engine.close()