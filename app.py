# -*- coding: utf-8 -*-
import os

from flask import Flask
from langchain import OpenAI

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello, world'

if __name__ == '__main__':
    app.run()
