"""
植物とLine側の「電話交換手」の役割を果たします
また、そのほかのシステム的な機能を担います
"""
from datetime import datetime

from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)

from linebot import (
    LineBotApi,
    WebhookHandler,
)


class PlantAnimator:
    def __init__(self, user_data, line_bot_api):
        self.user_data = user_data
        self.__line_bot_api = line_bot_api
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
    # 既に植物と接続している場合は接続を切ってから再生します
    def connect(self, name, event):
        new_plant = self.user_data.reanimate_plant(name)
        if new_plant is None:
            chat_text = "その名前の植物はいないよ"
            if chat_text is not None:
                self.__line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text=chat_text))
        else:
            if self.connecting():
                self.disconnect()
            new_plant.push_message = self.push_message
            self.__plant = new_plant
            chat_text = name + ": なに？"
            if chat_text is not None:
                self.__line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text=chat_text))

    # 植物との接続を切断します
    def disconnect(self, event=None):
        if not self.connecting() and event is not None:
            chat_text = "植物が選択されてないよ"
            if chat_text is not None:
                self.__line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text=chat_text))
        else:
            self.__plant = None
            if event is not None:
                chat_text = self.__plant.say_see_you()
                if chat_text is not None:
                    self.__line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text=chat_text))

    # 植物と接続しているか確認します
    def connecting(self):
        return self.__plant is not None

    # Lineのテキストを植物に伝え、応答を受け取ります
    def communicate(self, text, event):
        if self.connecting():
            chat_text = self.__plant.chat(text)
            if chat_text is not None:
                self.__line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text=chat_text))
        else:
            pass

    # ユーザがビーコンの近くにいたら呼ばれます
    def listen_beacon(self, now, beacon_config):
        self.__plant.listen_beacon = (now, beacon_config)

    # ユーザのビーコンが一度呼ばれたらそれから60分は呼ばれないようにするためのパーツ
    def listen_beacon_span(self, now):
        if self.__plant.listen_beacon[0] is None or (
                now - self.__plant.listen_beacon[0]) < 3600:
            return False
        else:
            return True

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
                self.__plant.set_beacon_buf_span()

    def __report_weather_forecast(self):
        if self.connecting():
            ud = self.user_data
            self.__plant.report_weather_forecast(ud.postal_code)
