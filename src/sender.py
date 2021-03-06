import json
import urllib2
import json

import credentials
import logger
import model

# calls Facebook API to get first & second name by user id
def get_user_info(id):
    url = "https://graph.facebook.com/v2.6/%s?fields=first_name,last_name&access_token=%s" % (id, credentials.access_token)
    res = json.loads(urllib2.urlopen(url).read())
    if ("first_name" in res) and ("last_name" in res):
        return {"first_name": res["first_name"], "last_name": res["last_name"]}
    else:
        print "Cannot get user info of user id %s" % id

def send_reminder(dest_userid, group_name, source_userid, text):
    if group_name != "":
        g = model.Group.query().filter(group_name == model.Group.group_name).get()
        if g is None:
            return None
        for sub in g.subscribers:
            send_reminder(sub, "", source_userid, text)
        return

    dest_user = model.Users.get_by_id(dest_userid)
    if dest_user is None:
        return None

    source_user = model.Users.get_by_id(source_userid)
    if source_user is None:
        return None

    url = ("https://graph.facebook.com/v2.6/me/messages?access_token=" +
           credentials.access_token)
    data = json.dumps({
    "recipient": {"id": dest_userid},
    "message": {
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"generic",
            "elements":[
              {
                "title":"Hi %s, you have a reminder!" % (dest_user.first_name.title()),
                "image_url":"http://puu.sh/oB7DO/530537c5d2.png",
                "subtitle":"%s would like to remind you to %s" % (source_user.first_name.title(), text),
              }
            ]
          }
        }
      }})
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    response = urllib2.urlopen(req)
    return response.read()

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
