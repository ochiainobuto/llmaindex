# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
from langchain import OpenAI

openai.api_key = os.environ["OPENAI_API_KEY"]

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello, world'

if __name__ == '__main__':
    app.run()
