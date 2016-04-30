#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.api import urlfetch
import logger
import model
import sender
import parse
import credentials

class MainHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.get('hub.verify_token') == 'fiend':
            self.response.write(self.request.get('hub.challenge'))
        else:
            self.response.write('Error, wrong validation token.')
 
    def post(self):
        logger.log(self.request.body)

        msg_data = parse.parse_msg(self.request.body)
        source_user_id = parse.get_source_user_id(self.request.body)
        # if user not in database, add them in
        if not model.Users.get_by_id(source_user_id):
            source_user_info = sender.get_user_info(source_user_id)
            model.Users.add_user(source_user_info["first_name"], source_user_info["last_name"], source_user_id)

        if msg_data is None:
            # TODO: send an error response.
            sender.send_chat_message(source_user_id, "Oh no! I didn't understand your message.")
            return

        # TODO handle invalid name
        # TODO handle multiple matches to name string
        dest_user_id = model.Users.find_by_name(msg_data[parse.INFO_DEST_FIRST_NAME], msg_data[parse.INFO_DEST_LAST_NAME])
        if not dest_user_id:
            sender.send_chat_message(source_user_id, "Oh no! The user's name doesn't exist.")
            return
        dest_user_id = dest_user_id.user_id

        model.Reminder.add_reminder(source_user_id, dest_user_id,
                                    msg_data[parse.INFO_TEXT], msg_data[parse.INFO_TIME])
        sender.send_chat_message(source_user_id, "Ok! I'll be sure to remind %s %s."
                                 % (msg_data[parse.INFO_DEST_FIRST_NAME], msg_data[parse.INFO_DEST_LAST_NAME]) )

class CronHandler(webapp2.RequestHandler):
    def get(self):
        reminders = model.Reminder.get_current_reminders()
        for reminder in reminders:
            sender.send_reminder(reminder.dest_userid,
                                 reminder.source_userid,
                                 reminder.text)
        #sender.send_reminder(938118842973491,938118842973491,"heydude")  
        model.Reminder.update_current_reminders(reminders)
        self.response.write("success!")

class LogHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.get('clear') == 'T':
            logger.clear_log()
        if self.request.get('msg'):
            logger.log(self.request.get('msg'))

        self.response.write(logger.dump_log())

app = webapp2.WSGIApplication([
    ('/webhook', MainHandler),
    ('/log', LogHandler),
    ('/cron', CronHandler),
], debug=True)

if __name__ == '__main__':
    run_wsgi_app(application)   

