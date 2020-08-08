from apscheduler.schedulers.blocking import BlockingScheduler
import requests

sched = BlockingScheduler(timezone="America/Vancouver")

#@sched.scheduled_job('interval', minutes=1)
#def timed_job():
#    print('This job is run every 1 minutes.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=20)
def scheduled_job():
    print('This job is run every weekday at 9pm.')

    url = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Case_Details.csv'
    r = requests.get(url)
    with open('data/BCCDC_COVID19_Dashboard_Case_Details.csv', 'wb') as f:
        f.write(r.content)

    url = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Lab_Information.csv'
    r = requests.get(url)
    with open('data/BCCDC_COVID19_Dashboard_Lab_Information.csv', 'wb') as f:
        f.write(r.content)

    files_list = [ "timeseries_canada/cases_timeseries_canada.csv",
               "timeseries_canada/testing_timeseries_canada.csv",
               "timeseries_canada/mortality_timeseries_canada.csv",
               "timeseries_canada/active_timeseries_canada.csv",
               "timeseries_canada/recovered_timeseries_canada.csv",
               "timeseries_prov/cases_timeseries_prov.csv",
               "timeseries_prov/mortality_timeseries_prov.csv",
               "timeseries_prov/testing_timeseries_prov.csv",
               "timeseries_prov/recovered_timeseries_prov.csv",
               "timeseries_prov/active_timeseries_prov.csv",
               "timeseries_hr/cases_timeseries_hr.csv" ,
               "timeseries_hr/mortality_timeseries_hr.csv" ]

    for csv_file in files_list:
        url = 'https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/' + csv_file
        r = requests.get(url)
        with open('data/Covid19Canada/' + csv_file, 'wb') as f:
            f.write(r.content)

sched.start()