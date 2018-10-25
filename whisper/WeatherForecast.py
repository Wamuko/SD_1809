# -*- coding: utf-8 -*-
import json
import requests
from statistics import mean

API_KEY = "2f9611d9fe751ad5525f69daf6b3e43f"
API_URL = "http://api.openweathermap.org/data/2.5/forecast?zip={postal},JP&APPID={key}"
WEATHER_RATE = {
    "Clear": 5,
    "Clouds": 1,
    "Rain": -5,
    "Snow": -50,
    "Extreme": -100
}


class WeatherForecast:
    @staticmethod
    def get_weather(postal_code):
        url = API_URL.format(postal=postal_code, key=API_KEY)
        print(url)
        r = requests.get(url)
        data = json.loads(r.text)
        # 9:00 - 18:00のデータを取り出す
        usable_weather = {"weather": [], "detail": [], "wind": [], "time": []}
        for each_data in data["list"][:4]:
            usable_weather["weather"].append(
                WEATHER_RATE[each_data["weather"][0]["main"]])
            usable_weather["detail"].append(
                each_data["weather"][0]["description"])
            usable_weather["wind"].append(each_data["wind"]["speed"])
            usable_weather["time"].append(each_data["dt_txt"])
        return usable_weather

    @staticmethod
    def calc_average(weather_data):
        return {
            "weather": mean(weather_data["weather"]),
            #"detail": mean(weather_data["detail"]),
            "wind": mean(weather_data["wind"])
        }
