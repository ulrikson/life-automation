import requests
from dotenv import load_dotenv
import os
import uuid
import json
from fantasy import Fantasy

load_dotenv()


class Todoist:
    def __init__(self) -> None:
        self.inbox_project_id = 2309764563
        self.home_project_id = 2309764566
        self.headers = self.get_headers()

    def get_task(self, task_id):
        """Get task from Todoist API
        See https://developer.todoist.com/rest/v2/#get-a-task
        :param task_id: int
        :return: json
        """
        url = "https://api.todoist.com/rest/v2/tasks/" + str(task_id)

        response = requests.get(url, headers=self.headers)

        return response.json()

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

    def create_deadline_tasks(self):
        """Create deadline tasks in Todoist for Premier League and Allsvenskan"""

        self._create_league_task(
            "Premier League",
            "https://fantasy.premierleague.com/api/bootstrap-static/",
            "FPL Deadline",
            "https://fantasy.premierleague.com/the-scout/"
        )

        self._create_league_task(
            "Allsvenskan",
            "https://fantasy.allsvenskan.se/api/bootstrap-static/",
            "FAL Deadline",
            "https://www.fotbollskanalen.se/allsvenskan/?tab=nyheter"
        )

    def _create_league_task(self, league_name, api_url, title, description):
        """Create a deadline task in Todoist for a specific league
        :param league_name: Name of the league
        :param api_url: API URL for the league
        :param title: Content of the task
        :param description: Description of the task"""

        league = Fantasy(api_url)

        if league.is_deadline_today():
            deadline = league.get_next_deadline()
            todoist = Todoist()
            todoist.create_task(
                {
                    "content": title,
                    "description": description,
                    "due_string": deadline.strftime("%Y-%m-%d %H:%M"),
                    "priority": 4,
                    "project_id": todoist.home_project_id,
                }
            )

            print(f"{league_name} deadline task created")


if __name__ == "__main__":
    todoist = Todoist()
    tasks = todoist.get_completion_tasks()
    print(tasks)
