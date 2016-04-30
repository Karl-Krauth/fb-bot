from google.appengine.ext import ndb

class Reminder(ndb.Model):
    # Possible values include unique, daily, weekly, monthly.
    # reminder_type = ndb.StringProperty()
    # Value is in UTC.
    reminder_time = ndb.DateTimeProperty()
    text = ndb.StringProperty()
    source_userid = ndb.StringProperty()
    dest_userid = ndb.StringProperty() 

class Log(ndb.Model):
    log = ndb.StringProperty()

