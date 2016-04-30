import json
from datetime import datetime, timedelta
import logger
import re

INFO_SOURCE_USER_ID = "source_user_id"
INFO_DEST_FIRST_NAME = "dest_first_name"
INFO_DEST_LAST_NAME = "dest_last_name"
INFO_TEXT = "text"
INFO_TIME = "time"

# Parses message string
# returns the remindee, date and text of reminder
def parse_msg(j):
    string = get_message_text(j)
    # "Remind <userid> on <23 May 2016 14:03> to <text>"
    p1 = re.compile(r'(?i)remind ([^ ]+) ([^ ]+) on (.+) to (.+)')
    # "Remind <userid> in <12 minutes> to <text>"
    p2 = re.compile(r'(?i)remind ([^ ]+) ([^ ]+) in ([0-9]+) (seconds|minutes|hours) to (.+)')
    m1 = p1.match(string)
    m2 = p2.match(string)

    info = dict()

    if m1:
        mg = m1.groups()
        
        info[INFO_DEST_FIRST_NAME] = mg[0]
        info[INFO_DEST_LAST_NAME] = mg[1]
        info[INFO_TEXT] = mg[3]
        info[INFO_SOURCE_USER_ID] = get_source_user_id(j)
        try:
            info[INFO_TIME] = datetime.strptime(mg[2], "%d %B %Y %H:%M") # <23 May 2016 14:03>
        except:
            # cannot parse date format so assume remind now
            info[INFO_TIME] = datetime.now()
        return info
    elif m2:
        mg = m2.groups()

        info[INFO_DEST_FIRST_NAME] = mg[0]
        info[INFO_DEST_LAST_NAME] = mg[1]
        info[INFO_TEXT] = mg[4]
        info[INFO_SOURCE_USER_ID] = get_source_user_id(j)
        info[INFO_TIME] = datetime.now()
        amount = int(mg[2])
        if mg[3] == "seconds":
            info[INFO_TIME] += timedelta(seconds=amount)
        elif mg[3] == "minutes":
            info[INFO_TIME] += timedelta(minutes=amount)
        elif mg[3] == "hours":
            info[INFO_TIME] += timedelta(hours=amount)

        return info
    else:
        print "no match!"
        return None

# Takes in json from Messenger API
# returns user ID of sender
def get_source_user_id(j):
    extracted = json.loads(j)
    try:
        userId = extracted["entry"][0]["messaging"][0]["sender"]["id"]
    except:
        return None

    return userId

# Takes in json from Messenger API
# returns body text of message
def get_message_text(j):
    extracted = json.loads(j)
    try:
        text = extracted["entry"][0]["messaging"][0]["message"]["text"]
    except:
        return None

    return text
