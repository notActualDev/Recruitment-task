import os
import json
import requests
from Prompts.JsonRepairPrompt import PROMPT


class LlmJsonRepairService:

    def __init__(self):

        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise Exception("GROQ_API_KEY not configured")

        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def repair_json(self, corrupted_json: str):

        payload = {

            "model": "llama-3.1-8b-instant",

            "temperature": 0,

            "messages": [
                {
                    "role": "system",
                    "content": PROMPT
                },
                {
                    "role": "user",
                    "content": corrupted_json
                }
            ]

        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.post(
            self.url,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            raise Exception(f"Groq API error: {response.text}")

        data = response.json()

        if "choices" not in data:
            raise Exception(f"Unexpected Groq response: {data}")

        content = data["choices"][0]["message"]["content"]

        try:
            parsed = json.loads(content)
        except Exception:
            raise Exception(f"LLM returned invalid JSON: {content}")

        return parsed