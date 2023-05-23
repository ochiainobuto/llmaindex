from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from langchain import OpenAI

import sys

from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, StringIterableReader,PromptHelper
from llama_index import Document, LLMPredictor


app = Flask(__name__)


#環境変数取得
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

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
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))

    # 受信したメッセージのテキストを取得
    text = event.message.text

    # テキストに対する処理を実行
    processed_text = process_text(text)

    # 返信メッセージを作成して送信
    reply_message = TextSendMessage(text=processed_text)
    line_bot_api.reply_message(event.reply_token, reply_message)


def process_text(text):
    text = text + 'ありんす。'
	# os.environ["OPENAI_API_KEY"] = apikey
    question = text
    modelType = 'gpt-3.5-turbo'

	llm_predictor = LLMPredictor(llm=OpenAI(
	    temperature=0, # 温度
	    model_name=modelType # モデル名
	))

    prompt_helper=PromptHelper(
        max_input_size=6000,  # LLM入力の最大トークン数
        num_output=2000,  # LLM出力のトークン数
        chunk_size_limit=4000,  # チャンクのトークン数
        max_chunk_overlap=0,  # チャン
    )

    index = GPTSimpleVectorIndex.load_from_disk('data.json')
    output = index.query(question)
		
    return output

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)