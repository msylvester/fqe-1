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
fbToken = os.environ.get('EAAMnZBjjGep0BAKZB3KSM9qcMN0eC0Fw25jDjNDP9icLWb4gX9fjiTQUZApYq8TJ3XzKYh6QdHwvOroZCSYPxcoCAm5ygZCu7qlO7Vm3B5AhniGVacqliZBA7lYDRLzZAsu2cOtvlBd1XSLRTwRNK0Kts79ppFd2SfAsfZAulQQfLwZDZD')


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
        msg = SendMessage(sender)
        msg.sendMessage("hey")

    except Exception as e:
        print(e)

    return ""
    #     #TODO check if they sent an audio message


# Helper method to check if a value can be converted to an int
def can_convert_to_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def get_user_model(sender):


    user = {}

    try:
        r = requests.get("https://graph.facebook.com/v2.6/"+ str(sender) + "?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=" +str(fbToken))

        try:
            name = r.json()['first_name']


        except KeyError as e:
            print(e)

        try:
            last_name = r.json()['last_name']


        except KeyError as e:
            print(e)

        try:
            gender = r.json()['gender']


        except KeyError as e:
            print(e)

        try:
            profile_pic = r.json()['profile_pic']


        except KeyError as e:
            print(e)
        try:
            locale = r.json()['locale']


        except KeyError as e:
            print(e)
        try:
            timezone = r.json()['timezone']


        except KeyError as e:
            print(e)


        user =  {
                    "first_name":name,
                    "last_name": last_name,
                    "gender": gender,
                    "profile_pic": profile_pic,
                    "locale": locale,
                    "timezone": timezone

        }

    except Exception as e:
        print("Could not find name: " + str(e))


    return user



def ask_for_admin(sender):
    message_content = ""
    messageData = {
    "recipient":{
            "id":sender
          },
          "message":{
            "text":"What type of user are you?",
            "quick_replies":[
              {
                "content_type":"text",
                "title":"Admin",
                "payload":"admin_quick_reply"
              },
              {
                "content_type":"text",
                "title":"User",
                "payload":"user_quick_reply"
              }

            ]
          }
        }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + str(fbToken), json=messageData)
    #return "hello"
