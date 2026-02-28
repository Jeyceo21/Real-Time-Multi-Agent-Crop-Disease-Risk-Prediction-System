import requests
import os

def get_weather_forecast(lat, lon):
    url = (
        "https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid=6fe883b06b738d45a35f744cb8d1234f&units=metric"
    )

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }