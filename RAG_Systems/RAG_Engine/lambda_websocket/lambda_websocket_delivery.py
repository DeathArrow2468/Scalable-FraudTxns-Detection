import json
import boto3
import os


def lambda_handler(event, context):

    endpoint = os.environ["WEBSOCKET_ENDPOINT"]

    client = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url=endpoint
    )

    for record in event["Records"]:

        message = json.loads(record["body"])

        connection_id = message["connectionId"]
        answer = message["answer"]

        client.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps({
                "type": "rag_response",
                "answer": answer
            }).encode("utf-8")
        )

    return {
        "statusCode": 200
    }