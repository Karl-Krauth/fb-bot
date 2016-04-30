import json
from datetime import datetime

# Parses message string
# returns the remindee, date and text of reminder
def parseText(string):
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
            info["date"] = datetime.datetime.now()
        info["remindee"] = mg[0]            
        info["text"] = mg[2]
        return info
    else:
        print "no match!"

# Takes in json from Messenger API
# returns user ID of sendee
def getUserId(j):
    extracted = json.loads(j)
    try:
        userId = extracted["entry"][0]["messaging"][0]["sender"]["id"]
    except:
        print "Unexpected json format: %s" % extracted
    else:
        return userId

# Takes in json from Messenger API
# returns body text of message
def getText(j):
    extracted = json.loads(j)
    try:
        text = extracted["entry"][0]["messaging"][0]["message"]["text"]
    except:
        print "Unexpected json format %" % extracted
    else:
        return text

# returns JSON object ready to send to Messenger API
def constructJsonMessage(recipient, text):
    j = { 
        "recipient":{ 
            "id": recipient 
        }, 
        "message":{
            "text": text
        }
    }
    return json.dumps(j)