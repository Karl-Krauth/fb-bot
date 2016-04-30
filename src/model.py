import datetime

from google.appengine.ext import ndb

class Reminder(ndb.Model):
    # Possible values include unique, daily, weekly, monthly.
    # reminder_type = ndb.StringProperty()
    # Value is in UTC.
    reminder_time = ndb.DateTimeProperty()
    text = ndb.StringProperty()
    source_userid = ndb.StringProperty()
    dest_userid = ndb.StringProperty() 

    @classmethod
    def get_and_update_current_reminders(cls):
        now = datetime.datetime.utcnow()
        reminders = cls.query().filter(cls.reminder_time < now)
        for reminder in reminders:
            # TODO(karl): instead of deleting reminders we might want
            # to renew them.
            reminder.key().delete()
        return reminders   

class Log(ndb.Model):
    log = ndb.StringProperty()

