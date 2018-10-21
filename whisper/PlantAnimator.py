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

    # 植物を生成します　memo: 引数にとりあえずdisplay_nameをいれておきます
    def register_plant(self, display_name):
        self.__plant = self.user_data.add_plant(display_name)

    def delete_plant(self, display_name):
        if self.__plant.display_name == display_name:
            self.disconnect()
        self.user_data.remove_plant(display_name)

    # 要求された名前から対応する植物を再生します
    def connect(self, name):
        self.__plant = self.user_data.reanimate_plant(name)

    # 植物との接続を切断します
    def disconnect(self):
        text = self.__plant.display_name + ": またね"
        self.__plant = None
        return text

    # 植物と接続しているか確認します
    def connecting(self):
        return self.__plant is None

    # Lineのテキストを植物に伝え、応答を受け取ります
    def communicate(self, text):
        return self.__plant.chat(text)

    # ユーザがビーコンの近くにいたら呼ばれます
    def listen_beacon(self, now, beacon_config):
        self.__plant.listen_beacon = (now, beacon_config)

    # ユーザのビーコンが一度呼ばれたらそれから30分は呼ばれないようにするためのパーツ
    def listen_beacon_span(self, now):
        if self.__plant.listen_bieacon[0] is None or (
                now - self.__plant.listen_bieacon[0]) < 3600:
            return False
        else:
            return True

    # 植物の状態の更新をします
    def update(self):
        feedback = self.__plant.update()
        if datetime.now().hour == 0:
            self.tell_weather = False
        elif self.tell_weather and datetime.now().hour >= 6:
            feedback = self.__report_weather_forecast()
            self.tell_weather = True
        return feedback

    def __report_weather_forecast(self):
        ud = self.user_data
        return self.__plant.report_weather_forecast(ud.postal_code)
