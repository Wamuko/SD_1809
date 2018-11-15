import numpy as np
from WeatherForecast import WeatherForecast
from Plant import Plant
import random

def sample_one(*args):
    return random.sample(args, 1)[0]

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
            ret = "%s: "
            ret += sample_one(" ..?", "なに言っているの？", "よくわかんないや")
            return ret % plant.display_name

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
    def respond_health(plant : Plant):
        response_msg = ""
        plant.sense_condition()
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
        plant.sense_condition()
        response_msg = ""
        if plant.needWater():
            response_msg += sample_one("水が欲しいよ！", "うん！", "のどが渇いたな")
        else:
            response_msg += sample_one("もう十分だよ", "いらないよー", "大丈夫だよ、ありがとう")

        return response_msg

    @staticmethod
    def respond_light_demand(plant):
        response_msg = ""
        plant.sense_condition()
        if plant.needLuminesity():
            response_msg += sample_one("少し暗いかな", "明るいところに行きたいな", "光が欲しいよ")
        else:
            response_msg += sample_one("ちょうどいいよ！", "気持ちいいよ！", "十分だよ")

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
