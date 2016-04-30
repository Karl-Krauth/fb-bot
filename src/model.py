import datetime

from google.appengine.ext import ndb

class Reminder(ndb.Model):
    # Possible values include unique, daily, weekly, monthly.
    # reminder_type = ndb.StringProperty()
    # Value is in UTC.
    reminder_time = ndb.DateTimeProperty()
    text = ndb.StringProperty(indexed=False)
    source_userid = ndb.IntegerProperty()
    dest_userid = ndb.IntegerProperty() 

    @classmethod
    def add_reminder(cls, source_userid, dest_userid, text, reminder_time):
        r = cls(source_userid=source_userid,
	        dest_userid=dest_userid,
	        text=text,
	        reminder_time=reminder_time)
        r.put()

    @classmethod
    def get_current_reminders(cls):
        now = datetime.datetime.utcnow()
        reminders = cls.query().filter(cls.reminder_time < now)
        return reminders

    @classmethod
    def update_current_reminders(cls, reminders):
        for reminder in reminders:
            reminder.key.delete()

class Log(ndb.Model):
    log = ndb.StringProperty(indexed=False)

