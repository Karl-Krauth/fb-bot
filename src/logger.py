import model

def dump_log():
    if model.Log.query().get() is None:
        log("")
    return model.Log.query().get().log

def log(msg):
    log = model.Log.query().get()
    if log is None:
        log = model.Log(log="")

    log.log += msg + "\n"
    log.put()
