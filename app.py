    #!/usr/bin/env python
# -*- coding: utf-8 -*-

# from __future__ import print_function
from flask import Flask, request, redirect, session



from time import gmtime, strftime
import json
from random import randint
from datetime import datetime, timedelta
import io
import os # For API AI
import sys # For API AI
import re
import time
import requests # For the webhook



HUB_VERIFY_TOKEN = "hello"
fbToken = 'EAAMnZBjjGep0BAKZB3KSM9qcMN0eC0Fw25jDjNDP9icLWb4gX9fjiTQUZApYq8TJ3XzKYh6QdHwvOroZCSYPxcoCAm5ygZCu7qlO7Vm3B5AhniGVacqliZBA7lYDRLzZAsu2cOtvlBd1XSLRTwRNK0Kts79ppFd2SfAsfZAulQQfLwZDZD'


facebook_url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + str(fbToken) # Messenger

TIMEZONE = 'US/Pacific'


# Flask app configuration
app = Flask(__name__)
app.config.from_object(__name__)


# MARK: helper methods
# twilio_to_slack: pushes an incoming message to slack
# -Parmaters: sender = fbPageID , message = Message to send to slack

#MARK: FBGet
@app.route("/webhook", methods=["GET"])
def fb_webhook():
    verification_code = HUB_VERIFY_TOKEN
    verify_token = request.args.get("hub.verify_token")
    if verification_code == verify_token:
        return request.args.get('hub.challenge')


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        #get a json from request
        data = json.loads(request.data)
        messaging_events = data['entry'][0]['messaging']
        sender = messaging_events[0]['sender']['id']
        # msg = SendMessage(sender)
        # msg.sendMessage("hey")
        # msg.sendMessage(data)

        print(data)

        payload = {'recipient': {'id': sender}, 'message': {"text": "hey"}} # We're going to send this back
        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
   
        payload = {'recipient': {'id': sender}, 'message': {"text": str(data)}} # We're going to send this back
        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
   


    except Exception as e:
        print(e)

   
    #     #TODO check if they sent an audio message
