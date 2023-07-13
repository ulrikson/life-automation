import os
import openai
from dotenv import load_dotenv

load_dotenv()


class ChatGPT:
    def __init__(self):
        self.model = "gpt-4"
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def curious(self, message, context=None):
        messages = [
            {
                "role": "system",
                "content": "You are my curious assistant. You help me explore the world by answering my questions give me ideas for further research.",
            },
        ]

        if context:
            messages.append({"role": "user", "content": "You've previously told me: " + context})
            messages.append({"role": "user", "content": "I want to follow up on that by asking: " + message})
        else:
            messages.append({"role": "user", "content": message})

        messages.append(
            {
                "role": "assistant",
                "content": "Could you please answer my question? Always end with one (1) idea for further research.",
            },
        )

        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
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
