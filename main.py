# coding=utf-8

from flask import Flask,request,jsonify,abort,make_response
import os
from multiprocessing import Process
import time
import requests
import base64

app = Flask(__name__)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
XI_API = os.environ.get('XI_API')
THIS_URL = os.environ.get('THIS_URL')
process_list = {}

@app.route('/<string:token>', methods=["POST"])
def webhook(token):
    if token != BOT_TOKEN:
        abort(404)
    
    data = request.json
    try:
        userid = data['inline_query']['from']['id']
        content = data['inline_query']['query']
        inline_query_id = data['inline_query']['id']
        if process_list.has_key(userid):
            process_list[userid].terminate()
        process_list[userid] = Process(target=compute, args=(content,inline_query_id,))
        process_list[userid].start()
    except:
        pass
    return ""

@app.route('/voice/<uuid:task_id>', methods=['GET'])
def ogg_file(task_id):
    r = requests.get("{}/result?id={}".format(XI_API,task_id))
    ogg_audio = r.json()["result"]["audio"]
    resp = make_response(base64.b64decode(ogg_audio))
    resp.headers['Content-Type'] = "audio/ogg"
    return resp


def compute(content,inline_query_id):
    time.sleep(3)
    print content
    try:
        r = requests.post("{}/task_ogg".format(XI_API), json={"text": content})
        if not r.json()["request_successful"]:
            raise
        task_id = r.json()["id"]

        while True:
            time.sleep(1)
            r = requests.get("{}/progress?id={}".format(XI_API,task_id))
            if not r.json()["request_successful"]:
                raise
            if r.json()["result"]["finished"]:
                break

    except:
        print "Except Exit."
        return
    
    body = {
        "inline_query_id": inline_query_id,
        "results": [
            {
                "type": "voice",
                "id": task_id,
                "voice_url": "{}/voice/{}".format(THIS_URL,task_id),
                "title": content
            }
        ]
    }
    requests.post("https://api.telegram.org/bot{}/answerInlineQuery".format(BOT_TOKEN), json=body)

def init_webhook():
    webhook_url = "{}/{}".format(THIS_URL,BOT_TOKEN)
    requests.post("https://api.telegram.org/bot{}/setWebhook".format(BOT_TOKEN), json={"url":webhook_url})
    print "Telegram Webhook is already set."

if __name__ == '__main__':
    init_webhook()
    app.run(host='0.0.0.0', debug=True)
