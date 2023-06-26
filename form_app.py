import pdb
import requests
import datetime
from flask import Flask, request
from slack_bolt import App
slack_token = 'slack_access_token'
app = Flask(__name__)
import json

def open_json():
	file_json = open('payload.json')
	# pdb.set_trace()
	return json.load(file_json)

@app.route("/")
def hello_world():
    return "Hello"

@app.route("/form")
def hit_form():
    date_now = datetime.datetime.now()
    str_date = date_now.strftime("%d %B, %Y")
    url = 'incoming_webhook_url'
    payload = {
            'blocks': open_json()
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print('Form questions sent successfully.')
    else:
        print(f'Error sending form questions: {response.text}')

# @app.route('/slack')
# def handle_slash_command():
#     # Extract the trigger_id from the request payload
#     payload = request.form.get('payload')
#     pdb.set_trace()
#     trigger_id = payload['callback_id']
#     print("--------------callback_id----------------")
#     print(trigger_id)
#     print("------------------------------")

#     return '', 200

if __name__ == '__main__':
    app.run()
