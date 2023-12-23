from flask import Flask
# import os

# test = os.environ.get("MYAPIKEY")

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"


@app.route('GPT_output')
def GPT(): 
    return("Hello this is chatGPT here")

