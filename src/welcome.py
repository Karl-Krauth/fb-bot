import urllib2
import credentials
import json

def run_welcome_message():
    url = ("https://graph.facebook.com/v2.6/%d/thread_settings?access_token=%s" % (credentials.page_id, credentials.access_token))
    data = json.dumps({
      "setting_type":"call_to_actions",
      "thread_state":"new_thread",
      "call_to_actions":[
        {
          "message":{
            "attachment":{
              "type":"template",
              "payload":{
                "template_type":"generic",
                "elements":[
                  {
                    "title":"Let's get started. Copy & paste the text:",
                    "image_url":"http://puu.sh/oBuqA/29b203a8b7.png",
                    "subtitle":"Remind John Doe on 12 April 2010 11:14 to pay me back for lunch"
                  }
                ]
              }
            }
          }
        }
      ]
    })
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    response = urllib2.urlopen(req)
    print "hello"
    return response.read()
