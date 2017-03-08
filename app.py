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



        payload = {'recipient': {'id': sender}, 'message': {"text": "hey"}} # We're going to send this back
        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
   
        payload = {'recipient': {'id': sender}, 'message': {"text": "data"}} # We're going to send this back
        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
   


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



FB_TOKEN = fbToken

# send message fields
RECIPIENT_FIELD = 'recipient'
MESSAGE_FIELD = 'message'
ATTACHMENT_FIELD = 'attachment'
TYPE_FIELD = 'type'
TEMPLATE_TYPE_FIELD = 'template_type'
TEXT_FIELD = 'text'
TITLE_FIELD = 'title'
SUBTITLE_FIELD = 'subtitle'
IMAGE_FIELD = 'image_url'
BUTTONS_FIELD = 'buttons'
PAYLOAD_FIELD = 'payload'
URL_FIELD = 'url'
ELEMENTS_FIELD = 'elements'


class SendMessage:
    def __init__(self, recipient_id):
        #super().__init__()
        #self.receipient_type = Recipient.ID
        self.receipient_value = recipient_id
        self.message_data = None




    def getID(self):
        #receipient_value
        return self.receipient_value


    def send_message(self, message):

        if self.receipient_value is None:
            print("Please set the recipient!")
            return
        payload = {'recipient': {'id': self.receipient_value}, 'message': {"text": message}} # We're going to send this back
        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + FB_TOKEN, json=payload)
       

#send_image:  sends an image to the user
#-paramters: image is a string, a url to the image 
#-complecity: O(1)
#-returns: void 


# curl -X POST -H "Content-Type: application/json" -d '{
#   "recipient":{
#     "id":"USER_ID"
#   },
#   "message":{
#     "attachment":{
#       "type":"image",
#       "payload":{
#         "url":"https://petersapparel.com/img/shirt.png"
#       }
#     }
#   }
# }' "https://graph.facebook.com/v2.6/me/messages?access_token=PAGE_ACCESS_TOKEN"   


    def send_image(self, image):

        if self.receipient_value is None:
          print("Please set the recipient!")
          return
        if image is None:
          print("there needs to be a url")
          return
        #TODO: use regex to verfiy image is in the form of a url with .jpg or .png as a tariler
        #make sure you have a url 

        payload =  {'recipient': {'id': self.receipient_value}, "message":{ 'attachment':{ 'type':'image', 'payload':{ 'url':image}}}}
        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + fbToken, json=payload)
        return

#send_carousel:  creates a carousel
#parameters: element_list is an array of elements

    def send_carousel(self, element_list):
        print("I am in carousel")
        #create json of element
        part_nums = []

        #poplulate part_nums
        try:
          for element in element_list:
            part_nums.append({'title':str(element.getTitle()), 'image_url':str(element.getImageUrl()), 'subtitle':str(element.getSubTitle()), 'buttons': element.button_list_to_array()})
        except Exception as e:
            print(e)

        bomb = {
           'recipient' : {'id': str(self.receipient_value)},
           'message' : {'attachment': {'type': 'template', 'payload': {'template_type': 'generic', 'elements': part_nums}}},


        }

        json_data = json.dumps(bomb)
        parsed_json  = json.loads(json_data)
        #r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + FB_TOKEN, json=json_data)
        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + FB_TOKEN, json=parsed_json)

        print("**********")
        print(json_data)
        print("**********")



        return

    #TODO: generics messages


    #sends a structured message with buttons, but not a scroll/view
    #send_buttons:  returns a sturcuted message with len(button_list) number of buttons
    #message = title of structured message
    #button_list = array of buttons
    #returns void, but posts to fb

    def send_buttons(self, message, button_list):

        part_nums = []
        counter = 0

        try:
            for button in button_list:
                counter += 1

                if button.getURL() == True:

                  part_nums.append({'type':'web_url', 'url': str(button.getPayload()), 'title': str(button.getTitle())})
                else:
                  part_nums.append({'type':str(button.getType()), 'title': str(button.getTitle()), 'payload': str(button.getPayload())})

                  #jase = json.dumps(part_nums)

            bomb = {
               'recipient' : {'id': str(self.receipient_value)},
               'message' : {'attachment': {'type': 'template', 'payload': {'template_type': 'button', 'text': str(message), 'buttons': part_nums}}},

            }


            json_data = json.dumps(bomb)
            parsed_json  = json.loads(json_data)
            #r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + FB_TOKEN, json=json_data)
            r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + FB_TOKEN, json=parsed_json)

            print("**********")
            print(json_data)
            print("**********")


        except Exception as e:

            print(e)


        return

    #TODO: generics messages

#class element creates an object of type element which is defined in the facebook messenger api
#https://developers.facebook.com/docs/messenger-platform/send-api-reference


class Element:

    def __init__(self, title, image_url, subtitle, button_list):
      print("I am in element")
      self.title = title
      self.image_url = image_url
      self.subtitle = subtitle
      self.button_list = button_list


    def getTitle(self):
      return self.title

    def getImageUrl(self):
      return self.image_url

    def getSubTitle(self):

      return self.subtitle

    def getButtonList(self):

      return self.button_list

    #button_list_to_array: returns the buttons as an array of json
    #parts_num, array of buttons in json form
    def button_list_to_array(self):

      part_nums = []
      print("******button list****")
      print(len(self.button_list))
      for button in self.button_list:


        if button.getURL() == True:
          part_nums.append({'type':'web_url', 'url': str(button.getPayload()), 'title': str(button.getTitle())})
        else:
          part_nums.append({'type':str(button.getType()), 'title': str(button.getTitle()), 'payload': str(button.getPayload())})


      return part_nums

class Button:

    def __init__(self, btnType, title, payload, url):

        print("I am in button")
        #payload or web_url
        self.type = btnType

        #name of button
        self.title = title

        #assign either payload or a url
        if url == "":
            self.payload = payload
            self.isURL = False
        else:
            self.payload = url
            self.isURL = True

    def getType(self):
        return self.type
    def getTitle(self):
        return self.title
    def getPayload(self):
        return self.payload
    def getURL(self):
        return self.isURL

