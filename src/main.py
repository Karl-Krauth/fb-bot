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

import logger
import models

class MainHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.get('hub.verify_token') == 'fiend':
            self.response.write(self.request.get('hub.challenge'))
        else:
            self.response.write('Error, wrong validation token.')
 
    def post(self):
        logger.log(self.request.body)


class CronHandler(webapp2.RequestHandler):
    def get(self):
        logger.log(models.Reminders.get_and_update_current_reminders())

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
