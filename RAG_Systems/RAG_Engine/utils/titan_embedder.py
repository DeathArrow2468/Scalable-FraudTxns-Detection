import json
import time
import boto3
from botocore.exceptions import ClientError
from utils.bedrock_client import BedrockClient

class TitanEmbedder:
    MODEL_ID = "amazon.titan-embed-text-v2:0"

    def __init__(self, region="ap-south-1"):
        self.client = BedrockClient.get_client()
        
    def embed(self, text: str):
        body = {
            "inputText": text,
            "dimensions": 1024,
            "normalize": True
        }

        for attempt in range(3):
            try:
                reponse = self.client.invoke_model(
                    modelId=self.MODEL_ID,
                    body=json.dumps(body)
                )

                response_body = json.loads(reponse["body"].read())

                return response_body["embedding"]
            except ClientError:
                if attempt == 2:
                    raise

                time.sleep(2 ** attempt)

