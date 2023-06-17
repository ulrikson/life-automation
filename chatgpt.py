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
                    "content": "You are my curious assistant. You help me explore the world by answering my questions give me ideas for further research.",
                },
                {"role": "user", "content": message},
                {
                    "role": "assistant",
                    "content": "Could you please answer my question? Always end with ideas for further research.",
                },
            ],
        )
        return completion.choices[0].message.content
