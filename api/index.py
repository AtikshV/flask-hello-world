from flask import Flask, make_response, request
from flask_cors import CORS
import os
import openai
from openai import OpenAI
from urllib.parse import unquote
import json
import tiktoken

PASSWORD = os.environ.get("PASSWORD")
client = OpenAI(
    api_key=os.environ.get("MYAPIKEY")
)

# print("version: " + openai.VERSION)

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
            response = client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages = messages
            )
            ChatGPT_reply = response.choices[0].message.content.strip()
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
        user_input = request.form["user_input"]
        print(user_input)

        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        num_tokens = num_tokens_from_messages(messages_new)
        print(str(num_tokens))
        


        # name = request.form["name"]
        # messages.append({"role": "system", "content": "My name is " + name + ".Try to refer to me by my name often. "})

        if passkey == PASSWORD:

            if num_tokens < 4000: # normal

                print("there are a good num of tokens: " + str(num_tokens))

                response = make_response("hello")
                response.headers["Access-Control-Allow-Origin"] = "*"
                # print(request.form["data"])
                messages_new.append({"role": "user", "content": user_input})

                response = client.chat.completions.create(
                    model = "gpt-3.5-turbo",
                    messages = messages_new
                )

                # ChatGPT_reply = response["choices"][0]["message"]["content"]
                ChatGPT_reply = response.choices[0].message.content.strip()
                messages_new.append({"role": "assistant", "content": ChatGPT_reply})
                
                # return jsonify({"response": ChatGPT_reply})
                print(messages_new)
                print(ChatGPT_reply)
                # return(ChatGPT_reply)
                return(messages_new)
            else: # too many tokens, need to compress
                print("There are too many tokens: " + str(num_tokens))
                response = make_response("hello")
                response.headers["Access-Control-Allow-Origin"] = "*"
                # print(request.form["data"])

                # COMPRESS HERE

                messages_new.append({"role": "user", "content": user_input})

                response = client.chat.completions.create(
                    model = "gpt-3.5-turbo",
                    messages = messages_new
                )
                ChatGPT_reply = response.choices[0].message.content.strip()
                messages_new.append({"role": "assistant", "content": ChatGPT_reply})
                
                # return jsonify({"response": ChatGPT_reply})
                print(messages_new)
                print(ChatGPT_reply)
                # return(ChatGPT_reply)
                return(messages_new)

                 
        
        else:
            return("sorry")

    

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens