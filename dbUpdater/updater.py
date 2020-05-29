from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from dbUpdater import updatedata

def start():
    print("We are here")
    scheduler = BackgroundScheduler()
    scheduler.add_job(updatedata.dataupdate, 'interval', minutes=20)
    scheduler.start()
