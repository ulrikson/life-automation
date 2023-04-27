import requests
from urllib.parse import quote


class NewsAPI:
    """Fetches popular topics from the Omni API."""

    BASE_URL = "https://omni-content.omni.news"

    def __init__(self, offset=0, limit=10, sort="current"):
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

    def get_topics_formatted(self):
        text = "## Popular topics 🗞\n"
        topics = self.get_popular_topics()

        for i, topic in enumerate(topics, start=1):
            title_encoded = quote(topic["title"])
            url = f"https://omni.se/sok?q={title_encoded}&tab=articles"
            text += f"{i}. [{topic['title']}]({url})\n"

        return text


if __name__ == "__main__":
    api = NewsAPI()
    text = api.get_topics_formatted()

    print(text)
