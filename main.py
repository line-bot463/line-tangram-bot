from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

tangrams = {
    "貓": {
        "image": "https://i.imgur.com/XXXXcat.jpg",
        "instructions": "貓的拼法：1. 用大三角形做身體，2. 小三角形做耳朵..."
    },
    "鳥": {
        "image": "https://i.imgur.com/XXXXbird.jpg",
        "instructions": "鳥的拼法：1. 大三角形做翅膀，2. 小正方形當身體..."
    }
}

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.strip()
    tangram = tangrams.get(msg)
    if tangram:
        line_bot_api.reply_message(
            event.reply_token,
            [
                ImageSendMessage(
                    original_content_url=tangram["image"],
                    preview_image_url=tangram["image"]
                ),
                TextSendMessage(text=tangram["instructions"])
            ]
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="目前沒有這個圖案，請試試輸入：貓、鳥")
        )

if __name__ == "__main__":
    app.run()
