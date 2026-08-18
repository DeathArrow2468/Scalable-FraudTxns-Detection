import os
import boto3

ssm = boto3.client("ssm")

PARAMETER_NAME = os.environ["CONNECTION_PARAMETER"]


def lambda_handler(event, context):

    print("EVENT:", event)

    route = event["requestContext"]["routeKey"]
    connection_id = event["requestContext"]["connectionId"]

    if route == "$connect":

        ssm.put_parameter(
            Name=PARAMETER_NAME,
            Value=connection_id,
            Type="String",
            Overwrite=True
        )

        print("WEBSOCKET CONNECTED:", connection_id)

    elif route == "$disconnect":

        try:
            ssm.delete_parameter(
                Name=PARAMETER_NAME
            )

            print("WEBSOCKET DISCONNECTED:", connection_id)

        except ssm.exceptions.ParameterNotFound:
            pass

    return {
        "statusCode": 200
    }