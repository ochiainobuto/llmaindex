import os
import sys

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
from langchain import OpenAI

from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, StringIterableReader,PromptHelper
from llama_index import Document, LLMPredictor

app = Flask(__name__)
input_text = ""
indexnames = ""
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
	global input_text,indexnames,filenames,history

	# print("upload....")
	# sys.stdout.flush()

	apikey = request.form['apikey']
	os.environ["OPENAI_API_KEY"] = apikey
	question = request.form['question']
	modelType = request.form['modelType']

	print("input_text0: ", input_text)
	sys.stdout.flush()

	if input_text == "":
		if request.files['input_text']:
			upload_files = request.files.getlist('input_text')

			for file in upload_files:
				filenames = filenames + file.filename + ' '
				input_text = input_text + file.stream.read().decode()
				filename = file.filename
				indexnames = indexnames + file.filename.split('.')[0]

	print("input_text1:", input_text)
	sys.stdout.flush()

	print(filenames)
	documents = [Document(input_text)]

	# llm_predictor = LLMPredictor(llm=OpenAI(
	#     temperature=0, # 温度
	#     model_name=modelType, # モデル名
	#     max_tokens=1000
	# ))
	# define LLM
	llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=1000))

	#PromptHelperの準備
	if modelType=="gpt-3.5-turbo":
		prompt_helper=PromptHelper(
			max_input_size=4000,  # LLM入力の最大トークン数
			num_output=256,  # LLM出力のトークン数
			chunk_size_limit=2000,  # チャンクのトークン数
			max_chunk_overlap=0,  # チャンクオーバーラップの最大トークン数
			separator="。"  # セパレータ
		)
	else:
		prompt_helper=PromptHelper(
			max_input_size=4000,  # LLM入力の最大トークン数
			num_output=256,  # LLM出力のトークン数
			chunk_size_limit=2000,  # チャンクのトークン数
			max_chunk_overlap=0,  # チャンクオーバーラップの最大トークン数
			separator="。"  # セパレータ
		)

	try:
		index = GPTVectorStoreIndex.load_from_disk(indexnames + '.json')
	except:
		# インデックスの作成
		index = GPTVectorStoreIndex(
			documents,  # ドキュメント
			llm_predictor=llm_predictor,  # LLMPredictor
			prompt_helper=prompt_helper  # PromptHelper
		)
		index.save_to_disk(indexnames + '.json')
	# print("question: ", question)
	# sys.stdout.flush()

	if question != "":
		output = index.query(question)
		history.append("User: "+str(question))
		history.append("System: "+str(output))

		print("output: ", output)
		sys.stdout.flush()

	return render_template('index.html', apikey=apikey, question=question, output=output, filenames=filenames, history=history, modelType=modelType)


@app.route('/clear', methods=['POST'])
def clear():
	global input_text,indexnames,filenames,history

	modelType = "gpt-3.5-turbo"
	indexnames = ""
	try:
		os.remove(indexnames + '.json')
	except:
		pass

	print("clear...")

	apikey = request.form['apikey']
	os.environ["OPENAI_API_KEY"] = apikey
	input_text = ""
	question = ""
	filenames = ""
	input_text = ""
	output = ""
	history = []

	return render_template('index.html', apikey=apikey, question=question, output=output, filenames=filenames, history=history, modelType=modelType)

if __name__ == '__main__':
	app.run()
