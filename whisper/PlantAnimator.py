"""
植物とLine側の「電話交換手」の役割を果たします
また、そのほかのシステム的な機能を担います
"""
from datetime import datetime


class PlantAnimator:
    def __init__(self, user_data):
        self.user_data = user_data
        self.__plant = None
        self.tell_weather = False
        self.push_message = None

    @property
    def plant(self):
        return self.__plant

    # 植物を生成します　memo: 引数にとりあえずdisplay_nameをいれておきます
    def register_plant(self, display_name):
        pl = self.__plant = self.user_data.add_plant(display_name)
        pl.push_message = self.push_message

    def delete_plant(self, display_name):
        if self.__plant.display_name == display_name:
            self.disconnect()
        self.user_data.remove_plant(display_name)

    # 要求された名前から対応する植物を再生します
    def connect(self, name):
        self.__plant = plant = self.user_data.reanimate_plant(name)
        if plant is None:
            return "その名前の植物はいません"
        else:
            plant.push_message = self.push_message
            return name + ": なに？"

    # 植物との接続を切断します
    def disconnect(self):
        if self.__plant is None:
            return "植物が選択されてないよ"
        else:
            text = self.__plant.display_name + ": またね"
            self.__plant = None
            return text

    # 植物と接続しているか確認します
    def connecting(self):
        return self.__plant is None

    # Lineのテキストを植物に伝え、応答を受け取ります
    def communicate(self, text):
        if self.connecting():
            return self.__plant.chat(text)
        else:
            return None

    # ユーザがビーコンの近くにいたら呼ばれます
    def listen_beacon(self, now, beacon_config):
        self.__plant.listen_beacon = (now, beacon_config)

    # ユーザのビーコンが一度呼ばれたらそれから30分は呼ばれないようにするためのパーツ
    def listen_beacon_span(self, now):
        if self.__plant.listen_beacon[0] is None or (
                now - self.__plant.listen_beacon[0]) < 3600:
            return False
        else:
            return True

    # 植物の状態の更新をします
    def update(self):
        self.__plant.update()
        hour = datetime.now().hour
        if hour == 0:
            self.tell_weather = False
        elif self.tell_weather and hour >= 6:
            self.__report_weather_forecast()
            self.tell_weather = True

    def __report_weather_forecast(self):
        ud = self.user_data
        self.__plant.report_weather_forecast(ud.postal_code)
