import os
import json
import boto3

ssm = boto3.client("ssm")
apigw = boto3.client(
    "apigatewaymanagementapi",
    endpoint_url=os.environ["WEBSOCKET_ENDPOINT"]
)

PARAMETER_NAME = os.environ["CONNECTION_PARAMETER"]


def lambda_handler(event, context):

    print("FRAUD DELIVERY: Lambda started")

    # 1. Get current WebSocket connection
    print("STEP 1: Getting connection ID from SSM")

    response = ssm.get_parameter(
        Name=PARAMETER_NAME
    )

    connection_id = response["Parameter"]["Value"]

    print("STEP 2: Connection ID:", connection_id)

    # 2. Process SQS records
    for record in event["Records"]:

        message = json.loads(record["body"])

        print("STEP 3: SQS MESSAGE:", message)

        payload = {
            "type": "transaction",
            "isFraud": True,
            "data": message
        }

        # 3. Send to WebSocket
        print("STEP 4: Sending WebSocket message")

        apigw.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps(payload).encode("utf-8")
        )

        print("STEP 5: WebSocket message sent")

    return {
        "statusCode": 200
    }