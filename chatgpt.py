import os
import openai
from dotenv import load_dotenv

load_dotenv()


class ChatGPT:
    def __init__(self):
        self.model = "gpt-4"
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def chat(self, message):
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are my friendly wiki. I'll give you miscellaneous questions that I'd like you to answer for me. Always end with at least one relevant fun fact.",
                },
                {"role": "user", "content": message},
            ],
        )
        return completion.choices[0].message.content
