from flask import Flask, make_response, request
from flask_cors import CORS
import os
import openai


test = os.environ.get("MYAPIKEY")

messages = [
    {"role": "system", "content": "You are my very good friend. You must always keep the conversation going, share your experiences and asking followup questions from our discussion. Your responses should be as if humans are discussing and short as possible. Please start the conversation with a greeting and as if we met not so long ago "}
    ]
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello, World!"


@app.route('/GPT_output', methods=["POST"])
def speech():
        user_input = request.form["data"]

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
        return  (ChatGPT_reply)
