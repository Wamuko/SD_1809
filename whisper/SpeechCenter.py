from numpy import random
import WeatherForecast


class SpeechCenter:
    def make_response(self, plant):
        raise NotImplementedError()


class ExampleResponce(SpeechCenter):
    def __init__(self):
        klass = ExampleResponce
        self.examples = {
            "調子はどう？": klass.respond_health,
            "水はいる？": klass.respond_water_demand,
            "日当たりはどう？": klass.respond_light_demand,
            "気温はどう？": klass.respond_temperture
        }

    # 植物の状態に応じたテキストを生成します
    # TODO: ユーザーテキストが無い時のテキスト生成
    def make_response(self, plant, user_text=None):
        if user_text is None:
            return ""
        else:
            return self.examples[user_text](plant)

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
            if random.randrange(10) < 2:
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
