import os
import openai
from dotenv import load_dotenv

load_dotenv()


class ChatGPT:
    def __init__(self):
        """Initializes the ChatGPT model and loads the OPENAI_API_KEY."""
        self.model = "gpt-4"
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
                "content": "You are my curious assistant. You help me explore the world by answering my questions give me ideas for further research.",
            },
        ]

        if context:
            messages.append({"role": "user", "content": f"You've previously told me: {context}"})
            messages.append({"role": "user", "content": f"I want to follow up on that by asking: {message}"})
        else:
            messages.append({"role": "user", "content": message})

        messages.append(
            {
                "role": "assistant",
                "content": "Could you please answer my question? Always end with one (1) idea for further research.",
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
                    "content": "Du är min nyhetssammanfattare. Jag ger dig ett par aktuella ämnen och du sammanfattar dem åt mig.",
                },
                {"role": "user", "content": news},
                {
                    "role": "assistant",
                    "content": "Kan du sammanfatta nyheterna till en gemensam text? Dela inte upp i flera ämnen.",
                },
            ],
        )

        return completion.choices[0].message.content


if __name__ == "__main__":
    chatgpt = ChatGPT()
    print(chatgpt.curious("How are you?", "I'm not fine."))
