from apscheduler.schedulers.background import BackgroundScheduler
from .views import update_seller_offers



def start():
    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.start()
    scheduler.add_job(update_seller_offers, 'cron', hour='08',minute="31",id='my_job_id')
    
    