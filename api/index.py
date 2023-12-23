from flask import Flask
import os

test = os.environ.get("MYAPIKEY")

app = Flask(__name__)

@app.route('/')
def home():
    return test

@app.route('/about')
def about():
    return 'About'
