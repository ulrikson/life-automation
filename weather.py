import requests
import os
from dotenv import load_dotenv

load_dotenv()


class Weather:
    """Using the Weather API from https://www.weatherapi.com/"""

    def __init__(self):
        self.url = "http://api.weatherapi.com/v1/forecast.json"
        self.city = "Stockholm"
        self.params = {"key": os.getenv("WEATHER_API_KEY"), "q": self.city, "days": 3}

    def getForecast(self):
        """Returns a list of dictionaries with the forecast for the next 3 days"""

        response = requests.get(self.url, headers={}, params=self.params).json()

        forecasts = []

        for forecast in response["forecast"]["forecastday"]:
            date = forecast["date"]
            avg_temp = forecast["day"]["avgtemp_c"]
            min_temp = forecast["day"]["mintemp_c"]
            max_temp = forecast["day"]["maxtemp_c"]
            condition = forecast["day"]["condition"]["text"]

            forecasts.append(
                {
                    "date": date,
                    "avg_temp": int(avg_temp),
                    "min_temp": int(min_temp),
                    "max_temp": int(max_temp),
                    "text": condition,
                }
            )

        return forecasts

    def getForecastText(self):
        """Returns a string with the forecast for the next 3 days in markdown format
        for example: * 2021-03-01: Partly cloudy, 3°C (1°C - 5°C)"""

        forecasts = self.getForecast()
        text = "## Weather forecast 🌦\n"
        for forecast in forecasts:
            text += f"* {forecast['date']}: {forecast['text']}, {forecast['avg_temp']}°C ({forecast['min_temp']}°C - {forecast['max_temp']}°C)\n"
        return text
