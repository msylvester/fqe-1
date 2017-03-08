import json
import requests
from Controller.message import *

###
### Properties
###
fb_token = os.environ.get('FB_TOKEN')
# Firebase credendtial for https://hans-artist.firebaseio.com/
firebase_credential = os.environ.get('FIREBASE_ACCESS_TOKEN')
firebase_root_url = "https://hans-artist.firebaseio.com/"

###
### Messages
###

'''
Main Menu
- Quick replies: connect, listen, watch, shop, settings
'''
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


def dummy_response(sender):
    msg = SendMessage(sender)
    msg.send_message("Thank you for using our service!")

def user_connect(sender):
    print("Displaying user_connect")
    message_data = {
        "recipient": {"id":sender},
        "message":{
            "text": "Choose from the following:",
            "quick_replies":[
                {
                "content_type": "text",
                "title": "Schedule",
                "payload": "user_connect_schedule"
                }, {
                "content_type": "text",
                "title": "Leave a Message",
                "payload": "user_connect_message"
                }
            ]
        }
    }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + str(fb_token), json=message_data)
    print(r.json())

def user_connect_schedule(sender):
    print("Displaying user_connect_schedule")
    message_data = {
        "recipient": {"id":sender},
        "message":{
            "text": "Choose from the following:",
            "quick_replies":[
                {
                "content_type": "text",
                "title": "Show 1",
                "payload": "dummy_response"
                }, {
                "content_type": "text",
                "title": "Show 2",
                "payload": "dummy_response"
                }, {
                "content_type": "text",
                "title": "Show 3",
                "payload": "dummy_response"
                }
            ]
        }
    }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + str(fb_token), json=message_data)
    print(r.json())


def user_connect_message(sender):
    print("Displaying user_connect_message")
    msg = SendMessage(sender)
    msg.send_message("Type your message and hit send and we will pass it along to Aoki.")
    # Set firebase property
    firebase_url = "https://hans-artist.firebaseio.com/users/" + sender + ".json?auth=" + firebase_credential
    firebase_payload = {
        "send_next_message_to_human" : "true"
    }
    r = requests.patch(firebase_url, data=json.dumps(firebase_payload))


def user_listen(sender):
    print("Displaying user_listen")
    message_data = {
        "recipient": {"id":sender},
        "message":{
            "text": "Choose from the following:",
            "quick_replies":[
                {
                "content_type": "text",
                "title": "New Single",
                "payload": "dummy_response"
                }, {
                "content_type": "text",
                "title": "Album",
                "payload": "dummy_response"
                }, {
                "content_type": "text",
                "title": "Friends",
                "payload": "dummy_response"
                }
            ]
        }
    }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + str(fb_token), json=message_data)
    print(r.json())

def user_watch(sender):
    print("Displaying user_watch")
    message_data = {
        "recipient": {"id":sender},
        "message":{
            "text": "Choose from the following:",
            "quick_replies":[
                {
                "content_type": "text",
                "title": "Popular",
                "payload": "dummy_response"
                }, {
                "content_type": "text",
                "title": "Live",
                "payload": "dummy_response"
                }, {
                "content_type": "text",
                "title": "Submit",
                "payload": "dummy_response"
                }
            ]
        }
    }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + str(fb_token), json=message_data)
    print(r.json())

def user_shop(sender):
    print("Displaying user_shop")
    message_data = {
        "recipient": {"id":sender},
        "message":{
            "text": "Choose from the following:",
            "quick_replies":[
                {
                "content_type": "text",
                "title": "Music",
                "payload": "dummy_response"
                }, {
                "content_type": "text",
                "title": "Merchendise",
                "payload": "dummy_response"
                }, {
                "content_type": "text",
                "title": "Favorites",
                "payload": "dummy_response"
                }
            ]
        }
    }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + str(fb_token), json=message_data)
    print(r.json())

def user_settings(sender):
    print("Displaying user_settings")

    # Check firebase for the user's alert settings
    firebase_url = "https://hans-artist.firebaseio.com/users/" + sender + "/alerts.json?auth=" + firebase_credential
    r = requests.get(firebase_url)

    alerts = r.json()
    latest_news = alerts["latest_news"]
    secret_shows = alerts["secret_shows"]
    exclusive_content = alerts["exclusive_content"]

    buttons = []
    msg = SendMessage(sender)
    button_edit_alerts = Button("postback", "Edit Alerts", "user_edit_alerts", "")
    button_about_artist = Button("postback", "About Artist", "dummy_response", "")
    buttons.append(button_edit_alerts)
    buttons.append(button_about_artist)
    message_text = (
        'Turn alerts on or off here. \n\n'
        'Alerts: \n'
        'Latest News: ' + latest_news.upper() + ' \n'
        'Secret Shows: ' + secret_shows.upper() + ' \n'
        'Exclusive Content: ' + exclusive_content.upper()
    )
    msg.send_buttons(message_text, buttons)

def user_edit_alerts(sender):
    print("Displaying user_edit_alerts")
    # Check firebase for the user's alert settings
    firebase_url = "https://hans-artist.firebaseio.com/users/" + sender + "/alerts.json?auth=" + firebase_credential
    r = requests.get(firebase_url)

    alerts = r.json()
    latest_news = alerts["latest_news"]
    secret_shows = alerts["secret_shows"]
    exclusive_content = alerts["exclusive_content"]

    # Create gallery
    # Select which alert you want to change.
    reply_message = SendMessage(sender)

    if latest_news == "on":
        latest_news_button = Button("postback", "Stop Latest News", "change_latest_news", "")
    else:
        latest_news_button = Button("postback", "Enable Latest News", "change_latest_news", "")

    latest_news_element = Element("Latest News is " + latest_news, "", "Get the latest news.", [latest_news_button])

    if secret_shows == "on":
        secret_shows_button = Button("postback", "Stop Secret Shows", "change_secret_shows", "")
    else:
        secret_shows_button = Button("postback", "Enable Secret Shows", "change_secret_shows", "")

    secret_shows_element = Element("Secret Shows is " + secret_shows, "", "Get access to secret shows.", [secret_shows_button])

    if exclusive_content == "on":
        exclusive_content_button = Button("postback", "Stop Exclusive Content", "change_exclusive_content", "")
    else:
        exclusive_content_button = Button("postback", "Enable Exclusive Content", "change_exclusive_content", "")

    exclusive_content_element = Element("Exclusive Content is " + exclusive_content, "", "Get exclusive content.", [exclusive_content_button])

    reply_message.send_carousel([latest_news_element, secret_shows_element, exclusive_content_element])


def change_latest_news(sender):
    print("Displaying change_latest_news")

    firebase_url = "https://hans-artist.firebaseio.com/users/" + sender + "/alerts.json?auth=" + firebase_credential
    r = requests.get(firebase_url)
    alerts = r.json()
    latest_news = alerts["latest_news"]

    if latest_news == "on":
        firebase_payload = {
            "latest_news" : "off"
        }
        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))
    else:
        firebase_payload = {
            "latest_news" : "on"
        }
        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))

    msg = SendMessage(sender)
    msg.send_message("OK, got it.")


def change_secret_shows(sender):
    print("Displaying change_secret_shows")

    firebase_url = "https://hans-artist.firebaseio.com/users/" + sender + "/alerts.json?auth=" + firebase_credential
    r = requests.get(firebase_url)
    alerts = r.json()
    secret_shows = alerts["secret_shows"]

    if secret_shows == "on":
        firebase_payload = {
            "secret_shows" : "off"
        }
        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))
    else:
        firebase_payload = {
            "secret_shows" : "on"
        }
        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))

    msg = SendMessage(sender)
    msg.send_message("OK, got it.")

def change_exclusive_content(sender):
    print("Displaying stop_exclusive_content")

    firebase_url = "https://hans-artist.firebaseio.com/users/" + sender + "/alerts.json?auth=" + firebase_credential
    r = requests.get(firebase_url)
    alerts = r.json()
    exclusive_content = alerts["exclusive_content"]

    if exclusive_content == "on":
        firebase_payload = {
            "exclusive_content" : "off"
        }
        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))
    else:
        firebase_payload = {
            "exclusive_content" : "on"
        }
        r = requests.patch(firebase_url, data=json.dumps(firebase_payload))

    msg = SendMessage(sender)
    msg.send_message("OK, got it.")
