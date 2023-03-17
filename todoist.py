import requests
from dotenv import load_dotenv
import os
import uuid
import json

load_dotenv()

INBOX_PROJECT_ID = 2309764563


def get_tasks(params):
    """Get tasks from Todoist API
    See https://developer.todoist.com/rest/v2/#get-active-tasks
    :param params: dict
    :return: json
    """
    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {"Authorization": f"Bearer {os.getenv('TODOIST_TOKEN')}"}

    response = requests.get(url, headers=headers, params=params)

    return response.json()


def create_task(data):
    """Create task in Todoist API
    See https://developer.todoist.com/rest/v2/#create-a-new-task
    :param data: dict
    :return: bool
    """

    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {
        "Content-Type": "application/json",
        "X-Request-Id": str(uuid.uuid4()),
        "Authorization": f"Bearer {os.getenv('TODOIST_TOKEN')}",
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    return True
