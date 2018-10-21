from UserData import UserData

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
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
            reply_token,
            line_bot_api,
            userData):
        self.__reply_token = reply_token
        self.__user_data = userData
        self.__line_bot_api = line_bot_api

    def activationMsg(self):
        # Lineビーコンが接続された場合、もし0:未設定なら設定プロセスを起動する
        if self.__user_data.json_data['use_line_beacon'] is 0:
            confirm_template = ConfirmTemplate(text="LINE beacon が接続されたようです。Beacon Ecoを使用しますか？\nこれを用いることでスマホがビーコンから遠くにあるときはセンサを省エネ化し、センサ寿命を延ばすことができます。\nbeacon と話しかけると設定を変更できます。", actions=[
                PostbackAction(label='Yes', data='set_beacon_on', displayText='はい！'),
                PostbackAction(label='No', data='set_beacon_off', displayText='いいえ'),
            ])
            template_message = TemplateSendMessage(
                alt_text='Confirm alt text', template=confirm_template)
            self.__line_bot_api.reply_message(self.__reply_token, template_message)


    def setBeacon(self, react):
        # ビーコンのOnとOffを変更する
        if react is 'set_beacon_on':
            self.__user_data.set_use_line_beacon(1)
            self.__line_bot_api.reply_message(
                self.__reply_token,
                TextSendMessage(
                    text='BeaconをONに設定しました'
                )
            )
        elif react is 'set_beacon_off':
            self.__user_data.set_use_line_beacon(2)
            self.__line_bot_api.reply_message(
                self.__reply_token,
                TextSendMessage(
                    text='BeaconをOFFに設定しました'
                )
            )

    # beaconを使うかどうかを手動で設定する
    def configBeaconMsg(self):
            confirm_template = ConfirmTemplate(text="LINE beacon の設定を行います。Beacon Ecoを使用しますか？\nこれを用いることでスマホがビーコンから遠くにあるときはセンサを省エネ化し、センサ寿命を延ばすことができます。\nbeacon と話しかけると設定を変更できます。", actions=[
                PostbackAction(label='Yes', data='set_beacon_on', displayText='はい'),
                PostbackAction(label='No', data='set_beacon_off', displayText='いいえ'),
            ])
            template_message = TemplateSendMessage(
                alt_text='Confirm alt text', template=confirm_template)
            self.__line_bot_api.reply_message(self.__reply_token, template_message)

    def readBeaconConfig(self):
        if self.__user_data.json_data['use_line_beacon'] is 1:
            return True
        else:
            return False