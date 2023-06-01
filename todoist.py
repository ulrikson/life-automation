import requests
from dotenv import load_dotenv
import os
import uuid
import json

load_dotenv()


class Todoist:
    def __init__(self) -> None:
        self.inbox_project_id = 2309764563
        self.home_project_id = 2309764566
        self.headers = self.get_headers()

    def get_tasks(self, params):
        """Get tasks from Todoist API
        See https://developer.todoist.com/rest/v2/#get-active-tasks
        :param params: dict
        :return: json
        """
        url = "https://api.todoist.com/rest/v2/tasks"

        response = requests.get(url, headers=self.headers, params=params)

        return response.json()

    def get_completion_tasks(self):
        """Get tasks from Todoist API that contain a question mark and has no description
        See https://developer.todoist.com/rest/v2/#get-active-tasks
        :return: json
        """
        params = {"filter": "#Inbox & search:?"}

        # extra safety layer, the API should return only inbox tasks with a question mark, but it's wonky
        tasks = []
        for task in self.get_tasks(params):
            # project is inbox
            is_inbox = int(task["project_id"]) == int(self.inbox_project_id)
            # description is empty
            is_empty = task["description"] == ""
            # question mark in content
            is_question = "?" in task["content"]

            if is_inbox and is_empty and is_question:
                tasks.append(task)

        return tasks

    def create_task(self, data):
        """Create task in Todoist API
        See https://developer.todoist.com/rest/v2/#create-a-new-task
        :param data: dict
        :return: bool
        """

        url = "https://api.todoist.com/rest/v2/tasks"

        response = requests.post(url, data=json.dumps(data), headers=self.headers)

        return True if response.status_code == 200 else False

    def update_task(self, data, task_id):
        """Update task in Todoist API
        See https://developer.todoist.com/rest/v2/#update-a-task
        :param data: dict
        :param task_id: int
        :return: bool
        """

        url = "https://api.todoist.com/rest/v2/tasks/" + str(task_id)

        response = requests.post(url, data=json.dumps(data), headers=self.headers)

        return True if response.status_code == 200 else False

    def get_headers(self):
        """Get headers for Todoist API"""

        return {
            "Content-Type": "application/json",
            "X-Request-Id": str(uuid.uuid4()),
            "Authorization": f"Bearer {os.getenv('TODOIST_TOKEN')}",
        }


if __name__ == "__main__":
    todoist = Todoist()
    tasks = todoist.get_completion_tasks()
    print(tasks)