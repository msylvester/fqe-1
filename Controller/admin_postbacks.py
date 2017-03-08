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
from View.admin_messages import *


firebase_credential = os.environ.get('FIREBASE_ACCESS_TOKEN')
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai
os.environ.get('HUB_VERIFY_TOKEN')


# Flask app configuration
app = Flask(__name__)

def postback_action(data):
    messaging_events = data['entry'][0]['messaging']
    sender = messaging_events[0]['sender']['id']
    payload = messaging_events[0]['postback']['payload']
    print("Payload: " + payload)

    if 'confirm_everyone_quick' in payload:
        #city_state_quick_reply(sender)
        #message_type_quick_reply
       # message_type_quick_reply(sender)
        opted_in = []

        firebase_url = "https://hans-artist.firebaseio.com/users.json?auth=" + firebase_credential
        r = requests.get(firebase_url)
        print("****** printing json *(*** *")
        print(r.json())

        firebase_url = "https://hans-artist.firebaseio.com/admin/" + sender + ".json?auth=" + firebase_credential
        r = requests.get(firebase_url)
        texting_everyone = r.json()['is_texting_everyone']
        print(texting_everyone)
        firebase_payload = {"is_texting_everyone": "true"}
        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))
        msg = SendMessage(sender)
        msg.send_message("enter your message")

        #do something

    #check to se if the are confirming a text message

    if 'confirm_everyone_postback' in payload:

        #get all users, send a messaege
        opted_in = []

        #firebase_url = "https://hans-artist.firebaseio.com/users.json?auth=" + firebase_credential

        firebase_url = "https://hans-artist.firebaseio.com/users.json?auth=" + firebase_credential
        r = requests.get(firebase_url)
        print("****** printing json *(*** *")
        print(r.json())
        is_admin = "false"
        notification = ""
        for k,v in r.json().items():

            if v['alerts']['exclusive_content'] == 'on':
                opted_in.append(k)

                firebase_url_message = "https://hans-artist.firebaseio.com/Alert/1.json?auth=" + firebase_credential
                r_message = requests.get(firebase_url_message)
                print(r_message.json())

                print(r_message.json()['message'])
                notification = r_message.json()['message']
        if len(opted_in) >= 1:
            for a in opted_in:
                msg = SendMessage(a)
                msg.send_message(notification)
            msg = SendMessage(sender)
            msg.send_message("Message has been sent to " + str(len(opted_in)) + " people")
        else:
            msg = SendMessage(sender)
            msg.send_message("No one is opted in for subscriptions")


        firebase_url = "https://hans-artist.firebaseio.com/admin/" + sender + ".json?auth=" + firebase_credential
        r = requests.get(firebase_url)

        texting_everyone = r.json()['is_texting_everyone']
        print(texting_everyone)
        firebase_payload = {"is_texting_everyone": "false"}
        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))

    elif 'confirm_show_one' in payload:
        city_state_quick_reply(sender)

    elif 'confirm_show_one' in payload:
        city_state_quick_reply(sender)


    elif 'confirm_edit_postback' in payload:
        msg = SendMessage(sender)
        msg.send_message("Please re input your message")

    elif 'send_image_postback' in payload:
               #get all users, send a messaege
        opted_in = []

        #firebase_url = "https://hans-artist.firebaseio.com/users.json?auth=" + firebase_credential

        firebase_url = "https://hans-artist.firebaseio.com/users.json?auth=" + firebase_credential
        r = requests.get(firebase_url)
        print("****** printing json *(*** *")
        print(r.json())

        notification = ""
        for k,v in r.json().items():

            if v['alerts']['exclusive_content'] == 'on':
                opted_in.append(k)

                firebase_url_message = "https://hans-artist.firebaseio.com/Alert/2.json?auth=" + firebase_credential
                r_message = requests.get(firebase_url_message)
                print(r_message.json())

                print(r_message.json()['image_url'])
                notification = r_message.json()['image_url']
        if len(opted_in) >= 1:
            for a in opted_in:
                payload =  {'recipient': {'id': a}, "message":{ 'attachment':{ 'type':'image', 'payload':{ 'url':notification}}}}
                r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)

            msg = SendMessage(sender)
            msg.send_message("Message has been sent to " + str(len(opted_in)) + " people")
        else:
            msg = SendMessage(sender)
            msg.send_message("No one is subscribed")


        firebase_url = "https://hans-artist.firebaseio.com/admin/" + sender + ".json?auth=" + firebase_credential
        r = requests.get(firebase_url)
        texting_everyone = r.json()['is_texting_image']
        print(texting_everyone)
        firebase_payload = {"is_texting_image": "false"}
        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))


    elif 'add_text_postback' in payload:

        #change shit


        firebase_url = "https://hans-artist.firebaseio.com/admin/" + sender + ".json?auth=" + firebase_credential
        r = requests.get(firebase_url)
        texting_everyone = r.json()['is_adding_label']
        print(texting_everyone)
        firebase_payload = {"is_adding_label": "true"}
        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))

        msg = SendMessage(sender)
        msg.send_message("Please type your message")

    elif 'confirm_label_image_postback' in payload:
        opted_in = []

        #firebase_url = "https://hans-artist.firebaseio.com/users.json?auth=" + firebase_credential

        firebase_url = "https://hans-artist.firebaseio.com/users.json?auth=" + firebase_credential
        r = requests.get(firebase_url)
        print("****** printing json *(*** *")
        print(r.json())

        notification = ""
        image_info = ""
        image_notification = ""
        print("just bevore dict")

        for k,v in r.json().items():
            print("k")
            print("getting thorugh this")
            print("v")
            print("now printing k ")
            print(k)
            print(v)

            print( v['alerts'])
            print(v['alerts']['exclusive_content'])


            if v['alerts']['exclusive_content'] == 'on':
                opted_in.append(k)

                firebase_url_message = "https://hans-artist.firebaseio.com/Alert/2.json?auth=" + firebase_credential
                r_message = requests.get(firebase_url_message)
                print(r_message.json())

                print(r_message.json()['image_url'])
                image_info = r_message.json()['image_url']
                image_notification = r_message.json()['message']


        print(str(len(opted_in)))
        if len(opted_in) >= 1:
            print("I am in if statement")
            for a in opted_in:
                payload =  {'recipient': {'id': a}, "message":{ 'attachment':{ 'type':'image', 'payload':{ 'url':image_info}}}}
                r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
                msg = SendMessage(sender)
                msg.send_message(image_notification)

                msg = SendMessage(sender)
                msg.send_message("Message has been sent to " + str(len(opted_in)) + " people")



        else:
            print("I am in else statement")
            msg = SendMessage(sender)
            msg.send_message("No one is subscribed")


        firebase_url = "https://hans-artist.firebaseio.com/admin/" + sender + ".json?auth=" + firebase_credential
        r = requests.get(firebase_url)
        print("SFsdfdsf fong a")
        print(r.json())

        texting_everyone = r.json()['is_texting_image']
        print("herere comes ")
        print(texting_everyone)
        firebase_payload = {"is_texting_image": "false"}
        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))


        firebase_url = "https://hans-artist.firebaseio.com/admin/" + sender + ".json?auth=" + firebase_credential

        r = requests.get(firebase_url)

        texting_everyone = r.json()['is_adding_label']

        print(texting_everyone)

        firebase_payload = {"is_adding_label": "false"}
        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))



    elif 'confirm_show_two' in payload:
        city_state_quick_reply(sender)

    elif 'confirm_show_three' in payload:
        city_state_quick_reply(sender)


    elif 'exit_postback' in payload:

        firebase_url = "https://hans-artist.firebaseio.com/admin/" + sender + ".json?auth=" + firebase_credential
        r = requests.get(firebase_url)
        print(r.json())
        texting_everyone = r.json()['is_texting_everyone']
        print(texting_everyone)

        firebase_payload = {"is_texting_everyone": "false",
                            "is_texting_image": "false",
                            "is_adding_label": "false"

            }
        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))





    else:
        print("No matching postback in postbacks.py")
