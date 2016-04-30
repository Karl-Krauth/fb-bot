import json
import urllib2

import credentials
import logger

def send_reminder(dest_userid, source_userid, text):
    logger.log("%d %d %s" % (source_userid, dest_userid, text))
    message = ("Hi %d, %d asked me to remind you that: '%s'" %
               (dest_userid, source_userid, text))
    return send_chat_message(dest_userid, message)

def send_chat_message(dest_userid, message):
    logger.log("Sending '%s' to %d" % (message, dest_userid))
    url = ("https://graph.facebook.com/v2.6/me/messages?access_token=" +
           credentials.access_token)
    data = json.dumps({
        "recipient": {"id": dest_userid},
        "message": {"text": message}})
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    response = urllib2.urlopen(req)
    return response.read()
