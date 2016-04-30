import json
from datetime import datetime
import logger
import re

# Parses message string
# returns the remindee, date and text of reminder
def parse_text(j):
    string = get_text(j)
    if string is None:
        logger.log("Failed to get text.")
        return None
    string = string.lower()
    # "Remind <userid> on <23 May 2016 14:03> of <text>"
    p = re.compile(r'(?i)remind ([^ ]+) on (.+) of (.+)')
    m = p.match(string)

    info = dict()

    if m:
        mg = m.groups()
        try:
            info["date"] = datetime.strptime(mg[1], "%d %B %Y %H:%M") # <23 May 2016 14:03>
        except:
            # cannot parse date format so assume remind now
            info["date"] = datetime.now()
        info["remindee"] = int(mg[0])            
        info["text"] = mg[2]
        return info
    else:
        return None 
"""
=======
INFO_SOURCE_USER_ID = "source_userid"
INFO_DEST_USER_ID = "dest_userid"
INFO_TEXT = "text"
INFO_TIME = "time"
>>>>>>> ac4e472b424c373b2213d55d84eb62ec6401899c
"""

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

"""
# Parses message string
# returns the remindee, date and text of reminder
def parse_msg(j):
    string = get_message_text(j)
    # "Remind <userid> on <23 May 2016 14:03> of <text>"
    p = re.compile(r'(?i)remind ([^ ]+) on (.+) of (.+)')
    m = p.match(string)

    info = dict()

    if m:
        mg = m.groups()
        
        info[INFO_DEST_USER_ID] = mg[0]            
        info[INFO_TEXT] = mg[2]
        info[INFO_SOURCE_USER_ID] = get_source_user_id(j)
        try:
            info[INFO_TIME] = datetime.strptime(mg[1], "%d %B %Y %H:%M") # <23 May 2016 14:03>
        except:
            # cannot parse date format so assume remind now
            info[INFO_TIME] = datetime.datetime.now()
        return info
    else:
        print "no match!"
"""

# returns JSON object ready to send to Messenger API
def construct_json_message(recipient, text):
    j = { 
        "recipient":{ 
            "id": recipient 
        }, 
        "message":{
            "text": text
        }
    }
    return json.dumps(j)
