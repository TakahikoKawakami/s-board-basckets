from apscheduler.schedulers.background import BackgroundScheduler
from baskets.controllers.BasketController import BasketScheduler

def hello():
    print("hello")


def syncTodaysBasket():
    BasketScheduler.syncTodaysBasket()


sched = BackgroundScheduler(standalone=True, coalesce=True)
# sched.add_job(hello, 'interval', minutes=1)
sched.add_job(syncTodaysBasket, 'cron', hour="9")
sched.start()