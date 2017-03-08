##!/usr/bin/env python
# -*- coding: utf-8 -*-

#this file posts to fb

import requests
import json
import emoji
import os

from Controller.message import Button, SendMessage, Element



fbToken = os.environ.get('FB_TOKEN')
#broadcast quick reply


def make_broadcast_analytics(sender):

	print("****tinside echos")
	message_content = ""
	messageData = {
	"recipient":{
		    "id":sender
		  },
		  "message":{
		    "text":"Who would you like to do?",
		    "quick_replies":[
		      {
		        "content_type":"text",
		        "title":"Broadcast",
		        "payload":"make_main_broadcast"
		      },
		      {
		        "content_type":"text",
		        "title":"Analytics",
		        "payload":"make_main_analytics"
		      }

		    ]
		  }
		} 
	r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + str(fbToken), json=messageData)

def make_main_analytics(sender):

	print("****tinside echos")
	message_content = ""
	messageData = {
	"recipient":{
		    "id":sender
		  },
		  "message":{
		    "text":"What type of analytics would you like?",
		    "quick_replies":[
		      {


		        "content_type":"text",
		        "title":"# of subscribers",
		        "payload":"make_number_subscribers"
		      },
		      {
		        "content_type":"text",
		        "title":"# of total users",
		        "payload":"make_number_users"
		      }

		    ]
		  }
		} 
	r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + str(fbToken), json=messageData)




def make_main_quick_reply(sender):

	print("****tinside echos")
	message_content = ""
	messageData = {
	"recipient":{
		    "id":sender
		  },
		  "message":{
		    "text":"Who would you like to broadcast to?",
		    "quick_replies":[
		      {
		        "content_type":"text",
		        "title":"Everyone",
		        "payload":"make_main_everyone"
		      },
		      {
		        "content_type":"text",
		        "title":"Local",
		        "payload":"make_main_local"
		      },
		      {
		        "content_type":"text",
		        "title":"Specific",
		        "payload":"make_main_specific"
		      },
		      {
		        "content_type":"text",
		        "title":"Checked-In",
		        "payload":"make_main_checked_in"
		      }

		    ]
		  }
		} 
	r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + str(fbToken), json=messageData)



def show_quick_reply(sender):


	print("****tinside quick reply for show")
	message_content = ""
	messageData = {
	"recipient":{
		    "id":sender
		  },
		  "message":{
		    "text":"What show are you inquiring about?",
		    "quick_replies":[
		      {
		        "content_type":"",
		        "title":"07/30/2016",
		        "payload":"make_show_one"
		      },
		      {
		        "content_type":"text",
		        "title":"08/01/2016",
		        "payload":"make_show_two"
		      },
		      {
		        "content_type":"text",
		        "title":"08/15/2016",
		        "payload":"make_show_three"
		      }

		    ]
		  }
		} 
	r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + str(fbToken), json=messageData)


def message_type_quick_reply(sender):


	print("****inside message for text video or image")
	message_content = ""
	messageData = {
	"recipient":{
		    "id":sender
		  },
		  "message":{
		    "text":"Please select:",
		    "quick_replies":[
		      {
		        "content_type":"text",
		        "title":"Text",
		        "payload":"text_quick_reply"
		      },
		      {
		        "content_type":"text",
		        "title":"Photo",
		        "payload":"photo_quick_reply"
		      },
		      {
		        "content_type":"text",
		        "title":"Video",
		        "payload":"video_quick_reply"
		      }

		    ]
		  }
		} 
	r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + str(fbToken), json=messageData)


def city_state_quick_reply(sender):


	print("****inside message for text video or image")
	message_content = ""
	messageData = {
	"recipient":{
		    "id":sender
		  },
		  "message":{
		    "text":"Search by City or State?",
		    "quick_replies":[
		      {
		        "content_type":"text",
		        "title":"City",
		        "payload":"city_quick_reply"
		      },
		      {
		        "content_type":"text",
		        "title":"State",
		        "payload":"state_quick_reply	"
		      }

		    ]
		  }
		} 
	r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + str(fbToken), json=messageData)




