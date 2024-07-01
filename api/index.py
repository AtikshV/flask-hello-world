from flask import Flask, make_response, request
from flask_cors import CORS
import os
import openai
from urllib.parse import unquote
import json


openai.api_key = os.environ.get("MYAPIKEY")
PASSWORD = os.environ.get("PASSWORD");  

messages = [
    {"role": "system", "content": "You are my very good human friend, and your name is Andy. You must always keep the conversation going, share your experiences and asking followup questions from our discussion. Your responses should be as if humans are discussing and short as possible. Please start the conversation with a greeting and as if we met not so long ago. As a real human, you have thoughts, emotions, and feelings."}
    ]
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello, World!"


@app.route('/GPT_output', methods=["POST"])
def speech():
        user_input = request.form["data"]
        print(user_input)
        passkey = request.form["pass"]
        print(passkey)

        name = request.form["name"]
        messages.append({"role": "system", "content": "My name is " + name + ".Try to refer to me by my name often. "})

        if passkey == PASSWORD:
            response = make_response("hello")
            response.headers["Access-Control-Allow-Origin"] = "*"
            print(request.form["data"])
            messages.append({"role": "user", "content": user_input})
            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = messages
            )
            ChatGPT_reply = response["choices"][0]["message"]["content"]
            messages.append({"role": "assistant", "content": ChatGPT_reply})
            
            # return jsonify({"response": ChatGPT_reply})
            print(ChatGPT_reply)
            return(ChatGPT_reply)
        else:
            return("sorry")
        
@app.route('/GPT_output_msg', methods=["POST"])
def speech_msg():
        messages_new = json.loads(unquote(request.form["data"]))
        print(messages_new)
        passkey = request.form["pass"]
        print(passkey)

        # name = request.form["name"]
        # messages.append({"role": "system", "content": "My name is " + name + ".Try to refer to me by my name often. "})

        if passkey == PASSWORD:
            response = make_response("hello")
            response.headers["Access-Control-Allow-Origin"] = "*"
            # print(request.form["data"])
            # messages.append({"role": "user", "content": user_input})
            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = messages_new
            )
            ChatGPT_reply = response["choices"][0]["message"]["content"]
            # messages.append({"role": "assistant", "content": ChatGPT_reply})
            
            # return jsonify({"response": ChatGPT_reply})
            print(messages_new)
            print(ChatGPT_reply)
            return(ChatGPT_reply)
        else:
            return("sorry")

    
