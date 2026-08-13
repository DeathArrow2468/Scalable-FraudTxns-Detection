import boto3
from config import AWS_REGION, LLM_MODEL_ID

class BedrockLLM:
    def __init__(self):
        self.client = boto3.client("bedrock-runtime", region_name=AWS_REGION)

    def generate(self, prompt):
        response = self.client.converse(
                modelId = LLM_MODEL_ID,
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
        )

        return response["output"]["message"]["content"][0]["text"]