from slacker import Slacker
import json
from datetime import timedelta, datetime

slack = Slacker('xoxp-28044674112-27990941411-30299723268-9c385b8d6a')
too_old = datetime.now() - timedelta(minutes=5)

# get all the channels
try:
    all_channels = slack.channels.list()
    json_dump = json.dumps(all_channels.body)
    parsed_json = json.loads(json_dump)
    channels = parsed_json["channels"]
except:
    print("Slack couldn't be reached.")
    channels = []

# get last messages from each channel
for channel in channels:
    channel_id = channel['id']
    channel_name = channel['name']
    print(channel_name)
    channel_is_archived = channel['is_archived']
    channel_history = slack.channels.history(channel=channel_id, count=1, inclusive=1)
    json_dump = json.dumps(channel_history.body)
    parsed_json = json.loads(json_dump)
    message = parsed_json['messages'][0]
    text = message['text']
    ts = float(message['ts'])
    last_message_ts = datetime.fromtimestamp(ts)

    if last_message_ts < too_old and channel_is_archived == False and channel_name != "general" and channel_name != "random":
        # if the last message is >120 minutes old, archive
        # if you try to archive an already archived channel, you will get an error
        print(channel_name)
        print("^^ was more than 120 minutes old, and archived thusly.")
        slack.channels.archive(channel_id)
    else:
        print("Nothing needed to be archived.")
