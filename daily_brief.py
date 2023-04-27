from todoist import Todoist
from weather import Weather
from news import NewsAPI, NewsMarkdownFormatter
from fantasy import Fantasy


class DailyBrief:
    def __init__(self) -> None:
        pass

    def create_brief(self):
        """Create a daily brief in Todoist"""

        todoist = Todoist()
        weather = Weather().get_forecast_text()
        news = NewsMarkdownFormatter().format(NewsAPI().get_popular_topics())
        text = f"{news}\n{weather}"

        todoist.create_task(
            {
                "content": "Daily brief",
                "due_string": "today",
                "priority": 2,
                "description": text,
                "project_id": todoist.inbox_project_id,
            }
        )

        print("Daily brief created")

    def create_deadline_tasks(self):
        """Create deadline tasks in Todoist for Premier League and Allsvenskan"""

        self._create_deadline_task(
            "Premier League",
            "https://fantasy.premierleague.com/api/bootstrap-static/",
            "FPL Deadline",
        )

        self._create_deadline_task(
            "Allsvenskan",
            "https://fantasy.allsvenskan.se/api/bootstrap-static/",
            "FAL Deadline",
        )

    def _create_deadline_task(self, league_name, api_url, task_content):
        """Create a deadline task in Todoist for a specific league
        :param league_name: Name of the league
        :param api_url: API URL for the league
        :param task_content: Content of the task"""

        league = Fantasy(api_url)

        if league.is_deadline_today():
            deadline = league.get_next_deadline()
            todoist = Todoist()
            todoist.create_task(
                {
                    "content": task_content,
                    "due_string": deadline.strftime("%Y-%m-%d %H:%M"),
                    "priority": 4,
                    "project_id": todoist.home_project_id,
                }
            )

            print(f"{league_name} deadline task created")


DailyBrief().create_brief()
DailyBrief().create_deadline_tasks()
