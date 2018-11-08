from UserData import UserData

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    PostbackAction,
)

from linebot import (
    LineBotApi, WebhookHandler
)

"""
Line beaconについての設定やコンフィグはこちらでやっています
user_data.json_data['user_line_beacon'] {0 : 未設定, 1 : On, 2: Off}
"""
class BeaconWhisperEvent:

    def __init__(
            self,
            line_bot_api,
            userData):
        self.__user_data = userData
        self.__line_bot_api = line_bot_api

    def activation_msg(self, event):
        # Lineビーコンが接続された場合、もし0:未設定なら設定プロセスに移行する
        if self.__user_data.json_data['use_line_beacon'] is 0:
            confirm_template = ConfirmTemplate(text="LINE beacon が接続されたようです。Beacon Ecoを使用しますか？\nこれを用いることでスマホがビーコンから遠くにあるときはセンサを省エネ化し、センサ寿命を延ばすことができます。\nbeacon と話しかけると設定を変更できます。", actions=[
                PostbackAction(label='はい', data='set_beacon_on', displayText='はい！'),
                PostbackAction(label='いいえ', data='set_beacon_off', displayText='いいえ'),
            ])
            template_message = TemplateSendMessage(
                alt_text='Confirm alt text', template=confirm_template)
            self.__line_bot_api.reply_message(event.reply_token, template_message)


    def set_beacon(self, event):
        # ビーコンのOnとOffを変更する
        react = event.postback.data
        if react == 'set_beacon_on':
            self.__user_data.set_use_line_beacon(1)
            self.__line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text='Beacon EcoをONに設定しました'
                )
            )
        elif react == 'set_beacon_off':
            self.__user_data.set_use_line_beacon(2)
            self.__line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text='Beacon EcoをOFFに設定しました'
                )
            )
        else:
            pass

    # beaconを使うかどうかを手動で設定する
    def config_beacon_msg(self, event):
            confirm_template = ConfirmTemplate(text="LINE beacon Ecoの設定を行います。Beacon Ecoを使用しますか？\nこれを用いることでスマホがビーコンから遠くにあるときはセンサを省エネ化し、センサ寿命を延ばすことができます。\nbeacon と話しかけると設定を変更できます。", actions=[
                PostbackAction(label='はい', data='set_beacon_on', displayText='はい'),
                PostbackAction(label='いいえ', data='set_beacon_off', displayText='いいえ'),
            ])
            template_message = TemplateSendMessage(
                alt_text='Confirm alt text', template=confirm_template)
            self.__line_bot_api.reply_message(event.reply_token, template_message)

    def readBeaconConfig(self):
        if self.__user_data.json_data['use_line_beacon'] == 1:
            return True
        else:
            return False