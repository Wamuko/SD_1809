"""
植物とLine側の「電話交換手」の役割を果たします
また、そのほかのシステム的な機能を担います
"""
from datetime import datetime
import ResponseDict

from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)

from linebot import (
    LineBotApi,
    WebhookHandler,
)
import random


class PlantAnimator:
    def __init__(self, user_data, line_bot_api):
        self.user_data = user_data
        self.__line_bot_api = line_bot_api
        self.__plant = None
        self.tell_weather = False
        self.push_message = None
        self.__listen_beacon_datetime = None

    @property
    def plant(self):
        return self.__plant

    # 植物を生成し、接続します　memo: 引数にとりあえずdisplay_nameをいれておきます
    def register_plant(self, display_name):
        msg = []
        if self.connecting():
            msg.extend(self.disconnect())

        plant = self.__plant = self.user_data.add_plant(display_name)
        plant.push_message = self.push_message
        msg.append(plant.say_nice_to_meet_you())
        return msg

    # 植物を削除します
    def delete_plant(self, display_name):
        msg = []
        if self.connecting() and self.__plant.display_name == display_name:
            msg.extend(self.disconnect())

        self.user_data.remove_plant(display_name)
        return msg

    # 要求された名前から対応する植物を再生します
    def connect(self, name, event=None):
        new_plant = self.user_data.reanimate_plant(name)
        if new_plant is None:
            return "その名前の植物はいないよ"
        else:
            print("connect %s" % new_plant.display_name)
            new_plant.push_message = self.push_message
            self.__plant = new_plant
            return new_plant.say_hello()

    # 植物との接続を切断します
    def disconnect(self):
        if not self.connecting():
            return "誰ともお話ししてないよ"
        else:
            print("disconnect")
            pl = self.__plant
            self.__plant = None
            return pl.say_see_you()
            

    # 植物と接続しているか確認します
    def connecting(self):
        return self.__plant is not None

    # Clovaに呼ばれたときにランダムに接続を行う
    def clova_random_connect(self):
        return self.connect(random.choice(self.user_data.list_plant_name()))
        

    # Lineのテキストを植物に伝え、応答を受け取ります
    def communicate(self, text):
        if self.connecting():
            return self.__plant.chat(text)
        else:
            resp = ResponseDict.Instance
            if text in resp.WhoAreYou:
                return resp.IamWhisper
            else:
                return resp.NobodySpeaking

    # ユーザがビーコンの近くかつ、コンフィグ設定がOnの時に呼ばれます
    def listen_beacon(self, beacon_config):
        if beacon_config ==  1:
            self.__listen_beacon_datetime = datetime.now()

    # ユーザのビーコンが一度呼ばれたらそれから60分は呼ばれないようにするためのパーツ
    def listen_beacon_span(self):
        self.__listen_beacon_datetime is None or 3600 < (datetime.now() - self.__listen_beacon_datetime).total_seconds()
    
    # センサがエコモードになってから（listen_beaconが呼ばれてから）4時間たったかを確認
    def check_beacon_eco_time(self):
        return (datetime.now() - self.__listen_beacon_datetime).total_seconds() < 14401
        

    # 植物の状態の更新をします
    def update(self):
        if self.connecting():
            self.__plant.update()
        time = datetime.now()
        hour = time.hour
        second = time.second
        if hour == 0:
            self.tell_weather = False
        elif self.tell_weather and hour >= 6:
            self.__report_weather_forecast()
            self.tell_weather = True
        if second == 0:
            if self.connecting():
                self.__plant.set_beacon_buf_span(self.check_beacon_eco_time())

    def __report_weather_forecast(self):
        if self.connecting():
            ud = self.user_data
            self.__plant.report_weather_forecast(ud.postal_code)
