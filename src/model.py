from google.appengine.ext import ndb

class Reminder(ndb.Model):
    # Possible values include unique, daily, weekly, monthly.
    # reminder_type = ndb.StringProperty()
    # Value is in UTC.
    next_reminder = ndb.DateTimeProperty()
    # 

class Log(ndb.Model):
    log = ndb.StringProperty()

