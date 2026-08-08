import requests


class OllamaClient:

    def __init__(self):

        self.url = "http://localhost:11434/api/generate"

        self.model = "qwen3:14b"

    def generate(self, prompt):

        response = requests.post(

            self.url,

            json={

                "model": self.model,

                "prompt": prompt,

                "stream": False

            }

        )

        response.raise_for_status()

        return response.json()["response"]