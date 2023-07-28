import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import base64
import hashlib
import hmac

app = Flask(__name__)

channel_secret = os.environ.get("CHANNEL_SECRET")
channel_access_token = os.environ.get("CHANNEL_ACCESS_TOKEN")

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/", methods=["GET", "POST"])
def callback():
    if request.method == "GET":
        return "Get Test"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        app.logger.info("Request body: ", body)
        app.logger.info("Request header: ", request.headers)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text

    # Send To Line
    reply = TextSendMessage(text=f"{get_message}")
    line_bot_api.reply_message(event.reply_token, reply)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    # port = 5000
    # app.run(host="127.0.0.1", port=port)
