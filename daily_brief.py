from todoist import Todoist
from weather import Weather
from news import NewsAPI
from stocks import StockPrice


class DailyBrief:
    def __init__(self) -> None:
        pass

    def create_brief(self):
        """Create a daily brief in Todoist"""

        weather = Weather().get_forecast_text()
        news = NewsAPI().get_news_text()
        omx = StockPrice("^OMX").get_change_formatted()
        text = f"{news}\n{weather}\n{omx}"

        todoist = Todoist()
        todoist.create_task(
            {
                "content": "Daily brief",
                "due_string": "today",
                "priority": 2,
                "description": text,
                "project_id": todoist.inbox_project_id,
            }
        )

        todoist.create_deadline_tasks()

        print("Daily brief created")


DailyBrief().create_brief()
