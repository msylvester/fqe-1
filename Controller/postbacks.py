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

# from Controller.apiai_manager import apiai_query
# from Controller.messenger_manager import getUser
from View.user_messages import *
# from Controller.message import Button, SendMessage, Element
# from Controller.now import getElements

from Model.Location import *

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai



HUB_VERIFY_TOKEN = os.environ.get('HUB_VERIFY_TOKEN')

fbToken = os.environ.get('FB_TOKEN')


firebase_credential = os.environ.get('FIREBASE_CREDENTIAL') # Firebase credential "messengerbot-test"
account_sid = os.environ.get('TWILIO_ACCOUNT_SID') # Twilio
auth_token = os.environ.get('TWILIO_ACCOUNT_AUTH_TOKEN') # Twilio
facebook_url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + str(fbToken) # Messenger
client = TwilioRestClient("AC6ac444ac5e869124d78dd722524650c1", "dd19a1a9d44febebcb3450f9671648e9") # Twilio client
twilio_phone = os.environ.get('TWILIO_PHONE') # Twilio
slack = Slacker(os.environ.get('SLACK')) # Slack
TIMEZONE = 'US/Pacific'


def postback_action(data):

    # We need to extract the payload from either a postback, or a quick reply.
    # Check if it's a postback or a quick reply, and extract the payload accordingly.

    messaging_events = data['entry'][0]['messaging']
    sender = messaging_events[0]['sender']['id']

    if "postback" in messaging_events[0]:
        # It's a postback...
        payload = messaging_events[0]['postback']['payload']
    elif "quick_reply" in messaging_events[0]["message"]:
        # It's a quick reply
        payload = messaging_events[0]['message']['quick_reply']['payload']

    print("PAYLOAD: ", str(payload))


    #is the postback from ther perosonal schedule
    # if messaging_events[0]['postback']['payload'] == "frdm_personal":
    #     make_favorites(sender)

    #check to see if the postback is from the persistant menu

    if "pers_menu" in payload:
        pers_menu_handler(payload, sender)

    ###
    ### User (i.e. not Admin) related postbacks & quick replies
    ###

    if payload == "dummy_response":
        dummy_response(sender)
        return

    elif payload == "user_home":
        user_home(sender)
        return

    elif payload == "user_connect_schedule":
        user_connect_schedule(sender)
        return

    elif payload == "user_connect_message":
        user_connect_message(sender)
        return

    elif payload == "user_connect":
        user_connect(sender)
        return

    elif payload == "user_connect":
        user_connect(sender)
        return

    elif payload == "user_listen":
        user_listen(sender)
        return

    elif payload == "user_watch":
        user_watch(sender)
        return

    elif payload == "user_shop":
        user_shop(sender)
        return

    elif payload == "user_settings":
        user_settings(sender)
        return

    elif payload == "user_edit_alerts":
        user_edit_alerts(sender)
        return

    elif payload == "change_latest_news":
        change_latest_news(sender)
        return

    elif payload == "change_secret_shows":
        change_secret_shows(sender)
        return

    elif payload == "change_exclusive_content":
        change_exclusive_content(sender)
        return

    else:
        print("No postback or quick reply for this payload.")



def pers_menu_handler(payload, sender):
    menu_type = payload[9:]
    if menu_type == "main":
        make_menu(sender)
        #make sch
    elif menu_type == 'now':
        make_now(sender)
        #do the now shit
    elif menu_type == 'map':
        #donate shit
        payload =  {'recipient': {'id': sender}, "message":{ 'attachment':{ 'type':'image', 'payload':{ 'url':"http://brainitch.com/Hans/map.jpg"}}}}
        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)

    elif menu_type == "personal_schedule":
        make_favorites(sender)
        #human shit
    else:
        fbUserName = getUser(sender. fbToken)
        make_help(sender, fbUserName)
        #personal scheduler


    return


#get_user_list returns an arry of users who are neither bots nor admisn
def get_user_list():
     #get users list, notes a response object
    users = slack.users.list()

    #get the body
    users_info_json = json.dumps(users.body)
    users_parsed_json = json.loads(users_info_json)
    users_list = users_parsed_json['members']

    list_length = len(users_list)

    i = 0
    user_array = []
   #only add users to user_array who are not bots, an admin, or a slackbot
    while i < (list_length):

       if(users_list[i]['deleted'] == False):

         if users_list[i]['is_admin'] == False and users_list[i]['is_bot'] == False and users_list[i]['id'] != "USLACKBOT":
            user_array.append(users_list[i]['id'])
       i += 1


    return user_array
