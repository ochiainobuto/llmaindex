from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
from langchain import OpenAI

import os
import sys

from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, StringIterableReader,PromptHelper
from llama_index import Document, LLMPredictor

app = Flask(__name__)
input_text = ""
filenames = ""
history = []

@app.route('/')
def index(apikey="", question="", output=""):
	print("index....")
	global input_text,history

	input_text = ""
	return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	global input_text,filenames,history

	# print("upload....")
	# sys.stdout.flush()

	apikey = request.form['apikey']
	os.environ["OPENAI_API_KEY"] = apikey
	question = request.form['question']

	print("input_text0: ", input_text)
	sys.stdout.flush()

	if input_text == "":
		if request.files['input_text']:
			upload_files = request.files.getlist('input_text')

			for file in upload_files:
				filenames = filenames + file.filename + ' '
				input_text = input_text + file.stream.read().decode()

	print("input_text1:", input_text)
	sys.stdout.flush()

	documents = [Document(input_text)]

	# LLMPredictorの準備
	llm_predictor = LLMPredictor(llm=OpenAI(
	    temperature=0, # 温度
	    model_name="text-davinci-003" # モデル名
	))

	# PromptHelperの準備
	prompt_helper=PromptHelper(
	    max_input_size=4000,  # LLM入力の最大トークン数
	    num_output=2000,  # LLM出力のトークン数
	    chunk_size_limit=2000,  # チャンクのトークン数
	    max_chunk_overlap=0,  # チャンクオーバーラップの最大トークン数
	    separator="。"  # セパレータ
	)

	# インデックスの作成
	index = GPTSimpleVectorIndex(
	    documents,  # ドキュメント
	    llm_predictor=llm_predictor,  # LLMPredictor
	    prompt_helper=prompt_helper  # PromptHelper
	)

	# print("question: ", question)
	# sys.stdout.flush()

	if question != "":
		output = index.query(question)
		history.append("User: "+str(question))
		history.append("System: "+str(output))

	# print("output: ", output)
	# sys.stdout.flush()

	return render_template('index.html', apikey=apikey, question=question, output=output, filenames=filenames, history=history)


@app.route('/clear', methods=['POST'])
def clear():
	global input_text,filenames,history

	print("clear...")

	apikey = request.form['apikey']
	os.environ["OPENAI_API_KEY"] = apikey
	input_text = ""
	question = ""
	filenames = ""
	input_text = ""
	output = ""
	history = []

	return render_template('index.html', apikey=apikey, question=question, output=output, filenames=filenames, history=history)

if __name__ == '__main__':
	app.run()
