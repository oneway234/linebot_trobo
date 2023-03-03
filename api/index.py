from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import ChatGPT

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"

app = Flask(__name__)
chatgpt = ChatGPT()

# domain root
@app.route('/')
def home():
    return 'Hello, World! 725'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status
    if event.message.type != "text":
        return

    if event.message.text == "hi":
        working_status = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="working"))
        return

    if working_status:
        chatgpt.add_msg("user", f"{event.message.text}")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))
        reply_msg = chatgpt.get_response().replace("AI:", "", 1)
        chatgpt.add_msg("assistant", f"{reply_msg}")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))


if __name__ == "__main__":
    app.run()

# from flask import Flask, request, abort
# from linebot import LineBotApi, WebhookHandler
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage
# from api.chatgpt import ChatGPT
#
# import os
#
# line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
# line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
# working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"
#
# app = Flask(__name__)
# chatgpt = ChatGPT()
#
# # domain root
# @app.route('/')
# def home():
#     return 'Hello, World!a'
#
# @app.route("/webhook", methods=['POST'])
# def callback():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']
#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
#     # handle webhook body
#     try:
#         line_handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#     return 'OK'
#
#
# @line_handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     global working_status
#     if event.message.type != "text":
#         return
#
#     if event.message.text == "說話":
#         working_status = True
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text="我可以說話囉，歡迎來跟我互動 ^_^ "))
#         return
#
#     if event.message.text == "閉嘴":
#         working_status = False
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text="好的，我乖乖閉嘴 > <，如果想要我繼續說話，請跟我說 「說話」 > <"))
#         return
#
#     if working_status:
#         # chatgpt.messages_container("user", f"HUMAN:{event.message.text}?\n")
#         TextSendMessage(text=event.message.text)
#         # reply_msg = chatgpt.get_response().replace("AI:", "", 1)
#         # chatgpt.messages_container("assistant", f"AI:{reply_msg}\n")
#         # line_bot_api.reply_message(
#         #     event.reply_token,
#         #     TextSendMessage(text=reply_msg))
#
#
# if __name__ == "__main__":
#     app.run()
