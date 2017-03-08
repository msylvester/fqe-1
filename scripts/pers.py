import json
import os
import requests
import sys

'''
Persistent Menu
- Supports up to 5 buttons.
'''

messenger_access_token = "EAAY7kZCugvrYBAILXdGlMCyQqtcm7dUgvjJ2riu5Ctbo3ZAWugm2ZAfzzNn8fddPPuOlq7QOZBHZB7LY7LRCP0yCzz1tUQR53QP2CdsmPKeyhu9CGXfhBBmyPZCzPZC9siR8Rc9jtojSuUgcmAO4qpoCosWVU0kRVK41oHzyvZA2JwZDZD"
messenger_root_url = "https://graph.facebook.com/v2.6/me/thread_settings?access_token="
messenger_url = messenger_root_url + messenger_access_token

payload = {
    "setting_type": "call_to_actions",
    "thread_state": "existing_thread",
    "call_to_actions":[
        {
        "type":"postback",
        "title":"Home",
        "payload":"user_home"
        },
        {
        "type":"postback",
        "title":"Connect",
        "payload":"user_connect"
        },
        {
        "type":"postback",
        "title":"Settings",
        "payload":"user_settings"
        }
    ]
}

r = requests.post(messenger_url, json=json.loads(json.dumps(payload)))
print("persistent menu " + str(r))
print(r.json())

##
## Uncomment to remove Persistent Menu
##

# payload = {
#     "setting_type":"call_to_actions",
#     "thread_state":"existing_thread"
# }

# r = requests.delete(messenger_url, json=json.loads(json.dumps(payload)))
# print("persistent menu " + str(r))
# print(r.json())

##
## Uncomment to remove Persistent Menu
##

# payload = {
#     "setting_type":"call_to_actions",
#     "thread_state":"existing_thread"
# }

# r = requests.post(messenger_url, json=json.loads(json.dumps(payload)))
# print("persistent menu " + str(r))
# print(r.json())
