import os
import openai
from dotenv import load_dotenv

load_dotenv()


class ChatGPT:
    def __init__(self):
        self.model = "gpt-4"
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def curious(self, message):
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are my curious assistant.",
                },
                {"role": "user", "content": message},
                {
                    "role": "assistant",
                    "content": "First, could you please answer my question? Second, always end with one related, relevant fact.",
                },
            ],
        )
        return completion.choices[0].message.content

    def summarize_news(self, news):
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "Du är min nyhetssammanfattare. Jag ger dig ett par aktuella ämnen och du sammanfattar dem åt mig.",
                },
                {"role": "user", "content": news},
                {"role": "assistant", "content": "Kan du sammanfatta dessa nyheter?"},
            ],
        )

        return completion.choices[0].message.content
