import numpy as np
from WeatherForecast import WeatherForecast
from Plant import Plant


class SpeechCenter:
    def make_response(self, plant):
        raise NotImplementedError()


class ExampleResponce(SpeechCenter):
    def __init__(self):
        self.examples = {}

    # 植物の状態に応じたテキストを生成します
    # TODO: ユーザーテキストが無い時のテキスト生成
    def make_response(self, plant, user_text=None):
        if user_text is None:
            return ""
        elif user_text in self.examples:
            return self.examples[user_text](plant)
        else:
            return "%s: ..?" % plant.display_name

    def report_weather_forecast(self, postal_code):
        weather = WeatherForecast.get_weather(postal_code)
        if WeatherForecast.calc_average(weather) > 0:
            return "今日は天気がいいから外に出して"
        else:
            return "今日はあまり天気が良くないね"

    def say_nice_to_meet_you(self, plant: Plant):
        return "%s: はじめまして!" % plant.display_name

    def say_hello(self, plant: Plant):
        return "%s: なに？" % plant.display_name

    def respond_see_you(self, plant: Plant):
        return "%s: またね" % plant.display_name

    @staticmethod
    def respond_health(plant):
        response_msg = ""
        need_water = plant.needWater()
        need_light = plant.needLuminesity()
        if need_water:
            response_msg += "水が欲しいよ！"

        if need_light:
            response_msg += "光が欲しいよ"

        if not need_light and not need_water:
            response_msg += "元気だよ！"
            if np.random.randint(0, 10) < 2:
                response_msg += "\nいつもありがとう(^^)"

        return response_msg

    @staticmethod
    def respond_water_demand(plant):
        response_msg = ""
        if plant.needWater():
            response_msg += "水が欲しいよ！"
        else:
            response_msg += "もう十分だよ"

        return response_msg

    @staticmethod
    def respond_light_demand(plant):
        response_msg = ""
        if plant.needLuminesity():
            response_msg += "少し暗いかな"
        else:
            response_msg += "ちょうどいいよ！"

        return response_msg

    @staticmethod
    def respond_temperture(plant):
        response_msg = ""
        temp = plant.getTemperture()
        if temp == 0:
            response_msg += "今日は寒すぎるよ"
        elif temp == 1:
            response_msg += "今日はきもちいいね！"
        elif temp == 2:
            response_msg += "今日は暑いね"

        return response_msg
