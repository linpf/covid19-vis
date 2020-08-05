from apscheduler.schedulers.blocking import BlockingScheduler
import requests

sched = BlockingScheduler(timezone="America/Vancouver")

@sched.scheduled_job('interval', minutes=60)
def timed_job():
    print('This job is run every 60 minutes.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=23)
def scheduled_job():
    print('This job is run every weekday at 5pm.')
    url = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Case_Details.csv'
    r = requests.get(url)
    with open('data/BCCDC_COVID19_Dashboard_Case_Details.csv', 'wb') as f:
        f.write(r.content)

    url = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Lab_Information.csv'
    r = requests.get(url)
    with open('data/BCCDC_COVID19_Dashboard_Lab_Information.csv', 'wb') as f:
        f.write(r.content)

sched.start()
