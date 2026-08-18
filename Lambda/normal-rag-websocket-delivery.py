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

    print("NORMAL DELIVERY: Lambda started")

    print("STEP 1: Getting connection ID from SSM")

    response = ssm.get_parameter(
        Name=PARAMETER_NAME
    )

    connection_id = response["Parameter"]["Value"]

    print("STEP 2: Connection ID:", connection_id)

    for record in event["Records"]:

        message = json.loads(record["body"])

        if isinstance(message, str):
            message = json.loads(message)

        print("STEP 3: SQS MESSAGE:", message)

        # If the SQS message is already wrapped, extract the actual transaction
        if (
            isinstance(message, dict)
            and message.get("type") == "transaction"
            and "data" in message
        ):
            transaction = message["data"]
        else:
            transaction = message

        payload = {
            "type": "transaction",
            "isFraud": False,
            "data": transaction
        }

        print("STEP 4: Sending WebSocket message")

        apigw.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps(payload).encode("utf-8")
        )

        print("STEP 5: WebSocket message sent")

    return {
        "statusCode": 200
    }