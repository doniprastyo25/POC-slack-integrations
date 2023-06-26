import pdb
import json
import requests
import datetime
from mapping_answer_form import mapping_answer
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

SLACK_API_URL = "https://slack.com/api/views.open"
SLACK_BOT_TOKEN = "xoxb-5385301141138-5386296991170-Wn2VqQZAGWTHIA4HWzt7JvO7"
# SLACK_ACCESS_TOKEN = "xoxe.xoxp-1-Mi0yLTUzODUzMDExNDExMzgtNTM3ODY0NDAxNTE3NC01NDA5NzQzMDc5NTIwLTU0NzQ4Nzk3NzU2NTItZDc3OGI4MDYyMTBkNmQzODRlMzFlNDYzMDNkNGMwMjhmZTgzOWFlMzU5NTNmMGI3NzA0ODhhMjYxNjgzNzYyNA"
url_list = [
    'https://hooks.slack.com/services/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',
    'https://hooks.slack.com/services/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',
    'https://hooks.slack.com/services/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',
    'https://hooks.slack.com/services/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'
    ]

def build_payload(type_form):
    file_json = open(f'{type_form}.json')
    return json.load(file_json)

def adjust_date(data_payload):
    date_now = datetime.datetime.now()
    str_date = date_now.strftime("%d %B, %Y")
    data_payload['blocks'][2]['fields'][0]['text'] = f'*Date:*\n{str_date}'
    return data_payload

@app.route("/")
def hello_world():
    return "test api"

@app.route('/send-alert')
def send_interactive_message():
    url = 'https://hooks.slack.com/services/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'
    data_payload = build_payload('form_performance')
    payload = adjust_date(data_payload)
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return make_response(jsonify({"message": "message already send"}), 200)
    else:
        return make_response(jsonify({"error": "Failed send message"}), response.status_code)

@app.route('/slack-interactive', methods=["POST"])
def slack_interactive():
    """
    1.get payload
        - user information
        - trigger_id
        - channel_id/name
        - date
    2.verify payload is open modal or submission
    2.check user information (for auth user is register od db)
    3.check channel_id/name (for filter what form will be send)
    4.validations date is today
    """
    data_payload = json.loads(request.form['payload'])
    print(data_payload['type'])
    if data_payload['type'] == 'view_submission':
        result_answer = mapping_answer(data_payload)
        print(json.dumps(result_answer, indent=2))
    trigger_id = data_payload['trigger_id']
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
    }
    payload = build_payload('payload')
    payload['trigger_id'] = trigger_id

    response = requests.post(SLACK_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return make_response(jsonify({"message": "Modal opened successfully"}), 200)
    else:
        return make_response(jsonify({"error": "Failed to open modal"}), response.status_code)

@app.route('/send-message', methods=["POST"])
def send_message_user():
    response_result = []
    for url in url_list:
        payload = build_payload('form_performance')
        payload = adjust_date(payload)
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            response_result.append({"message": "message already send"})
        else:
            response_result.append({"error": "Failed send message"})
    return make_response(jsonify(response_result), 200)
        

if __name__ == '__main__':
    app.run()