from flask import Flask
from flask_cors import CORS
# import os

# test = os.environ.get("MYAPIKEY")

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello, World!"


@app.route('/GPT_output')
def GPT(): 
    return("Hello this is chatGPT here")

