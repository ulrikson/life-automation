import requests
from datetime import datetime, timedelta
from pytz import timezone


class Fantasy:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_next_deadline(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

        data = response.json()
        next_deadline = None

        for event in data["events"]:
            event_deadline = datetime.strptime(
                event["deadline_time"], "%Y-%m-%dT%H:%M:%S%z"
            )
            if event_deadline > datetime.now(event_deadline.tzinfo):
                next_deadline = event_deadline
                break

        if next_deadline is None:
            print("Error: Unable to find the next deadline.")
        else:
            stockholm_tz = timezone("Europe/Stockholm")
            next_deadline = next_deadline.astimezone(stockholm_tz)
            return next_deadline

    def is_deadline_today(self):
        deadline = self.get_next_deadline()
        if deadline is not None:
            stockholm_tz = timezone("Europe/Stockholm")
            current_date = datetime.now(stockholm_tz).date()

            if deadline.date() == current_date + timedelta(days=1):
                return True

        return False


if __name__ == "__main__":
    premier_league = Fantasy("https://fantasy.premierleague.com/api/bootstrap-static/")
    print(premier_league.get_next_deadline())
    print(premier_league.is_deadline_today())

    allsvenskan = Fantasy("https://fantasy.allsvenskan.se/api/bootstrap-static/")
    print(allsvenskan.get_next_deadline())
    print(allsvenskan.is_deadline_today())
