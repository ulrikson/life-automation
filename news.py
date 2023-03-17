import urllib.parse
import requests


class News:
    """Using the Omni API from https://omni-content.omni.news/ to get popular topics"""

    def __init__(self):
        pass

    def getPopularTopics(self):
        """Returns a string with the popular topics in markdown format"""

        url = "https://omni-content.omni.news/topics?offset=0&limit=5&sort=current"
        response = requests.get(url).json()
        text = self.getTopicsText(response["topics"])

        return text

    def getTopicsText(self, topics):
        """Converts a list of topics to a string in markdown format"""

        text = "## Popular topics 🗞\n"

        for topic in topics:
            title_encoded = urllib.parse.quote(topic["title"])
            url = "https://omni.se/sok?q=" + title_encoded + "&tab=articles"
            text += f"* [{topic['title']}]({url})\n"

        return text
