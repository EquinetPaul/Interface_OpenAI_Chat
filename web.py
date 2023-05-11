#######
# API #
#######
import requests
import json

username = ""
password = ""
host = ""
port = ""

def call_api(input, token):
    url = "https://api.openai.com/v1/chat/completions"
    proxies = {
      'http': f'http://{username}:{password}@{host}:{port}',
      'https': f'http://{username}:{password}@{host}:{port}'
    }
    payload = json.dumps({
      "model": "gpt-3.5-turbo",
      "messages": [
        {
          "role": "user",
          "content": input
        }
      ],
      "n": 1,
      "max_tokens": 2048
    })
    headers = {
      'Authorization': 'Bearer '+token+'',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies, verify=False)

    return response.text

#######
# WEB #
#######
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['message']
    token = request.form['token']
    response_api = call_api(user_input, token=token)
    json_response_api = json.loads(response_api)
    msg_api = json_response_api["choices"][0]["message"]["content"]
    return render_template('index.html', response=msg_api, input=user_input, token=token)

if __name__ == '__main__':
    app.run(debug=True)
