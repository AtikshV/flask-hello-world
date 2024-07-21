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

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello, World!"
        
@app.route('/GPT_output_msg', methods=["POST"])
def speech_msg():
    messages_new = json.loads(unquote(request.form["data"]))
    print(messages_new)
    passkey = request.form["pass"]
    print(passkey)
    user_input = request.form["user_input"]
    print(user_input)
    # name = request.form["name"]
    # print(name)
    # test_tokens = request.form["tokens"]
    # print("test_tokens: " + test_tokens)

    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    num_tokens = num_tokens_from_messages(messages_new, "gpt-4o-mini")
    print(str(num_tokens))
    # num_tokens = test_tokens
    

    if passkey == PASSWORD:

        response = make_response("hello")
        response.headers["Access-Control-Allow-Origin"] = "*"

        if int(num_tokens) > 2000:
            print("There are too many tokens: " + str(num_tokens)) 
            messages_new = summarize(messages_new)
        
        messages_new.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = messages_new
        )

        ChatGPT_reply = response.choices[0].message.content.strip()
        messages_new.append({"role": "assistant", "content": ChatGPT_reply})

        print(messages_new)
        print(ChatGPT_reply)
        
        return(messages_new)
                
    
    else:
        return("sorry")
        
# @app.route('/test_msg', methods=["POST"])
# def test_msg():
#     messages_new = json.loads(unquote(request.form["data"]))
#     print(messages_new[1]["content"])
#     passkey = request.form["pass"]
#     # print(passkey)
#     user_input = request.form["user_input"]
#     # print(user_input)
#     # name = request.form["name"]
#     # print(name)
#     # test_tokens = request.form["tokens"]
#     # print("test_tokens: " + test_tokens)

#     encoding = tiktoken.encoding_for_model("gpt-4o-mini")
#     num_tokens = num_tokens_from_messages(messages_new, "gpt-4o-mini")
#     # print(str(num_tokens))
#     # num_tokens = test_tokens
    

#     if passkey == PASSWORD:

#         response = make_response("hello")
#         response.headers["Access-Control-Allow-Origin"] = "*"


#         messages_new = summarize(messages_new)

        
#         messages_new.append({"role": "user", "content": user_input})

#         response = client.chat.completions.create(
#             model = "gpt-4o-mini",
#             messages = messages_new
#         )

#         ChatGPT_reply = response.choices[0].message.content.strip()
#         messages_new.append({"role": "assistant", "content": ChatGPT_reply})
#         # print(messages_new)
#         # print(ChatGPT_reply)
        
#         return(messages_new)
                
    
#     else:
#         return("sorry")


def summarize(messages):

    system_msg = messages[0]["content"]
    name_msg = messages[1]["content"]
    print(system_msg)
    print(name_msg)
    
    messages.append(
        {"role": "user", "content": "Please provide a concise summary of our conversation highlighting the key topics discussed and any conclusions reached."}
    )


    context_reply = client.chat.completions.create( 
        model="gpt-4o-mini",
        messages=messages
    )
    context = context_reply.choices[0].message.content.strip()
    print(context)

    messages.append({"role": "system", "content": system_msg}) 
    messages.append({"role": "system", "content": name_msg}) 
    messages.append({"role": "assistant", "content": context}) # Appending context to chat history as assistant

    print(messages)
    return messages



def num_tokens_from_messages(messages, model):
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