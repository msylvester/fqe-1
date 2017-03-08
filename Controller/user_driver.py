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
from Controller.apiai_manager import apiai_query
from Controller.message import Button, SendMessage, Element
from Model.Location import *
from Controller.postbacks import *
messenger_url = "https://graph.facebook.com/v2.6/me/messages?access_token="
ai = os.environ.get('api_ai_access_token')

firebase_credential = os.environ.get('FIREBASE_ACCESS_TOKEN')


MESSENGER_ACCESS_TOKEN = os.environ.get('FB_TOKEN')
###
### Properties
###
slack = Slacker(os.environ.get('SLACK')) # Slack


fb_token = os.environ.get('FB_TOKEN')
def user_routing(data):
    print("Data flow to user_driver.py")

    try:
        data = json.loads(request.data)
        messaging_events = data['entry'][0]['messaging']
        sender = messaging_events[0]['sender']['id']

        # Check if the user sent an image
        try:
            if "attachments" in messaging_events[0]["message"]:
                if messaging_events[0]["message"]["attachments"][0]['type'] == "image":
                    print("The user sent an image.")
                    payload = {'recipient': {'id': sender}, 'message': {"text": "We received your image, thanks!"}} # We're going to send this back
                    r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
                    image_url = messaging_events[0]["message"]['attachments'][0]['payload']['url']
        except Exception as e:
            print("Exception when checking for an image: " + str(e))


        # Check to see if it is a location
        try:
            if "attachments" in messaging_events[0]["message"]:
                if messaging_events[0]["message"]["attachments"][0]['type'] == "location":
                    req = messaging_events[0]['message']['attachments'][0]
                    location_local = Location(req['title'], req['payload']['coordinates']['long'], req['payload']['coordinates']['lat'], req['url'], messaging_events[0]['timestamp'], messaging_events[0]['recipient']['id'])
                    payload = {'recipient': {'id': sender}, 'message': {"text": "We received your location, thanks! \n" + str(location_local.getLat()) + "\n" + str(location_local.getLong())}} # We're going to send this back
                    r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
        except Exception as e:
            print("Exception when checking for a location: " + str(e))


        ###
        ### Check for a postback payload
        ###
        if "postback" in messaging_events[0]:
            print("User sent a postback.")
            postback_action(data)
            return ""

        # If the 'message' key exists it's an inbound message from a user.
        if "message" in messaging_events[0]:


            ###
            ### Check for a quick reply payload
            ###
            if "quick_reply" in messaging_events[0]["message"]:
                # Handle the quick reply payload
                postback_action(data)
                return ""
            else:
                print("User typed a message.")



            # Parse user and message information from incoming POST
            sender = messaging_events[0]['sender']['id']
            recipient = messaging_events[0]['recipient']['id']
            message_timestamp = messaging_events[0]['timestamp']
            message_content = messaging_events[0]['message']['text'].encode("utf-8")

            ###
            ### Check if the user intends to leave a message for the artist.
            ###
            firebase_url = "https://hans-artist.firebaseio.com/users/" + sender + ".json?auth=" + firebase_credential
            r = requests.get(firebase_url)
            user = r.json()
            send_next_message_to_human = user["send_next_message_to_human"]
            if send_next_message_to_human == "true":
                print("Sending next message to a human!!!")
                # Twilio to slack
                twilio_to_slack(sender, message_content)
                msg = SendMessage(sender)
                msg.send_message("OK, we'll pass your message along!")
                # Set send_next_message_to_human to false
                firebase_payload = {
                    "send_next_message_to_human" : "false"
                }
                r = requests.patch(firebase_url, data=json.dumps(firebase_payload))



            else:
                # msg = SendMessage(sender)
                # msg.send_message("try something different")
                                # Query API.AI
                isAdmin = False
                apiai_response = apiai_query(message_content, sender, messenger_url, MESSENGER_ACCESS_TOKEN, ai, isAdmin)
                # Store the message to firebase.

                # Query API.AI
                #apiai_response = apiai_query(message_content, sender, messenger_url, messenger_access_token, ai)
                # Store the message to firebase.

                firebase_url = "https://hans-artist.firebaseio.com/adminmessages.json?auth=" + firebase_credential

                # sender, message, timestamp
                firebase_payload = {
                    "sender": sender,
                    "message_content": message_content,
                    "timestamp": time.time()
                }
                r = requests.post(firebase_url, data=json.dumps(firebase_payload))


            # try:
            #     if "quick_reply" in messaging_events[0]['message']:
            #         quick_reply = messaging_events[0]['message']['quick_reply']['payload']
            #         if quick_reply == 'admin_quick_reply':
            #             print("keep goign with this")

            # except Exception as e:
            #     print("couldnt quick reply" + str(e))



            # # Query API.AI
            # apiai_response = apiai_query(message_content, sender, messenger_url, messenger_access_token, ai)
            # # Store the message to firebase.
            # firebase_url = "https://dam-test-767c3.firebaseio.com/inbound.json?auth=" + firebase_token

            # # sender, message, timestamp
            # firebase_payload = {
            #     "sender": sender,
            #     "message_content": message_content,
            #     "timestamp": time.time()
            # }
            # r = requests.post(firebase_url, data=json.dumps(firebase_payload))

    except Exception as e:
        print("Exception: " + str(e))


def twilio_to_slack(sender, message):
    try:
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
    except Exception as e:
        print("Slack exception", str(e))

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






def user_home(sender):
    print("Displaying user_home")
    message_data = {
        "recipient": {"id":sender},
        "message":{
            "text": "Choose from the following:",
            "quick_replies":[
                {
                "content_type": "text",
                "title": "Connect",
                "payload": "user_connect"
                }, {
                "content_type": "text",
                "title": "Listen",
                "payload": "user_listen"
                }, {
                "content_type": "text",
                "title": "Watch",
                "payload": "user_watch"
                }, {
                "content_type":"text",
                "title": "Shop",
                "payload":"user_shop"
                }, {
                "content_type": "text",
                "title": "Settings",
                "payload": "user_settings"
                }
            ]
        }
    }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + str(fb_token), json=message_data)
    print(r.json())

def user_home(sender):
    print("Displaying user_home")
    message_data = {
        "recipient": {"id":sender},
        "message":{
            "text": "Choose from the following:",
            "quick_replies":[
                {
                "content_type": "text",
                "title": "Connect",
                "payload": "user_connect"
                }, {
                "content_type": "text",
                "title": "Listen",
                "payload": "user_listen"
                }, {
                "content_type": "text",
                "title": "Watch",
                "payload": "user_watch"
                }, {
                "content_type":"text",
                "title": "Shop",
                "payload":"user_shop"
                }, {
                "content_type": "text",
                "title": "Settings",
                "payload": "user_settings"
                }
            ]
        }
    }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + str(fb_token), json=message_data)
    print(r.json())
