import datetime
from google.appengine.ext import ndb
import logger

class Reminder(ndb.Model):
    # Possible values include unique, daily, weekly, monthly.
    # reminder_type = ndb.StringProperty()
    # Value is in UTC.
    recurring = ndb.IntegerProperty(default=0)
    reminder_time = ndb.DateTimeProperty()
    text = ndb.StringProperty(indexed=False)
    source_userid = ndb.IntegerProperty()
    dest_userid = ndb.IntegerProperty() 
    group_name = ndb.StringProperty(default="")

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
            if reminder.recurring == 0:
                reminder.key.delete()
            else:
                reminder.reminder_time + datetime.timedelta(days=reminder.recurring)

# keeping a database of userid and their names
class Users(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    user_id = ndb.IntegerProperty()

    @classmethod
    def add_user(cls, first_name, last_name, id):
        u = cls(first_name=first_name.lower(),
            last_name=last_name.lower(),
            user_id=id)
        u.put()

    @classmethod
    def get_by_id(cls, id):
        return cls.query().filter(cls.user_id == id).get()

    @classmethod
    def find_by_name(cls, first_name, last_name):
        logger.log("%s %s" % (first_name, last_name))
        return cls.query().filter(cls.first_name == first_name.lower() and cls.last_name==last_name.lower()).get()

class Group(ndb.Model):
    group_name = ndb.StringProperty()
    subscribers = ndb.IntegerProperty(repeated=True) 

class Log(ndb.Model):
    log = ndb.StringProperty(indexed=False)

