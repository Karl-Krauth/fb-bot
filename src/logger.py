import model
import parse

def dump_log():
    log = model.Log.query().get()
    if log is None:
        return ""

    return model.Log.query().get().log

def clear_log():
    log = model.Log.query().get()
    if log is None:
        return
    log.log = ""
    log.put()

def log(msg):
    log = model.Log.query().get()
    if log is None:
        log = model.Log(log="")

    log.log += msg + "<br>"
    log.put()

def add_reminder(j):
    info = parse.parse_text(j)
    source_userid = parse.get_sender_user_id(j)
    model.Reminder.add_reminder(source_userid, info["remindee"], info["text"], info["date"])