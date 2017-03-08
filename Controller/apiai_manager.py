#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file contains the primary function and helper methods for interfacing with API.AI

import requests
import json
import emoji

from Controller.message import Button, SendMessage, Element

from Controller.message import Button, SendMessage, Element
from Model.Location import *
from Controller.postbacks import *
from View.admin_messages import *
from View.user_messages import *


import os
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

firebase_credential = os.environ.get('FIREBASE_ACCESS_TOKEN')
api_ai_access_token = os.environ.get('API_AI_TOKEN')

#fbToken = os.environ.get('FB_TOKEN')
fbToken = os.environ.get('FB_TOKEN')

def apiai_query(message, sender, username, facebook_url, fbToken, isAdmin):
    try:
        ai = apiai.ApiAI(api_ai_access_token)
        request = ai.text_request()
        request.query = str(message)
        response = request.getresponse()
        data = json.loads(response.read())

        # If the action is incomplete, APIAI needs more information.
        if "actionIncomplete" in data["result"]:
            if data["result"]["actionIncomplete"]: # If the actionIncomplete field is True
                reply = data["result"]["fulfillment"]["speech"]
                return(reply)

        # Is there an action, i.e. did the model identify an intent?
        if "action" in data["result"]:
            action = data["result"]["action"]
            print("action: " + action)

            ###
            ### Based on the identified intent, parse the action field, and respond accordingly.
            ###

            #TODO: get list of restricted items
            #add support for thank you 
            #thanks

            if action == "thanks":
                # Sure, cancel.
                reply = "<Thumbs up emoji>"
                emo = emoji.emojize(':thumbs_up_sign:')
                payload = {'recipient': {'id': sender}, 'message': {'text': emo}}
                r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
                return


            if action == "main_menu":
                #frdm_menu_message(sender, facebook_url)
                if isAdmin == True: 
                    make_broadcast_analytics(sender)
                else:
                    user_home(sender)
                return
            if action == "settings":

                user_settings(sender)
                return 

            if action == "broadcast":
               make_main_quick_reply(sender)

               return 
            if action == "analytics":

                make_main_analytics(sender)
                return 


            if action == "user_listen":
                user_listen(sender)
                return

            if action == "user_watch":
                user_watch(sender)
                return

            if action == "user_shop":
                user_shop(sender)
                return




            #we  need one for main stage
            #we need one for icon stage 
            #we need one for free form stage
            if action == "total_users":
                firebase_url = "https://hans-artist.firebaseio.com/users.json?auth=" + firebase_credential
                r = requests.get(firebase_url)
                users_opted_in = []
                len(list(r.json().items()))
                number_of_users =  len(list(r.json().items()))
                msg = SendMessage(sender)
                msg.send_message("There are currently  " + str(number_of_users) + " users subscribed" )
                return 







            # Domains
            if action == "smalltalk.agent":
                #frdm_help_message(sender, facebook_url)
                #make_help(sender, username)
                reply = "<Thumbs up emoji>"
                emo = emoji.emojize(':thumbs_up_sign:')
                payload = {'recipient': {'id': sender}, 'message': {'text': emo}}
                r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
                return

            if action == "manage.app_menu":
                #frdm_menu_message(sender, facebook_url)
                #make_menu(sender)
                reply = "<Thumbs up emoji>"
                emo = emoji.emojize(':thumbs_up_sign:')
                payload = {'recipient': {'id': sender}, 'message': {'text': emo}}
                r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
                return

            if action == "smalltalk.appraisal":
                # That's great, that's horrible
                #frdm_wrong_message(sender, facebook_url)
                # msg = SendMessage(sender)
                # msg.send_message("Hey, " + str(username) + "!  I didnt catch that response, checkout the menu or type 'human' to speak to guest services")
                # make_menu(sender)
                reply = "<Thumbs up emoji>"
                emo = emoji.emojize(':thumbs_up_sign:')
                payload = {'recipient': {'id': sender}, 'message': {'text': emo}}
                r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)

                return

            if action == "smalltalk.confirmation":
                # Sure, cancel.
                reply = "<Thumbs up emoji>"
                emo = emoji.emojize(':thumbs_up_sign:')
                payload = {'recipient': {'id': sender}, 'message': {'text': emo}}
                r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
                return

            if action == "smalltalk.dialog":
                # Give me a second, tell me a secret.
                #frdm_wrong_message(sender, facebook_url)
                # msg = SendMessage(sender)
                # msg.send_message("Hey, " + str(username) + "!  I didnt catch that response, checkout the menu or type 'human' to speak to guest services")
                # make_menu(sender)
                reply = "<Thumbs up emoji>"
                emo = emoji.emojize(':thumbs_up_sign:')
                payload = {'recipient': {'id': sender}, 'message': {'text': emo}}
                r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)

                return

            if action == "smalltalk.emotions":
                # Can you become sad?
                # #frdm_wrong_message(sender, facebook_url)
                # msg = SendMessage(sender)
                # msg.send_message("Hey, " + str(username) + "!  I didnt catch that response, checkout the menu or type 'human' to speak to guest services")
                # make_menu(sender)
                reply = "<Thumbs up emoji>"
                emo = emoji.emojize(':thumbs_up_sign:')
                payload = {'recipient': {'id': sender}, 'message': {'text': emo}}
                r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
                return

            if action == "smalltalk.greetings":
                # See you later, what's up?
               #frdm_learn_more_message(sender, facebook_url)
                               #send an open message
               # msg = SendMessage(sender)
                if isAdmin == True: 
                    make_broadcast_analytics(sender)
                else:
                    user_home(sender)
                return

            if action == "smalltalk.person":
                # How old are you?
                # #frdm_wrong_message(sender, facebook_url)
                # msg = SendMessage(sender)
                # msg.send_message("Hey, " + str(username) + "!  I didnt catch that response, checkout the menu or type 'human' to speak to guest services")
                # make_menu(sender)
                reply = "<Thumbs up emoji>"
                emo = emoji.emojize(':thumbs_up_sign:')
                payload = {'recipient': {'id': sender}, 'message': {'text': emo}}
                return

            if action == "smalltalk.topics":
                # # I like kayaking.
                # msg = SendMessage(sender)
                # msg.send_message("Hey, " + str(username) + "!  I didnt catch that response, checkout the menu or type 'human' to speak to guest services")
                # make_menu(sender)
                reply = "<Thumbs up emoji>"
                emo = emoji.emojize(':thumbs_up_sign:')
                payload = {'recipient': {'id': sender}, 'message': {'text': emo}}
                return

            if action == "smalltalk.unknown":
                #frdm_learn_more_message(sender, facebook_url)
                #make_menu(sender)
                # msg = SendMessage(sender)
                # msg.send_message("Hey, " + str(username) + "!  I didnt catch that response, checkout the menu or type 'human' to speak to guest services")
                # make_menu(sender)
                # reply = "<Thumbs up emoji>"
                # emo = emoji.emojize(':thumbs_up_sign:')
                # payload = {'recipient': {'id': sender}, 'message': {'text': emo}}

                msg = SendMessage(sender)
                msg.send_message("hey didnt catch that, let me know")

                return


            if action == "smalltalk.user":
                # I really like you, I trust you, I'll be right back.
                # reply = "<Thumbs up emoji>"
                # emo = emoji.emojize(':thumbs_up_sign:')
                # payload = {'recipient': {'id': sender}, 'message': {'text': emo}}
                # r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
                # msg = SendMessage(sender)
                # msg.send_message("Hey, " + str(username) + "!  I didnt catch that response, checkout the menu or type 'human' to speak to guest services")
                # make_menu(sender)
                reply = "<Thumbs up emoji>"
                emo = emoji.emojize(':thumbs_up_sign:')
                payload = {'recipient': {'id': sender}, 'message': {'text': emo}}              
                return

        else:
            print("Null-state return.")
            msg = SendMessage(sender)
            msg.send_message("Hey, " + str(username) + "!  I didnt catch that response, but hit menu to see the options")
            make_menu(sender)
            #frdm_wrong_message(sender, facebook_url)

            return
    except Exception as e:
        print("Exception: " + str(e))


def getUser(sender):
    try:
        r = requests.get("https://graph.facebook.com/v2.6/"+ str(sender) + "?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=" +str(fbToken))
        obj = r.json()['first_name']
        return obj
    except Exception as e:
        print("Could not find name: " + str(e))
