import os
import openai
from dotenv import load_dotenv

load_dotenv()


class ChatGPT:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key
    
    def chat(self, message):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return completion.choices[0].message