# -*- coding: utf-8 -*-
import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]


from langchain import OpenAI



app = Flask(__name__)

@app.route('/')
def index():
    return 'hello, world'

if __name__ == '__main__':
    app.run()
