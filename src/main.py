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

class MainHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.get('hub.verify_token') == 'fiend':
            self.response.write(self.request.get('hub.challenge'))
        else:
            self.response.write('Error, wrong validation token.')
 
    def post(self):
        logger.log(self.request.body)
        sender = parse.get_source_user_id(self.request.body)
        if sender is None:
            # TODO: send an error response.
            logger.log("Invalid sender")
            return
        text_data = parse.parse_text(self.request.body)
        if text_data is None:
            # TODO: send an error response.
            logger.log("invalid text data")
            return
        model.Reminder.add_reminder(sender, text_data["remindee"],
                                    text_data["text"], text_data["date"])

class CronHandler(webapp2.RequestHandler):
    def get(self):
        reminders = model.Reminder.get_current_reminders()

        for reminder in reminders:
            try:
                sender.send_reminder(reminder.dest_userid,
                                     reminder.source_userid,
                                     reminder.text)
            except:
                logger.log("Failed to message %d" % reminder.dest_userid)

        model.Reminder.update_current_reminders(reminders)
class LogHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.get('clear') == 'T':
            logger.clear_log()
        if self.request.get('msg'):
            logger.add_reminder(self.request.get('msg'))
            logger.log(self.request.get('msg'))

        self.response.write(logger.dump_log())

app = webapp2.WSGIApplication([
    ('/webhook', MainHandler),
    ('/log', LogHandler),
    ('/cron', CronHandler),
], debug=True)

if __name__ == '__main__':
    run_wsgi_app(application)	

