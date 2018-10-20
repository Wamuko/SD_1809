# -*- coding: utf-8 -*-
from WeatherForecast import WeatherForecast

data = WeatherForecast.get_weather("980-0871")

print(WeatherForecast.calc_average(data))