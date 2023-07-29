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

    def curious(self, message, context=None):
        """Generates a completion using the curious assistant mode."""
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=self._get_curious_messages(message, context),
        )
        return completion.choices[0].message.content

    def _get_curious_messages(self, message, context=None):
        """Constructs the messages for the curious assistant mode."""
        messages = [
            {
                "role": "system",
                "content": "You are my curious assistant.",
            },
        ]

        if context:
            messages.append(
                {"role": "user", "content": f"You've previously told me: {context}"}
            )
            messages.append(
                {
                    "role": "user",
                    "content": f"I want to follow up on that by asking: {message}",
                }
            )
        else:
            messages.append({"role": "user", "content": message})

        messages.append(
            {
                "role": "assistant",
                "content": "First, could you please answer my question? Second, always end with one (1) relevant idea or fact.",
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
