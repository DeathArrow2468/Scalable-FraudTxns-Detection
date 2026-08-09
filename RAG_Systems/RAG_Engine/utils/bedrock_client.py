import boto3
from config import AWS_REGION

class BedrockClient:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = boto3.client("bedrock-runtime", region_name=AWS_REGION)

        return cls._client
    


    