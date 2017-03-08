    #!/usr/bin/env python
# -*- coding: utf-8 -*-

# from __future__ import print_function
from flask import Flask, request, redirect, session
import twilio.twiml
from slacker import Slacker
from twilio.rest import TwilioRestClient
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




from Controller.apiai_manager import apiai_query

from Controller.message import Button, SendMessage, Element
from Model.Location import *
from Controller.postbacks import *
from Controller.admin_driver import driver
from Controller.user_driver import user_routing
from Controller.apiai_manager import *

from View.admin_messages import *
from View.user_messages  import *


try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai



HUB_VERIFY_TOKEN = "hello"
fbToken = os.environ.get('EAAMnZBjjGep0BAKZB3KSM9qcMN0eC0Fw25jDjNDP9icLWb4gX9fjiTQUZApYq8TJ3XzKYh6QdHwvOroZCSYPxcoCAm5ygZCu7qlO7Vm3B5AhniGVacqliZBA7lYDRLzZAsu2cOtvlBd1XSLRTwRNK0Kts79ppFd2SfAsfZAulQQfLwZDZD')

firebase_credential = os.environ.get('FIREBASE_ACCESS_TOKEN')
account_sid = os.environ.get('TWILIO_ACCOUNT_SID') # Twilio
auth_token = os.environ.get('TWILIO_ACCOUNT_AUTH_TOKEN') # Twilio
facebook_url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + str(fbToken) # Messenger
client = TwilioRestClient(account_sid, auth_token) # Twilio client
twilio_phone = os.environ.get('TWILIO_PHONE') # Twilio
slack = Slacker(os.environ.get('SLACK')) # Slack
TIMEZONE = 'US/Pacific'


# Flask app configuration
app = Flask(__name__)
app.config.from_object(__name__)


# MARK: helper methods
# twilio_to_slack: pushes an incoming message to slack
# -Parmaters: sender = fbPageID , message = Message to send to slack
def twilio_to_slack(sender, message):
    if sender is not None:

        #this is for fb
        slack_channel = "#" + sender
    else:
        slack_channel = "#nonumber"

    # Get a list of all channels
    all_channels = slack.channels.list()
    json_dump = json.dumps(all_channels.body)
    parsed_json = json.loads(json_dump)
    channels = parsed_json["channels"]
    channels_array = []
    for channel in channels:
        channel_name = channel["name"]
        channels_array.append(channel_name)

    s = slack_channel[1:]

    #block channel if it is is blocked
    #check to see if there is channel blocked
    if "blocked" + s in channels_array:
        return ""


    if s in channels_array:
        print("in the array")
    else:
        #get a random number between 0 and the length of the userlist and invite this user to the new channel
        user_list = get_user_list()
        user_random = randint(0, len(user_list) - 1)
        slack.channels.join(slack_channel)
        channel_id =  slack.channels.get_channel_id(s)
        slack.channels.invite(channel_id, user_list[user_random])


    # Get the channel ID
    channel_id = slack.channels.get_channel_id(s)

    # Check if channel is archived or unarchived by checking the channel info
    # If archived, unarchive it
    channel_info = slack.channels.info(channel_id)
    channel_info_json = json.dumps(channel_info.body)
    parsed_json = json.loads(channel_info_json)
    is_archived = parsed_json["channel"]["is_archived"]
    print(channel_info_json)
    if is_archived:

        slack.channels.unarchive(channel_id)
        user_list = get_user_list()
        user_random = randint(0, len(user_list) - 1)
        slack.channels.join(slack_channel)
        slack.channels.invite(channel_id, user_list[user_random])
    else:

        print("was not archived")
    slack.chat.post_message(channel=slack_channel, text=message.decode('utf-8'), username='HANS: message inbound')


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
