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

# Takes in json from Messenger API
# returns user ID of sender
def get_sender_user_id(j):
    extracted = json.loads(j)
    try:
        userId = extracted["entry"][0]["messaging"][0]["sender"]["id"]
    except:
        return None

    return userId

# Takes in json from Messenger API
# returns body text of message
def get_text(j):
    extracted = json.loads(j)
    try:
        text = extracted["entry"][0]["messaging"][0]["message"]["text"]
    except:
        return None

    return text

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
