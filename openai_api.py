import os
import openai
from dotenv import load_dotenv

load_dotenv()


class ChatGPT:
    def __init__(self, model="gpt-3.5-turbo-16k"):
        """Initializes the ChatGPT model and loads the OPENAI_API_KEY."""
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("Missing OPENAI_API_KEY environment variable")
        openai.api_key = self.api_key

    def curious(self, message):
        """Generates a completion using the curious assistant mode."""
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=self._get_curious_messages(message),
        )
        return completion.choices[0].message.content

    def _get_curious_messages(self, message):
        """Constructs the messages for the curious assistant mode."""
        messages = [
            {
                "role": "system",
                "content": "You are my research assistant. I'll give you some questions and I want you to point me to what keywords to search on Wikipedia to answer the questions.",
            },
        ]

        messages.append({"role": "user", "content": message})
        messages.append(
            {
                "role": "assistant",
                "content": "Briefly answer the question and then tell me what keywords to search on Wikipedia to answer the question.",
            },
        )

        return messages

    def summarize_news(self, news):
        """Generates a completion using the news summarizer mode."""
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "Du är min nyhetssammanfattare. Varje morgon ger jag dig ett par aktuella ämnen och du sammanfattar dem åt mig. Målet är att jag ska få en så bra överblick som möjligt över vad som händer i världen just nu.",
                },
                {"role": "user", "content": news},
                {"role": "assistant", "content": "Kan du sammanfatta dessa nyheter?"},
            ],
        )

        return completion.choices[0].message.content


if __name__ == "__main__":
    chatgpt = ChatGPT()
    print(chatgpt.curious("Vad är en hund?"))
