"""
Retrieval Augmented Generation Engine.
"""

from clients.ollama_client import OllamaClient


class RAGEngine:

    def __init__(self):

        self.client = OllamaClient()

    def answer_question(
        self,
        question,
        context
    ):

        prompt = f"""
You are an IAM assistant.

Answer ONLY using the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        return self.client.chat(messages)