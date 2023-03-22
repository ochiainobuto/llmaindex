from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import openai

import os
#os.environ["OPENAI_API_KEY"] = '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'
#openai.api_key = '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'
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, StringIterableReader,PromptHelper
from llama_index import Document

app = Flask(__name__)
input_text = ""

@app.route('/')
def index(apikey="", question="", output="", filename="選択されていません"):
	print("index....")
	global input_text

	input_text = ""
	return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
	global input_text

	print("upload....")

	apikey = request.form['apikey']
	os.environ["OPENAI_API_KEY"] = apikey
	question = request.form['question']

	if input_text == "":
		filenames = ""
		if request.files['input_text']:
			upload_files = request.files.getlist('input_text')

			for file in upload_files:
				filenames = filenames + file.filename + ' '
				input_text = file.stream.read().decode()

	documents = [Document(input_text)]
	index = GPTSimpleVectorIndex(
	    documents=documents
	)

	if question != "":
		output = index.query(question)

	return render_template('index.html', apikey=apikey, question=question, output=output, filenames=filenames)

@app.route('/clear', methods=['POST'])
def clear():
	global input_text

	print("clear...")

	apikey = request.form['apikey']
	os.environ["OPENAI_API_KEY"] = apikey
	question = ""
	filenames = ""
	input_text = ""
	output = ""

	return render_template('index.html', apikey=apikey, question=question, output=output, filenames=filenames)

if __name__ == '__main__':
	app.run()
