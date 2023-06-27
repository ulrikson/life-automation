import requests
from urllib.parse import quote
from openai_api import ChatGPT


class NewsAPI:
    """Fetches popular topics from the Omni API."""

    BASE_URL = "https://omni-content.omni.news"

    def __init__(self, offset=0, limit=5, sort="current"):
        self.offset = offset
        self.limit = limit
        self.sort = sort
        self.session = requests.Session()

    def get_popular_topics(self):
        """Returns a list of popular topics."""

        url = f"{self.BASE_URL}/topics?offset={self.offset}&limit={self.limit}&sort={self.sort}"
        response = self.session.get(url)

        if response.status_code != 200:
            response.raise_for_status()

        return response.json()["topics"]

    def get_news_text(self):
        text = "## News 🗞️\n"
        chat = ChatGPT()
        news = self.get_topics_text()
        text += chat.summarize_news(news)
        return text

    def get_topics_text(self):
        text = ""
        topics = self.get_popular_topics()

        for i, topic in enumerate(topics, start=1):
            title_encoded = quote(topic["title"])
            url = f"https://content.omni.se/search?query={title_encoded}&offset={self.offset}&limit={self.limit}&feature_flag=mer"
            response = self.session.get(url)

            if response.status_code != 200:
                response.raise_for_status()

            text += f"Ämne {i}: {self._get_article_text(response.json()['articles'])} \n\n"

        return text

    def _get_article_text(self, articles):
        text = ""
        for article in articles:
            for resource in article["resources"]:
                if resource["type"] == "Text":
                    for paragraph in resource["paragraphs"]:
                        text += paragraph["text"]["value"]

        return text


if __name__ == "__main__":
    api = NewsAPI()
    text = api.get_news_text()

    print(text)
