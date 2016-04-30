import json
from datetime import datetime, timedelta
import logger
import re
import model

INFO_SOURCE_USER_ID = "source_user_id"
INFO_DEST_FIRST_NAME = "dest_first_name"
INFO_DEST_LAST_NAME = "dest_last_name"
INFO_TEXT = "text"
INFO_TIME = "time"

# Parses message string
# returns the remindee, date and text of reminder
def parse_msg(j):
    string = get_message_text(j)
    # "Remind <userid> on <23 May 2016 14:03> of <text>"
    p = re.compile(r'(?i)remind ([^ ]+) ([^ ]+) on (.+) of (.+)')
    m = p.match(string)

    info = dict()

    if m:
        mg = m.groups()
        
        info[INFO_DEST_FIRST_NAME] = mg[0]
        info[INFO_DEST_LAST_NAME] = mg[1]
        info[INFO_TEXT] = mg[3]
        info[INFO_SOURCE_USER_ID] = get_source_user_id(j)
        try:
            info[INFO_TIME] = datetime.strptime(mg[2], "%d %B %Y %H:%M") # <23 May 2016 14:03>
        except:
            # cannot parse date format so assume remind now
            info[INFO_TIME] = datetime.datetime.now()
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

def parse_group_message(source_id, text):
    split_txt = text.split(" ", 6)
    group_name = split_txt[1].lower()
    num = int(split_txt[3])
    msg = split_txt[6]

    g = model.Group.query().filter(model.Group.group_name == group_name).get()
    if g is None:
        g = Group(group_name=group_name)
        g.put()

    r = model.Reminder(reminder_time=datetime.utcnow() + timedelta(minutes=num), text=msg, source_userid=source_id, group_name=group_name)
    r.put() 

def parse_subscribe(source_id, text):
    split_txt = text.split()
    group_name = split_txt[2].lower()
    
    g = model.Group.query().filter(model.Group.group_name == group_name).get()
    if g is None:
        g = model.Group(group_name=group_name)
    
    if not source_id in g.subscribers:
        g.subscribers.append(source_id)

    g.put()
