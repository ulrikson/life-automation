from todoist import Todoist
from weather import Weather
from news import News


class DailyBrief:
    def __init__(self) -> None:
        pass

    def create_brief(self):
        todoist = Todoist()
        weather = Weather().getForecastText()
        news = News().getPopularTopics()
        text = f"{news}\n{weather}"

        todoist.create_task(
            {
                "content": "Daily brief",
                "due_string": "today",
                "priority": 2,
                "description": text,
                "project_id": todoist.inbox_project_id,  # empty string for inbox
            }
        )

        print("Daily brief created")


DailyBrief().create_brief()