from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
import concurrent.futures as futures

from argparse import ArgumentParser

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
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

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
print(channel_secret, file=sys.stderr)
print(channel_access_token, file=sys.stderr)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# ========================= whisper独自のフィールド ========================

from UserData import UserData
from PlantAnimator import PlantAnimator
from beaconWhisperEvent import BeaconWhisperEvent
from datetime import datetime

user_data = UserData()

plant_animator = PlantAnimator(user_data, line_bot_api)
beacon_whisper_event = BeaconWhisperEvent(line_bot_api,user_data)

user_id = "U70418518785e805318db128d8014710e"

# =========================================================================


# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    split_msg = text.split(' ')

    def reply(msgs):
        if not isinstance(msgs, (list, tuple)):
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msgs))
        else:
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=msg) for msg in msgs])

    # ユーザIDの取得
    
    # 送られてきた言葉が植物の名前だった場合は、それをキャッシュし「なに？」と返す
    # if user_data.plant_exists(text):
    #     current_plant = text
    #     line_bot_api.reply_message(
    #         event.reply_token, TextSendMessage(text='なに？'))
    
    # まずは現在アクティベートされている植物に対してCommunicateを投げる
    # 追記：先にcommunicateするのは拙い。システム処理に関する言葉も植物に投げられることになる
    # plant_animator.communicate(text, event)

    if text == 'bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='またね、今までありがとう'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='またね、今までありがとう'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="この会話から退出させることはできません"))

    # ユーザからビーコンの設定を行う
    elif text == 'beacon':
        beacon_whisper_event.config_beacon_msg(event)

    elif text == 'disconnect':
        reply(plant_animator.disconnect(event))

    # 植物の生成を行う
    elif split_msg[0] in ('create', 'register'):
        if len(split_msg) == 2:
            name = split_msg[1]
            reply(plant_animator.register_plant(name))
        elif len(split_msg) == 1:
            reply("名前が設定されていません")
        else:
            reply(("メッセージが不正です", "例：create `植物の名前`"))

    # 植物との接続命令
    elif split_msg[0] in ('connect', ):
        if len(split_msg) == 2:
            reply(plant_animator.connect(text.split[1], event)) 
        elif len(split_msg) == 1:
            reply("植物が選択されていません")
        else:
            reply(("メッセージが不正です：", "例：connect `植物の名前`"))

    # 植物を削除するときの命令
    elif split_msg[0] in ('delete', 'eliminate', 'remove'):
        if len(split_msg) == 2:
            reply(plant_animator.delete_plant(split_msg[1]))
        elif len(split_msg) == 1:
            reply("植物が選択されていません")
        else:
            reply(("メッセージが不正です：" , "例：delete `植物の名前`"))

    # 植物を削除するときの命令
        # if split_msg[1] is not None:        
        #     confirm_template = ConfirmTemplate(text= split_msg[1] +"の情報を削除します\n本当によろしいですか？\n", actions=[
        #         PostbackAction(label='Yes', data='delete_plant '+ split_msg[1], displayText='はい'),
        #         PostbackAction(label='No', data='delete_plant_cancel '+ split_msg[1], displayText='いいえ'),
        #     ])
        #     template_message = TemplateSendMessage(
        #         alt_text='Confirm alt text', template=confirm_template)
        #     line_bot_api.reply_message(event.reply_token, template_message)
        # else:
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(
        #             text='植物が選択されていません'
        #         )
        #     )
    else:
        msg = plant_animator.communicate(text, event)
        if msg is not None:
            reply(msg)
        # line_bot_api.reply_message(
        #     event.reply_token, TextSendMessage(text=event.message.text))



@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )


# Other Message Type
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    else:
        return

    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save content.'),
            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])


@handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='file-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '-' + event.message.file_name
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save file.'),
            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])


@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Got follow event'))


@handler.add(UnfollowEvent)
def handle_unfollow():
    app.logger.info("Got Unfollow event")


@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Joined this ' + event.source.type))


@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Got leave event")


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'ping':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='pong'))
    elif event.postback.data == 'datetime_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['datetime']))
    elif event.postback.data == 'date_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['date']))
    elif event.postback.data in ('set_beacon_on', 'set_beacon_off'):
        # ビーコンを使うかどうかを設定するときの"YES", "No"を押したときの挙動を設定
        beacon_whisper_event.set_beacon(event)
    else: 
        # 植物の名前を消すときにはワンクッション挟んであげる
        data = event.postback.data.split()
        if data[0] == 'delete_plant':
            plant_animator.delete_plant(data[1])
        elif data[0] == 'delete_plant_cancel':
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text='ありがとう^^'
                )
            )
    
    
# ビーコンがかざされたときに呼ばれる処理
@handler.add(BeaconEvent)
def handle_beacon(event):
    if plant_animator.listen_beacon_span(int(datetime.now().strftime('%s'))):
        beacon_whisper_event.activation_msg(event)
        if user_data.json_data['use_line_beacon'] is 1:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text='おかえりなさい！'
                         ))
            plant_animator.listen_beacon(int(datetime.now().strftime('%s')), user_data.json_data['use_line_beacon'])

import time

# should be modified when required
def update():
    plant_animator.update()
    

def main_loop(clock_span):
    while 1:
        time.sleep(clock_span)
        update()

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # create tmp dir for download content
    make_static_tmp_dir()

    def push_message(msg):
        line_bot_api.push_message(user_id, TextSendMessage(text=msg))

    plant_animator.push_message = push_message

    with futures.ThreadPoolExecutor(2) as exec:
        exec.submit(app.run, debug=options.debug, port=options.port)
        exec.submit(main_loop, 0.9)
