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
    def add_reminder(cls, source_userid, dest_userid, text, reminder_time):
    	r = cls(
	        source_userid=source_userid,
	        dest_userid=dest_userid,
	        text=text,
	        reminder_time=reminder_time,
	        )
	    r.put()

class Log(ndb.Model):
    log = ndb.StringProperty()

