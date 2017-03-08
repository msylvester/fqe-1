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
from Controller.admin_postbacks import postback_action

messenger_url = "https://graph.facebook.com/v2.6/me/messages?access_token="
ai = os.environ.get('api_ai_access_token')


firebase_credential = os.environ.get('FIREBASE_ACCESS_TOKEN')

MESSENGER_ACCESS_TOKEN = os.environ.get('FB_TOKEN')

def driver(data):

    try:
        data = json.loads(request.data)
        messaging_events = data['entry'][0]['messaging']
        sender = messaging_events[0]['sender']['id']

        #see if it iss an everyone psotback 




  

        firebase_url = "https://hans-artist.firebaseio.com/admin/" + sender + ".json?auth=" + firebase_credential
        r = requests.get(firebase_url)


        print("***about to print json return from admin driver***")
        print(r.json())




        try: 
            print("gonna check on that image first")
            if r.json()['is_texting_image'] == 'true':    

                sender = messaging_events[0]['sender']['id']
                recipient = messaging_events[0]['recipient']['id']
                message_timestamp = messaging_events[0]['timestamp']

                print("shyo7od see me here")

                if messaging_events[0]["message"]['attachments'][0]['type'] == 'image':
                    #payload = {'recipient': {'id': sender}, 'message': {"text": "We received your image, thanks!"}} # We're going to send this back
                    #r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
                   
                    print("should not see me here")
                    image_url = messaging_events[0]["message"]['attachments'][0]['payload']['url']

                    firebase_url = "https://hans-artist.firebaseio.com/Alert/2.json?auth=" + firebase_credential
                    print("about to ping for real")
                    r = requests.get(firebase_url)
                    print(r.json())

                    message_image = r.json()['image_url']
                    print(message_image)

                    if message_image is None:
                        firebase_payload = {"image_url": image_url}
                        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))
                        print("this nonya worked")
                        msg = SendMessage(sender)
                        btn_confirm_alert = Button("postback", "Ok", "add_text_postback", "")
                        btn_confirm_fail = Button("postback", "No, send it", "send_image_postback", "")
                        msg.send_buttons("Would you like a caption?: ?", [btn_confirm_alert, btn_confirm_fail])
                        return ""

                    else:

                        firebase_payload = {"image_url": image_url}
                        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))
                        print("this nonya worked")
                        msg = SendMessage(sender)
                        btn_confirm_alert = Button("postback", "Ok", "add_text_postback", "")
                        btn_confirm_fail = Button("postback", "No, send it", "send_image_postback", "")
                        msg.send_buttons("Would you like a caption?",  [btn_confirm_alert, btn_confirm_fail])
                        return ""

            else:

                print("yo are locked in")
                # msg = SendMessage(sender)
                # msg.send_message("plese send in a message")
              
        except Exception as e:
            print(e)






        try:
            if r.json()['is_adding_label'] == 'true':
                if "message" in messaging_events[0]:
                    print("User typed a message.")
                    # Parse user and message information from incoming POST
                    sender = messaging_events[0]['sender']['id']
                    recipient = messaging_events[0]['recipient']['id']
                    message_timestamp = messaging_events[0]['timestamp']
                    message_content = messaging_events[0]['message']['text'].encode("utf-8")

                    print("labeling")
                    #writealert 
                    firebase_url = "https://hans-artist.firebaseio.com/Alert/2.json?auth=" + firebase_credential
                    print("about to ping for real")
                    r = requests.get(firebase_url)
                    print(r.json())

                    message_alert = r.json()['message']
                    image_info = r.json()['image_url']
                    print(message_alert)

                    if message_alert is None:
                        firebase_payload = {"message": message_content}
                        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))
                        print("this nonya worked")
                        msg = SendMessage(sender)
                        btn_confirm_alert = Button("postback", "Ok", "confirm_label_image_postback", "")
                        btn_confirm_edit = Button("postback", "Edit", "confirm_edit_postback", "")
                        btn_confirm_fail = Button("postback", "Exit", "exit_postback", "")
                        msg.send_buttons("Can you confirm that you are sending: \n" + str(message_content) + "\n and the picture below?", [btn_confirm_alert, btn_confirm_edit, btn_confirm_fail])

                        payload =  {'recipient': {'id': sender}, "message":{ 'attachment':{ 'type':'image', 'payload':{ 'url':image_info}}}}
                        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
                        return ""

                    else:

                        firebase_payload = {"message": message_content}
                        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))
                        print("this nonya worked")
                        msg = SendMessage(sender)
                        btn_confirm_alert = Button("postback", "Ok", "confirm_label_image_postback", "")
                        btn_confirm_edit = Button("postback", "Edit", "confirm_edit_postback", "")
                        btn_confirm_fail = Button("postback", "Exit", "exit_postback", "")
                        msg.send_buttons("Can you confirm that you are sending: \n" + str(message_content) + "\n and the picture below?", [btn_confirm_alert, btn_confirm_edit, btn_confirm_fail])


                        payload =  {'recipient': {'id': sender}, "message":{ 'attachment':{ 'type':'image', 'payload':{ 'url':image_info}}}}
                        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
                        return ""



                    #image stuff 


            else: 
                print("admin can message whoever")
            


        except Exception as e:
                print(e)

        try:
            if r.json()['is_texting_everyone'] == 'true':
                if "message" in messaging_events[0]:
                    print("User typed a message.")
                    # Parse user and message information from incoming POST
                    sender = messaging_events[0]['sender']['id']
                    recipient = messaging_events[0]['recipient']['id']
                    message_timestamp = messaging_events[0]['timestamp']
                    message_content = messaging_events[0]['message']['text'].encode("utf-8")

                    print("about to ping firebase")
                    #writealert 
                    firebase_url = "https://hans-artist.firebaseio.com/Alert/1.json?auth=" + firebase_credential
                    print("about to ping for real")
                    r = requests.get(firebase_url)
                    print(r.json())

                    message_alert = r.json()['message']
                    print(message_alert)

                    if message_alert is None:
                        firebase_payload = {"message": message_content}
                        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))
                        print("this nonya worked")
                        msg = SendMessage(sender)
                        btn_confirm_alert = Button("postback", "Ok", "confirm_everyone_postback", "")
                        btn_confirm_fail = Button("postback", "Exit", "exit_postback", "")
                        msg.send_buttons("Can you cofirm that you are sending: \n" + str(message_content) + "\n to everone?", [btn_confirm_alert, btn_confirm_fail])
                        return ""

                    else:

                        firebase_payload = {"message": message_content}
                        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))
                        print("this nonya worked")
                        msg = SendMessage(sender)
                        btn_confirm_alert = Button("postback", "Ok", "confirm_everyone_postback", "")
                        btn_confirm_fail = Button("postback", "Exit", "exit_postback", "")
                        msg.send_buttons("Can you cofirm that you are sending: \n" + str(message_content) + "\n to everone?", [btn_confirm_alert, btn_confirm_fail])
                        return ""



                    #image stuff 


            else: 
                print("admin can message whoever")


        except Exception as e:
            print(e)


        if "postback" in messaging_events[0]:
            print("Admin sent a postback.")
            postback_action(data)
            #admin_postbacks(sender)



            return ""

        # If the 'message' key exists it's an inbound message from a user.
        if "message" in messaging_events[0]:
            print("User typed a message.")
            # Parse user and message information from incoming POST
            sender = messaging_events[0]['sender']['id']
            recipient = messaging_events[0]['recipient']['id']
            message_timestamp = messaging_events[0]['timestamp']
            message_content = messaging_events[0]['message']['text'].encode("utf-8")


            #see if user sent an image
            try:
                    #do what we need to do 
                    
                if messaging_events[0]["message"]['attachments'][0]['type'] == 'image':
                    payload = {'recipient': {'id': sender}, 'message': {"text": "We received your image, thanks!"}} # We're going to send this back
                    r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
                    image_url = messaging_events[0]["message"]['attachments'][0]['payload']['url']



            except Exception as e:
                print("caught general exception" + str(e))


            #check to see if it is a location 
            try:

                req = messaging_events[0]['message']['attachments'][0]


                if req['type'] == 'location':

                    location_local = Location(req['title'], req['payload']['coordinates']['long'], req['payload']['coordinates']['lat'], req['url'], messaging_events[0]['timestamp'], messaging_events[0]['recipient']['id'])
                    payload = {'recipient': {'id': sender}, 'message': {"text": "We received your location, thanks! \n" + str(location_local.getLat()) + "\n" + str(location_local.getLong())}} # We're going to send this back
                    r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
                 
            except KeyError as e:
                print("da fuq" + str(e))

            except Exception as e:
                print("caught general excption" + str(e))

            #check for quick replys


            try:
                if "quick_reply" in messaging_events[0]['message']:
                    quick_reply = messaging_events[0]['message']['quick_reply']['payload']



                    print("I(SDFDF")
                    print(quick_reply)
                    if quick_reply == 'make_number_subscribers':
                                    #ask them if they are user or admin
                        #go through and pull out all subscribers to alert 1
                        firebase_url = "https://hans-artist.firebaseio.com/users.json?auth=" + firebase_credential
                        r = requests.get(firebase_url)
                        opted_in = []

                        print(r.json())

                        for k,v in r.json().items():
                            print(k)
                            print(v)
                            if v['alerts']['exclusive_content'] == 'on':
                                opted_in.append(k)

                        if len(opted_in) >= 1:
                            msg = SendMessage(sender)
                            msg.send_message("There are currently  " + str(len(opted_in)) + " users subscribed" )
                
                        else:
                            msg = SendMessage(sender)
                            msg.send_message("There are not currently any users subscribed" )

                    if quick_reply == 'make_number_users':
                                    #ask them if they are user or admin
                        #go through and pull out all subscribers to alert 1
                        firebase_url = "https://hans-artist.firebaseio.com/users.json?auth=" + firebase_credential
                        r = requests.get(firebase_url)
                        users_opted_in = []
                        len(list(r.json().items()))
                        number_of_users =  len(list(r.json().items()))
                        msg = SendMessage(sender)
                        msg.send_message("There are currently  " + str(number_of_users) + " users subscribed" )

                    if quick_reply == 'make_main_broadcast':
                                    #ask them if they are user or admin
                        make_main_quick_reply(sender)

                    if quick_reply == 'make_main_analytics':
                                    #ask them if they are user or admin
                        make_main_analytics(sender)

                    if quick_reply == 'make_main_everyone':
                        message_type_quick_reply(sender)
                        # msg = SendMessage(sender)
                        # btn_one = Button("postback", "ok", "confirm_everyone_quick", "")
                        # msg.send_buttons("Send to everyon?", [btn_one])
                        #make quick replyas
                    if quick_reply == 'make_main_local':
                        # msg = SendMessage(sender)
                        # btn_one = Button("postback", "ok", "confirm_local", "")
                        # msg.send_buttons([btn_one])
                        msg = SendMessage(sender)
                        msg.send_message("please give us your location")

                    if quick_reply == 'make_main_specific':
                        city_staty_quick_reply(sender)
                        #send quick reply 

                    if quick_reply == 'make_main_checked_in':
                        show_quick_reply(sender)
                            

                    if quick_reply == 'make_show_one':
                        #confirm
                        msg = SendMessage(sender)
                        btn_one = Button("postback", "ok", "confirm_show_one", "")
                        msg.send_buttons("Confirm Show One?", [btn_one])

                    if quick_reply == 'make_show_two':
                                    #ask them if they are user or admin
                        msg = SendMessage(sender)
                        btn_one = Button("postback", "ok", "confirm_show_two", "")
                        msg.send_buttons("Confirm Show Two", [btn_one])


                    if quick_reply == 'make_show_three':

                        msg = SendMessage(sender)
                        btn_one = Button("postback", "ok", "confirm_show_three", "")
                        msg.send_buttons("Confirm Show Three", [btn_one])

                    if quick_reply == 'text_quick_reply':
                        # Query Firebase to determine if the message should be routed to a human.
                        try:
                            firebase_url = "https://hans-artist.firebaseio.com/admin/" + sender + ".json?auth=" + firebase_credential
                            r = requests.get(firebase_url)
                            print(r.json())
                            texting_everyone = r.json()['is_texting_everyone']
                            print(texting_everyone)
                            if texting_everyone is None:
                                firebase_payload = {"is_texting_everyone": "true"}
                                r = requests.patch(firebase_url, data=json.dumps(firebase_payload))
                            elif texting_everyone == 'false':
                                firebase_payload = {"is_texting_everyone": "true"}
                                r = requests.patch(firebase_url, data=json.dumps(firebase_payload))
                            else:
                                print("couldnt set admin data")
                        except Exception as e:
                            print("Exception when patching db " + str(e))

                        msg = SendMessage(sender)
                        msg.send_message("Please type in your message")
                    if quick_reply == 'photo_quick_reply':
                         #ask them if they are user or admin

                        try:
                            firebase_url = "https://hans-artist.firebaseio.com/admin/" + sender + ".json?auth=" + firebase_credential
                            r = requests.get(firebase_url)
                            print(r.json())
                            texting_everyone = r.json()['is_texting_image']
                            print(texting_everyone)
                            if texting_everyone is None:
                                firebase_payload = {"is_texting_image": "true"}
                                r = requests.patch(firebase_url, data=json.dumps(firebase_payload))
                            elif texting_everyone == 'false':
                                firebase_payload = {"is_texting_image": "true"}
                                r = requests.patch(firebase_url, data=json.dumps(firebase_payload))
                            else:
                                print("couldnt set admin data")
                        except Exception as e:
                            print("Exception when patching db " + str(e))                        

                        msg = SendMessage(sender)
                        msg.send_message("please send your image")

                    if quick_reply == 'state_quick_reply':
                        msg = SendMessage(sender)
                        msg.send_message("Please enter a city or zip")


                    if quick_reply == 'video_quick_reply':
                        print("hello")
                    #ceheck to see if city/state
                    if quick_reply == 'city_quick_reply':
                        msg = SendMessage(sender)
                        msg.send_message("Please enter a city or zip")
                    
          
                else:

                    message_content = messaging_events[0]['message']['text'].encode("utf-8")
                    print("hey hey ")
                    if message_content == 'hey':
                        make_broadcast_analytics(sender)

                    elif message_content == '$helloKitty':


                        print("up")

                    else:
                        # msg = SendMessage(sender)
                        # msg.send_message("try something different")
                                        # Query API.AI
                        isAdmin = True 
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


                    #change model 

            except Exception as e:
                print("failed in quick reply in admin driver" + str(e)) 

    except Exception as e:
        print(e)


