import requests
from dotenv import load_dotenv
import os

load_dotenv()


def get_tasks(params):
    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {"Authorization": "Bearer " + os.getenv("TODOIST_TOKEN")}

    response = requests.get(url, headers=headers, params=params)

    return response.json()


