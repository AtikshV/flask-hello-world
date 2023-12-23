from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
import uuid
import openai
import gradio
# import config
from langchain.memory import ConversationSummaryBufferMemory
from langchain.llms import OpenAI 
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate  ,
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate,
)

import gtts
from playsound import playsound
from io import BytesIO

import speech_recognition as sr

from transformers import pipeline
import numpy as np 

import multiprocessing
import time
import os

# openai.api_key = config.MYAPIKEY
# openai.api_key = os.environ.get("MYAPIKEY")



messages = [
    {"role": "system", "content": "You are my very good friend. You must always keep the conversation going, share your experiences and asking followup questions from our discussion. Your responses should be as if humans are discussing and short as possible. Please start the conversation with a greeting and as if we met not so long ago "}
    ]

app = Flask(__name__)
CORS(app)

@app.route("/") 
def home(): 
    return "Hello World!"


@app.route("/GPT_output", methods=["POST"])
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



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True) 

    
