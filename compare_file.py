import requests
import os

def scheduled_job():

    os.chdir("/home/peter/covid19-vis")

    file_bigger = False 
    url = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Case_Details.csv'
    r = requests.get(url)
    with open('data/BCCDC_COVID19_Dashboard_Case_Details.csv', 'rb') as f:
        file_size =  len(f.read())
        print(len(r.content),file_size)
        file_bigger = len(r.content) > file_size

    if file_bigger: 
        with open('data/BCCDC_COVID19_Dashboard_Case_Details.csv', 'wb') as f:
            f.write(r.content)

    file_bigger = False 
    url = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Lab_Information.csv'
    r = requests.get(url)
    with open('data/BCCDC_COVID19_Dashboard_Lab_Information.csv', 'rb') as f:
        file_size =  len(f.read())
        print(len(r.content),file_size)
        file_bigger = len(r.content) > file_size

    if file_bigger: 
        with open('data/BCCDC_COVID19_Dashboard_Lab_Information.csv', 'wb') as f:
            f.write(r.content)

    files_list = [ "cases.csv", "mortality.csv", 
               "recovered_cumulative.csv", "testing_cumulative.csv", 
               "timeseries_canada/cases_timeseries_canada.csv",
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
        file_bigger = False
        with open('data/Covid19Canada/' + csv_file, 'rb') as f:
            file_size =  len(f.read())
            print(len(r.content),file_size)
            file_bigger = len(r.content) > file_size
        if file_bigger:
            with open('data/Covid19Canada/' + csv_file, 'wb') as f:
                f.write(r.content)

    if file_bigger:
        csv_file = "update_time.txt"
        url = 'https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/' + csv_file
        r = requests.get(url)
        with open('data/Covid19Canada/' + csv_file, 'wb') as f:
            f.write(r.content)

if __name__ == "__main__":
    scheduled_job()
