from SensorBuffer import SensorBuffer
from UserData import UserData
import random
"""
ユーザからの問いかけに対して返答のTextを返す
"""


class Response:
    user_requests = ["調子はどう？", "水はいる？", "日当たりはどう？", "気温はどう？"]
    waterThreshold = 60
    luminesityThreshold = 900
    tempertureMinRelax = 15
    tempertureMaxRelax = 30

    def __init__(self,
                 sensor_buffer,
                 name="",
                 responce_ai,
                 waterThreshold=waterThreshold,
                 luminesityThreshold=luminesityThreshold,
                 tempertureMinRelax=tempertureMinRelax,
                 tempertureMaxRelax=tempertureMaxRelax):
        self.__sensorBuf = sensor_buffer
        self.responce_ai = responce_ai
        self.name = name
        self.__water_threshold = waterThreshold
        self.__luminosity_threshold = luminesityThreshold
        self.__tempertureMinRelax = tempertureMinRelax
        self.__tempertureMaxRelax = tempertureMaxRelax

    # 名前の設定に使用します
    def get_current_name(self, name):
        self.name = name

    # ユーザからの返答に植物からの返答を記載　return: text
    def response(self, message):
        return self.responce_ai[message]

        response_msg = ""
        if message == self.user_requests[0]:
            if self.needWater():
                response_msg += "水が欲しいよ！"
            if self.needLuminesity():
                response_msg += "光が欲しいよ"
            else:
                response_msg += "元気だよ！"
                if random.randrange(10) < 2:
                    response_msg += "\nいつもありがとう(^^)"
        elif message == self.user_requests[1]:
            if self.needWater():
                response_msg += "水が欲しいよ！"
            else:
                response_msg += "もう十分だよ"
        elif message == self.user_requests[2]:
            if self.needLuminesity():
                response_msg += "少し暗いかな"
            else:
                response_msg += "ちょうどいいよ！"
        elif message == self.user_requests[3]:
            temp = self.getTemperture()
            if temp == 0:
                response_msg += "今日は寒すぎるよ"
            elif temp == 1:
                response_msg += "今日はきもちいいね！"
            elif temp == 2:
                response_msg += "今日は暑いね"

        return response_msg

    # 水は必要か否か return: bool
    def needWater(self):
        if self.waterThreshold <= self.__sensorBuf.get_humidity():
            return True
        else:
            return False

    # 光が欲しいか否か return: bool
    def needLuminesity(self):
        if self.luminesityThreshold <= self.__sensorBuf.get_humidity():
            return True
        else:
            return False

    # 気温の状況を返す return: int. 0: 寒い, 1: 適温, 2: 暑い
    def getTemperture(self):
        temp = self.__sensorBuf.get_temperture()
        if temp < self.__tempertureMinRelax:
            return 0
        elif self.__tempertureMinRelax <= temp and temp <= self.__tempertureMaxRelax:
            return 1
        else:
            return 2

    def respond_health(self):
        response_msg = ""
        need_water = self.needWater()
        need_light = self.needLuminesity()
        if need_water:
            response_msg += "水が欲しいよ！"

        if need_light:
            response_msg += "光が欲しいよ"

        if not need_light and not need_water:
            response_msg += "元気だよ！"
            if random.randrange(10) < 2:
                response_msg += "\nいつもありがとう(^^)"

        return response_msg

    def respond_water_demand(self):
        responce_msg = ""
        if self.needWater():
            response_msg += "水が欲しいよ！"
        else:
            response_msg += "もう十分だよ"

        return responce_msg

    def respond_light_demand(self):
        response_msg = ""
        if self.needLuminesity():
            response_msg += "少し暗いかな"
        else:
            response_msg += "ちょうどいいよ！"

        return response_msg

    def respond_temperture(self):
        response_msg = ""
        temp = self.getTemperture()
        if temp == 0:
            response_msg += "今日は寒すぎるよ"
        elif temp == 1:
            response_msg += "今日はきもちいいね！"
        elif temp == 2:
            response_msg += "今日は暑いね"

        return response_msg
