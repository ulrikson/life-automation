import requests
import os
from dotenv import load_dotenv

load_dotenv()


class Weather:
    def __init__(self):
        self.url = "http://api.weatherapi.com/v1/forecast.json"
        self.city = "Stockholm"
        self.params = {"key": os.getenv("WEATHER_API_KEY"), "q": self.city, "days": 3}

    def getForecast(self):
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
                    "avg_temp": avg_temp,
                    "min_temp": min_temp,
                    "max_temp": max_temp,
                    "text": condition,
                }
            )

        return forecasts

    def getForecastText(self):
        forecasts = self.getForecast()
        forecast_text = ""
        for forecast in forecasts:
            forecast_text += f"{forecast['date']}: {forecast['text']}, {forecast['avg_temp']}°C, {forecast['min_temp']}°C - {forecast['max_temp']}°C\n"
        return forecast_text
