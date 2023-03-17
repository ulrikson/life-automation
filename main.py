from todoist import Todoist
from weather import Weather

todoist = Todoist()
weather = Weather()

# Creating a daily briefing task in Todoist
weather = weather.getForecastText()
Todoist().create_task(
    {
        "content": "Daily briefing",
        "due_string": "today",
        "priority": 2,
        "description": weather,
        "project_id": todoist.inbox_project_id,
    }
)
