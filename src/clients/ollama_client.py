"""
Client responsible for communication
with the local Ollama server.
"""

import requests

from config import MODEL_NAME,MODEL_URL


class OllamaClient:

    def __init__(self):

        self.base_url = MODEL_URL

    def chat(self, messages):

        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "stream": False
            },
            timeout=120
        )

        if response.status_code != 200:
            print("Status:", response.status_code)
            print("Response:", response.text)
            raise Exception("Ollama request failed")

        return response.json()["message"]["content"]