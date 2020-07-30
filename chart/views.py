import pygal
from pygal.style import DarkSolarizedStyle
import csv
from collections import Counter
from django.shortcuts import render
from django.views.decorators.cache import cache_page
import datetime


@cache_page(60 * 15)
def home_view(request):


    chart1 = canada_cases_and_mortality_weekly_bar_chart(request)
    chart3 = provs_latest_cases_and_mortality_stackbar_chart(request)
    chart4 = canada_cumulative_cases_lines_chart()
    chart2 = provs_cumulative_cases_stackbar_chart3(request)
    
    charts = [chart1, chart2, chart3, chart4]
    context = {
        "charts": charts,
        "title":  "Coronavirus Cases in CANADA"
    }

    return render(request, "chart/charts.html", context)
   
@cache_page(60 * 15)    
def canada_view(request):
    
    chart2 = canada_cases_and_mortality_bar_chart(request)
    chart4 = canada_cases_and_testing_weekly_bar_chart()
    chart1 = canada_cases_and_mortality_weekly_bar_chart(request)
    chart3 = provs_latest_cases_and_mortality_stackbar_chart(request)
    

    charts = [chart1, chart2, chart3, chart4]
    context = {
        "charts": charts,
        "title":  "Coronavirus Cases in CANADA"
    }

    return render(request, "chart/charts.html", context)
    
@cache_page(60 * 15)
def provinces_mortality_view(request):


    chart1 = provs_mortality_weekly_bar_chart(request)
    chart4 = provs_mortality_cumulative_line_chart()
    chart3 = provs_mortality_cumulative_hbar_chart(request)
    chart2 = provs_mortality_daily_bar_chart(request)

    charts = [chart1, chart2, chart3, chart4]

    context = {
        "charts": charts,
        "title":  "Coronavirus mortality per Province"
    }

    return render(request, "chart/charts.html", context)    

@cache_page(60 * 15)
def provinces_cases_view(request):

    chart1 = provs_cases_weekly_bar_chart(request)
    chart4 = provs_cases_cumulative_line_chart()
    chart3 = provs_cases_cumulative_hbar_chart(request)
    chart2 = provs_cases_daily_bar_chart(request)

    charts = [chart1, chart2, chart3, chart4]

    context = {
        "charts": charts,
        "title":  "Coronavirus mortality per Province"
    }

    return render(request, "chart/charts.html", context)
    
@cache_page(60 * 15)
def provinces_view(request):

    chart1 = provs_cases_weekly_bar_chart(request)
    chart3 = provs_latest_cases_and_mortality_stackbar_chart(request)
    chart4 = provs_cumulative_cases_line_chart(request)
    chart2 = provs_cumulative_cases_stackbar_chart(request)

    charts = [chart1, chart2, chart3, chart4]

    context = {
        "charts": charts,
        "title":  "Coronavirus Cases per Province"
    }

    return render(request, "chart/charts.html", context)
    
@cache_page(60 * 15)
def province_view(request, province):

    chart1 = prov_hrs_cases_bar_chart(province)
    chart2 = prov_hrs_cases_cumulative_line_chart(province)
    chart3 = prov_hrs_mortality_bar_chart(province)
    chart4 = prov_hrs_cumulative_mortality_line_chart(province)


    charts = [chart1, chart2, chart3, chart4, chart5]

    context = {
        "charts": charts,
        "title":  "Coronavirus Cases in " + province
    }

    return render(request, "chart/charts.html", context)

def canada_cases_bar_chart():

    data_x_y = {}
    groups_list = {}

    with open("data/Covid19Canada/timeseries_canada/cases_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_report"], "cases")
                     ] = int(row_data["cases"])
            groups_list["cases"] = int(row_data["cases"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_groups = sorted(groups_list.keys(), key=lambda k: -groups_list[k])
    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Bar(height=400, 
        show_minor_x_labels=False,show_x_labels=True,x_label_rotation=0.01,
        show_legend=False)
    for group in sorted_groups:
        data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                data_list.append(data_x_y[(day, group)])
            else:
                data_list.append(None)
        chart.add("", data_list)

    chart.title = "New Reported Cases in Canada"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()
    
def canada_cases_weekly_bar_chart():

    data_x_y = {} 
    with open("data/Covid19Canada/timeseries_canada/cases_timeseries_canada.csv", 'r') as file:
        groups_list = {} 
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            year_week = report_date_to_year_week(row_data["date_report"])
            if (year_week,"Canada") not in data_x_y:
                data_x_y[(year_week,"Canada")] = 0
            data_x_y[(year_week,"Canada")] += int(row_data["cases"])

    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart = pygal.Bar(height=400,legend_at_bottom=True, x_title="(year, week number)")
    for province in ["Canada"]:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week,province) in data_x_y:
                timeseries_data.append(data_x_y[(week,province)])
            else:
                timeseries_data.append(None)
        chart.add(province, timeseries_data)
        
        
    chart.title = "Canada weekly cases count"
    chart.x_labels = sorted_report_weeks 
    
    return chart.render_data_uri()   
    

def canada_cases_and_testing_bar_chart():

    data_x_y = {}
 
    with open("data/Covid19Canada/timeseries_canada/testing_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_testing"], "testing")
                     ] = int(row_data["testing"])

    with open("data/Covid19Canada/timeseries_canada/cases_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_report"], "cases")
                     ] = int(row_data["cases"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Bar(height=400, 
        show_minor_x_labels=False,show_x_labels=True,x_label_rotation=0.01,
        legend_at_bottom=True, x_title="(year, week number)")
        
    for group in ["cases", "testing"]:
        cumulative_data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                cumulative_data_list.append(data_x_y[(day, group)])
            else:
                cumulative_data_list.append(None)
        chart.add(group, cumulative_data_list)

    chart.title = "Cases and Testing by Date"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()
    

def canada_cases_and_mortality_bar_chart(request):

    data_x_y = {}
    
    with open("data/Covid19Canada/timeseries_canada/mortality_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_death_report"], "deaths")
                     ] = int(row_data["deaths"])
            
    with open("data/Covid19Canada/timeseries_canada/cases_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_report"], "cases")
                     ] = int(row_data["cases"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Bar(height=400, 
        show_minor_x_labels=False,show_x_labels=True,x_label_rotation=0.01,
        legend_at_bottom=True)
    xlinks = {"cases": "provinces_cases", "deaths": "provinces_mortality"} 
    for group in ["deaths" , "cases"]:
        cumulative_data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                cumulative_data_list.append(data_x_y[(day, group)])
            else:
                cumulative_data_list.append(None)
        chart.add({"title": group ,'xlink': {"href": request.build_absolute_uri(
            '/'+ xlinks[group] + '/'), "target": "_top"}}, cumulative_data_list)

    chart.title = "Cases and Deaths"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    
    return chart.render_data_uri()
    
def canada_cases_and_testing_weekly_bar_chart():

    data_x_y = {} 
    
    with open("data/Covid19Canada/timeseries_canada/testing_timeseries_canada.csv", 'r') as file:
        groups_list = {} 
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            year_week = report_date_to_year_week(row_data["date_testing"])
            if (year_week,"testing") not in data_x_y:
                data_x_y[(year_week,"testing")] = 0
            data_x_y[(year_week,"testing")] += int(row_data["testing"])
    
    with open("data/Covid19Canada/timeseries_canada/cases_timeseries_canada.csv", 'r') as file:
        groups_list = {} 
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            year_week = report_date_to_year_week(row_data["date_report"])
            if (year_week,"cases") not in data_x_y:
                data_x_y[(year_week,"cases")] = 0
            data_x_y[(year_week,"cases")] += int(row_data["cases"])

    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart = pygal.Bar(height=400,legend_at_bottom=True, x_title="Week number")
    for group in ["testing", "cases"]:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week,group) in data_x_y:
                timeseries_data.append(data_x_y[(week,group)])
            else:
                timeseries_data.append(None)
        chart.add(group, timeseries_data)
    chart.title = "Canada weekly Cases and Testing"
    chart.x_labels = [ w[1] for w in sorted_report_weeks ]  
    
    return chart.render_data_uri()      
    
def canada_cases_and_mortality_weekly_bar_chart(request):

    data_x_y = {} 
    
    with open("data/Covid19Canada/timeseries_canada/mortality_timeseries_canada.csv", 'r') as file:
        groups_list = {} 
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            year_week = report_date_to_year_week(row_data["date_death_report"])
            if (year_week,"deaths") not in data_x_y:
                data_x_y[(year_week,"deaths")] = 0
            data_x_y[(year_week,"deaths")] += int(row_data["deaths"])
    
    with open("data/Covid19Canada/timeseries_canada/cases_timeseries_canada.csv", 'r') as file:
        groups_list = {} 
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            year_week = report_date_to_year_week(row_data["date_report"])
            if (year_week,"cases") not in data_x_y:
                data_x_y[(year_week,"cases")] = 0
            data_x_y[(year_week,"cases")] += int(row_data["cases"])

    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart = pygal.Bar(height=400,legend_at_bottom=True, x_title="Week number")
    xlinks = {"cases": "provinces_cases", "deaths": "provinces_mortality"} 
    for group in [ "deaths", "cases"]:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week,group) in data_x_y:
                timeseries_data.append(data_x_y[(week,group)])
            else:
                timeseries_data.append(None)
        chart.add({"title": group ,'xlink': {"href": request.build_absolute_uri(
            '/'+ xlinks[group] + '/'), "target": "_top"}}, timeseries_data)
    chart.title = "Canada weekly Cases and Deaths"
    chart.x_labels = [ w[1] for w in sorted_report_weeks ] 
    
    return chart.render_data_uri()     
      
    
def canada_testing_bar_chart():

    data_x_y = {}
    groups_list = {}
    with open("data/Covid19Canada/timeseries_canada/testing_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_testing"], "testing")
                     ] = int(row_data["testing"])
            groups_list["testing"] = int(row_data["testing"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_groups = sorted(groups_list.keys(), key=lambda k: -groups_list[k])
    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Bar(height=400, 
        show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01,
        show_legend=False)
    for group in sorted_groups:
        data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                data_list.append(data_x_y[(day, group)])
            else:
                data_list.append(None)
        chart.add("", data_list)

    chart.title = "Canada daily testing"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]

    return chart.render_data_uri()


def canada_cumulative_testing_line_chart():
    data_x_y = {}
    groups_list = {}
    with open("data/Covid19Canada/timeseries_canada/testing_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_testing"], "cumulative_testing")
                     ] = int(row_data["cumulative_testing"])
            groups_list["cumulative_testing"] = int(
                row_data["cumulative_testing"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_groups = sorted(groups_list.keys(), key=lambda k: -groups_list[k])
    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Line(height=400, 
        show_minor_x_labels = False, show_x_labels = True, x_label_rotation = 0.01,
        show_legend=False)
    for group in sorted_groups:
        data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                data_list.append(data_x_y[(day, group)])
            else:
                data_list.append(None)
        chart.add("", data_list)

    chart.title = "Canada cumulative testing"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    
    return chart.render_data_uri()


@cache_page(60 * 15)
def canada_cumulative_cases_view(request):

    chart1 = canada_cumulative_cases_lines_chart()

    charts = [chart1]

    context = {
        "charts": charts,
        "title":  "Coronavirus Cases in CANADA"
    }

    return render(request, "chart/charts.html", context)


def canada_cumulative_cases_lines_chart():

    data_x_y = {}

    with open("data/Covid19Canada/timeseries_canada/active_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_active"], "active_cases")
                     ] = int(row_data["active_cases"])
            data_x_y[(row_data["date_active"], "cumulative_cases")
                     ] = int(row_data["cumulative_cases"])
            data_x_y[(row_data["date_active"], "cumulative_recovered")] = int(
                row_data["cumulative_recovered"])
            data_x_y[(row_data["date_active"], "cumulative_deaths")
                     ] = int(row_data["cumulative_deaths"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Line(height=400, 
        show_minor_x_labels=False, show_x_labels=True, x_label_rotation=0.01, 
        legend_at_bottom=True)
    for group in ["cumulative_deaths", "cumulative_cases", "cumulative_recovered", "active_cases"]:
        cumulative_data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                cumulative_data_list.append(data_x_y[(day, group)])
            else:
                cumulative_data_list.append(None)
        chart.add(group, cumulative_data_list)

    chart.title = "Active and cumulative cases in Canada"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]

    return chart.render_data_uri()
    
@cache_page(60 * 15)
def bc_view(request):  
    pass  

@cache_page(60 * 15)
def province_cases_view(request, province):

    chart1 = prov_cases_and_mortality_weekly_bar_chart(request, province)
    chart3 = prov_hrs_latest_cases_and_mortality_bar_chart(request, province)
    chart2 = prov_cases_and_mortality_bar_chart(request, province)
    chart4 = prov_cases_and_testing_weekly_bar_chart(province)
    
    charts = [chart1, chart2, chart3, chart4]

    context = {
        "charts": charts,
        "title":  "Province cases view by Reported Date"
    }

    return render(request, "chart/charts.html", context)


@cache_page(60 * 15)
def province_cumulative_view(request, province):

    chart4 = prov_cumulative_cases_lines_chart(province)
    chart2 = prov_cumulative_testing_line_chart(province)
    #chart3 = prov_hrs_cumulative_cases_hbar_chart(request, province)
    chart3 = prov_hrs_cumulative_cases_and_mortality_stacked_bar_chart(request, province)
    chart1 = prov_hrs_mortality_cumulative_hbar_chart(request, province)
    charts = [chart1, chart2, chart3, chart4]

    context = {
        "charts": charts,
        "title":  "Province cumulative view"
    }

    return render(request, "chart/charts.html", context)


@cache_page(60 * 15)
def provinces_testing_view(request):

    chart1 = provs_testing_line_chart()
    chart2 = provs_testing_compared_line_chart()
    charts = [chart1, chart2]

    context = {
        "charts": charts,
        "title":  "Coronavirus Testing in CANADA"
    }

    return render(request, "chart/charts.html", context)

def provs_cumulative_cases_bar_chart(request):

    provs_data = {}
    groups_list = {}
    provs_latest_report_date = {}

    with open("data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            province = row_data["province"]
            provs_data[province] = int(row_data["cumulative_cases"])
            provs_latest_report_date[province] = row_data["date_report"]

    chart = pygal.Bar(height=400, legend_at_bottom=True)

    sorted_provs = sorted(
        provs_data.keys(), key=lambda province: -provs_data[province])
    for province in sorted_provs:
        chart.add({"title": province, 'xlink': {"href": request.build_absolute_uri(
            '/province/' + province + '/') , "target": "_top"}}, [provs_data[province]])
    chart.title = "Cumulative reported cases per Province"
    return chart.render_data_uri()


def provs_mortality_cumulative_hbar_chart(request):

    provs_data = {}
    groups_list = {}
    provs_latest_report_date = {}

    with open("data/Covid19Canada/timeseries_prov/mortality_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            province = row_data["province"]
            provs_data[province] = int(row_data["cumulative_deaths"])
            provs_latest_report_date[province] = row_data["date_death_report"]

    chart = pygal.HorizontalStackedBar(height=400, legend_at_bottom=True)

    sorted_provs = sorted(
        provs_data.keys(), key=lambda province: -provs_data[province])
    for province in sorted_provs:
        chart.add({"title": province , 'xlink': {"href": request.build_absolute_uri(
            '/province_mortality_hrs/' + province + '/'), "target": "_top"} }, [provs_data[province]])
    chart.title = "cumulative mortality per Province"
    return chart.render_data_uri()
    
def provs_cases_cumulative_hbar_chart(request):

    provs_data = {}
    groups_list = {}
    provs_latest_report_date = {}

    with open("data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            province = row_data["province"]
            provs_data[province] = int(row_data["cumulative_cases"])
            provs_latest_report_date[province] = row_data["date_report"]

    chart = pygal.HorizontalStackedBar(height=400, legend_at_bottom=True)

    sorted_provs = sorted(
        provs_data.keys(), key=lambda province: -provs_data[province])
    for province in sorted_provs:
        chart.add({"title": province , 'xlink': {"href": request.build_absolute_uri(
            '/province_hrs/' + province + '/'), "target": "_top"} }, [provs_data[province]])
    chart.title = "cumulative Cases per Province"
    return chart.render_data_uri()

def provs_testing_line_chart():

    d1 = datetime.date.today()
    with open("data/Covid19Canada/timeseries_prov/testing_timeseries_prov.csv", 'r') as file:
        data_x_y = {}
        provinces_list = {}
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_testing"], row_data["province"])
                     ] = int(row_data["testing"])
            provinces_list[row_data["province"]] = int(
                row_data["cumulative_testing"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_provinces = sorted(provinces_list.keys(),
                              key=lambda k: -provinces_list[k])
    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Line(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01,
                       legend_at_bottom=True, show_dots=True, dots_size=2)
    for province in sorted_provinces:
        province_cases_per_day = []
        for day in sorted_report_days:
            if (day, province) in data_x_y:
                province_cases_per_day.append(data_x_y[(day, province)])
            else:
                province_cases_per_day.append(None)
        chart.add(province, province_cases_per_day)
    chart.title = "daily testing by province"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()


def provs_cases_weekly_bar_chart(request):

    data_x_y = {}
    provinces_list = {}
    
    with open("data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            year_week = report_date_to_year_week(row_data["date_report"])
            if (year_week,row_data["province"]) not in data_x_y:
                data_x_y[(year_week,row_data["province"])] = 0
            data_x_y[(year_week,row_data["province"])] += int(row_data["cases"])
            
            provinces_list[row_data["province"]] = int(
                row_data["cumulative_cases"])
                

    sorted_provinces = sorted(provinces_list.keys(),
                              key=lambda k: -provinces_list[k])
                              
    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart = pygal.StackedBar(height=400, show_x_labels=True, show_legend=True, legend_at_bottom=True, 
        x_title="(year, week number)")
    
    for province in sorted_provinces:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week,province) in data_x_y:
                timeseries_data.append(data_x_y[(week,province)])
            else:
                timeseries_data.append(None)
        chart.add({"title": province, 'xlink': { "href": request.build_absolute_uri(
            '/province_cases/' + province + '/') , "target": "_top"}}, timeseries_data)
                              
    chart.title = "Weekly New Cases by province"
    chart.x_labels = [ w[1] for w in sorted_report_weeks ] 

    return chart.render_data_uri()
    
    
def prov_hrs_cases_weekly_bar_chart(request, province):

    data_x_y = {}
    hrs_list = {}
    
    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                year_week = report_date_to_year_week(row_data["date_report"])
                if (year_week,row_data["health_region"]) not in data_x_y:
                    data_x_y[(year_week,row_data["health_region"])] = 0
                data_x_y[(year_week,row_data["health_region"])] += int(row_data["cases"])
                
                hrs_list[row_data["health_region"]] = int(row_data["cumulative_cases"])
                
    sorted_hrs = sorted(hrs_list.keys(),
                              key=lambda k: -hrs_list[k])
                              
    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart = pygal.StackedBar(height=400, show_x_labels=True, show_legend=False, x_title="Week number")
    for hr in sorted_hrs:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week,hr) in data_x_y:
                timeseries_data.append(data_x_y[(week,hr)])
            else:
                timeseries_data.append(None)
        chart.add({"title": hr}, timeseries_data)
                              
    chart.title = "{} Weekly New Cases by health region".format(province)
    chart.x_labels = [ w[1] for w in sorted_report_weeks ] 

    return chart.render_data_uri()    
    
    
def prov_hrs_cases_daily_bar_chart(request, province):

    data_x_y = {}
    hrs_list = {}
    
    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_report"],row_data["health_region"])] = int(row_data["cases"])
                hrs_list[row_data["health_region"]] = int(row_data["cumulative_cases"])
                
    sorted_hrs = sorted(hrs_list.keys(),
                              key=lambda k: -hrs_list[k])
    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.StackedBar(height=400, show_x_labels=True, show_legend=False,
            show_minor_x_labels=False, x_label_rotation=0.01)
    for hr in sorted_hrs:
        timeseries_data = []
        for day in sorted_report_days:
            if (day,hr) in data_x_y:
                timeseries_data.append(data_x_y[(day,hr)])
            else:
                timeseries_data.append(None)
        chart.add({"title": hr}, timeseries_data)
                              
    chart.title = "{} Daily New Cases by health region".format(province)
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    
    return chart.render_data_uri()      
    

def prov_hrs_mortality_daily_bar_chart(request, province):

    data_x_y = {}
    hrs_list = {}
    
    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_death_report"],row_data["health_region"])] = int(row_data["deaths"])
                hrs_list[row_data["health_region"]] = int(row_data["cumulative_deaths"])
                
    sorted_hrs = sorted(hrs_list.keys(),
                              key=lambda k: -hrs_list[k])
    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.StackedBar(height=400, show_x_labels=True, show_legend=False,
            show_minor_x_labels=False, x_label_rotation=0.01)
    for hr in sorted_hrs:
        timeseries_data = []
        for day in sorted_report_days:
            if (day,hr) in data_x_y:
                timeseries_data.append(data_x_y[(day,hr)])
            else:
                timeseries_data.append(None)
        chart.add({"title": hr}, timeseries_data)
                              
    chart.title = "{} Daily Deaths by health region".format(province)
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    
    return chart.render_data_uri()          
    
    
def prov_hrs_mortality_weekly_bar_chart(request, province):

    data_x_y = {}
    hrs_list = {}
    
    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                year_week = report_date_to_year_week(row_data["date_death_report"])
                if (year_week,row_data["health_region"]) not in data_x_y:
                    data_x_y[(year_week,row_data["health_region"])] = 0
                data_x_y[(year_week,row_data["health_region"])] += int(row_data["deaths"])
                
                hrs_list[row_data["health_region"]] = int(row_data["cumulative_deaths"])
                
    sorted_hrs = sorted(hrs_list.keys(),
                              key=lambda k: -hrs_list[k])
    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart = pygal.StackedBar(height=400, show_x_labels=True, show_legend=False, x_title="Week number")
    for hr in sorted_hrs:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week,hr) in data_x_y:
                timeseries_data.append(data_x_y[(week,hr)])
            else:
                timeseries_data.append(None)
        chart.add({"title": hr}, timeseries_data)
                              
    chart.title = "{} Weekly Deaths by health region".format(province)
    chart.x_labels = [ w[1] for w in sorted_report_weeks ] 

    return chart.render_data_uri()  
    

def prov_hrs_mortality_weekly_bar_chart(request, province):

    data_x_y = {}
    hrs_list = {}
    
    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                year_week = report_date_to_year_week(row_data["date_death_report"])
                if (year_week,row_data["health_region"]) not in data_x_y:
                    data_x_y[(year_week,row_data["health_region"])] = 0
                data_x_y[(year_week,row_data["health_region"])] += int(row_data["deaths"])
                
                hrs_list[row_data["health_region"]] = int(row_data["cumulative_deaths"])
                
    sorted_hrs = sorted(hrs_list.keys(),
                              key=lambda k: -hrs_list[k])
    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart = pygal.StackedBar(height=400, show_x_labels=True, show_legend=False, x_title="(year, week number)")
    for hr in sorted_hrs:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week,hr) in data_x_y:
                timeseries_data.append(data_x_y[(week,hr)])
            else:
                timeseries_data.append(None)
        chart.add({"title": hr}, timeseries_data)
                              
    chart.title = "{} Weekly Deaths by health region".format(province)
    chart.x_labels = sorted_report_weeks

    return chart.render_data_uri()  
    
def provs_mortality_daily_bar_chart(request):

    data_x_y = {}
    provs_list = {}
    
    with open("data/Covid19Canada/timeseries_prov/mortality_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            day = row_data["date_death_report"]
            if (day,row_data["province"]) not in data_x_y:
                data_x_y[(day,row_data["province"])] = 0
            data_x_y[(day,row_data["province"])] = int(row_data["deaths"])
               
            provs_list[row_data["province"]] = int(row_data["cumulative_deaths"])
                
    sorted_provs = sorted(provs_list.keys(),
                              key=lambda k: -provs_list[k])
    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)
                              
    sorted_report_days = sorted(list(report_days), key=day_month_year)

    chart = pygal.StackedBar(height=400, show_x_labels=True, show_legend=False,
        show_minor_x_labels=False, x_label_rotation=0.01)
    for province in sorted_provs:
        timeseries_data = []
        for day in sorted_report_days:
            if (day,province) in data_x_y:
                timeseries_data.append(data_x_y[(day,province)])
            else:
                timeseries_data.append(None)
        chart.add({"title": province}, timeseries_data)
                              
    chart.title = "Daily Deaths by Province"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]

    return chart.render_data_uri()    
    
def provs_cases_daily_bar_chart(request):

    data_x_y = {}
    provs_list = {}
    
    with open("data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            day = row_data["date_report"]
            if (day,row_data["province"]) not in data_x_y:
                data_x_y[(day,row_data["province"])] = 0
            data_x_y[(day,row_data["province"])] = int(row_data["cases"])
               
            provs_list[row_data["province"]] = int(row_data["cumulative_cases"])
                
    sorted_provs = sorted(provs_list.keys(),
                              key=lambda k: -provs_list[k])
    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)
                              
    sorted_report_days = sorted(list(report_days), key=day_month_year)

    chart = pygal.StackedBar(height=400, show_x_labels=True, show_legend=False,
        show_minor_x_labels=False, x_label_rotation=0.01)
    for province in sorted_provs:
        timeseries_data = []
        for day in sorted_report_days:
            if (day,province) in data_x_y:
                timeseries_data.append(data_x_y[(day,province)])
            else:
                timeseries_data.append(None)
        chart.add({"title": province}, timeseries_data)
                              
    chart.title = "Daily reported New Cases by Province"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]

    return chart.render_data_uri()       

    
def provs_mortality_weekly_bar_chart(request):

    data_x_y = {}
    provs_list = {}
    
    with open("data/Covid19Canada/timeseries_prov/mortality_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            year_week = report_date_to_year_week(row_data["date_death_report"])
            if (year_week,row_data["province"]) not in data_x_y:
                data_x_y[(year_week,row_data["province"])] = 0
            data_x_y[(year_week,row_data["province"])] += int(row_data["deaths"])
               
            provs_list[row_data["province"]] = int(row_data["cumulative_deaths"])
                
    sorted_provs = sorted(provs_list.keys(),
                              key=lambda k: -provs_list[k])
    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart = pygal.StackedBar(height=400, show_x_labels=True, show_legend=False, x_title="Week number")
    for province in sorted_provs:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week,province) in data_x_y:
                timeseries_data.append(data_x_y[(week,province)])
            else:
                timeseries_data.append(None)
        chart.add({"title": province}, timeseries_data)
                              
    chart.title = "Weekly Deaths by Province"
    chart.x_labels = [ w[1] for w in sorted_report_weeks ] 

    return chart.render_data_uri()  

def provs_cases_line_chart(request):

    with open("data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        data_x_y = {}
        provinces_list = {}
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_report"], row_data["province"])
                     ] = int(row_data["cases"])
            provinces_list[row_data["province"]] = int(
                row_data["cumulative_cases"])
                

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_provinces = sorted(provinces_list.keys(),
                              key=lambda k: -provinces_list[k])
                              
                              
    sorted_report_days = sorted(list(report_days), key=day_month_year)
    
    
    chart = pygal.StackedBar(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01,
                       legend_at_bottom=True, show_dots=True, dots_size=1)
    for province in sorted_provinces:
        province_cases_per_day = []
        for day in sorted_report_days:
            if (day, province) in data_x_y:
                province_cases_per_day.append(data_x_y[(day, province)])
            else:
                province_cases_per_day.append(None)
        chart.add({"title": province, 'xlink': { "href": request.build_absolute_uri(
            '/province_cases/' + province + '/') , "target": "_top"}}, province_cases_per_day)
    chart.title = "Daily reported cases by province"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()
    
    

def prov_cases_timeseries_stacked_bar_chart():
    d1 = datetime.date.today()
    with open("data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        data_x_y = {}
        provinces_list = {}
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_report"], row_data["province"])
                     ] = int(row_data["cases"])
            provinces_list[row_data["province"]] = int(row_data["cases"])

    report_day_set = set()
    for key in data_x_y:
        day = key[0]
        report_day_set.add(day)

    sorted_provinces = sorted(provinces_list.keys(),
                              key=lambda k: -provinces_list[k])
    sorted_report_days = sorted(list(report_day_set), key=day_month_year)
    chart = pygal.StackedBar(
        height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, legend_at_bottom=False)
    for province in sorted_provinces:
        province_cases_per_day = []
        for day in sorted_report_days:
            if (day, province) in data_x_y:
                province_cases_per_day.append(data_x_y[(day, province)])
            else:
                province_cases_per_day.append(None)
        chart.add(province, province_cases_per_day)
    chart.title = "daily new cases by province"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]

    return chart.render_data_uri()
    
    
def provs_latest_cases_and_mortality_stackbar_chart(request):

    data_x_y = {}

    with open("data/Covid19Canada/timeseries_prov/mortality_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["province"], "deaths")
                     ] = int(row_data["deaths"])
            
    with open("data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["province"], "cases")
                     ] = int(row_data["cases"])
            report_date = row_data["date_report"]
            
    report_provinces = set()
    for key in data_x_y:
        province = key[0]
        report_provinces.add(province)

    sorted_groups = list(reversed(
        ["cases", "deaths"]))
    sorted_report_provinces = sorted(
        report_provinces, key=lambda k: -data_x_y.get((k, "cases"),0) - data_x_y.get((k, "deaths"),0)) 
    chart = pygal.HorizontalStackedBar(height=400, 
        legend_at_bottom=True)
    for province in sorted_report_provinces:
        data_list = []
        for group in sorted_groups:
            if (province, group) in data_x_y:
                data_list.append(data_x_y[(province, group)])
            else:
                data_list.append(None)
        chart.add({"title": province, 'xlink': {"href": request.build_absolute_uri(
            '/province_cases/' + province + '/') , "target": "_top"}}, data_list)

    chart.title = "Cases and Deaths on " + report_date 
    chart.x_labels = sorted_groups

    return chart.render_data_uri()    
    
def hrs_latest_cases_and_mortality_stackbar_chart(request):

    data_x_y = {}

    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[((row_data["health_region"],row_data["province"]), "deaths")
                     ] = int(row_data["deaths"])
            
    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[((row_data["health_region"],row_data["province"]), "cases")
                     ] = int(row_data["cases"])
            report_date = row_data["date_report"]
            
    report_hrs = set()
    for key in data_x_y:
        hr = key[0]
        report_hrs.add(hr)

    sorted_groups = list(reversed(
        ["cases", "deaths"]))
    sorted_report_hrs = sorted(
        report_hrs, key=lambda hr: -data_x_y.get((hr, "cases"),0) - data_x_y.get((hr, "deaths"),0)) 
        
    chart = pygal.HorizontalStackedBar(height=400, show_legend=False,legend_at_bottom=False)
    
    for hr in sorted_report_hrs:
        data_list = []
        for group in sorted_groups:
            if (hr, group) in data_x_y:
                data_list.append({'value': data_x_y[(hr, group)], 'xlink': {"href": request.build_absolute_uri(
                '/health_region/' + hr[1] + '/' + hr[0] + '/') , "target": "_top"}})
            else:
                data_list.append(None)
        chart.add({"title": hr, 'xlink': {"href": request.build_absolute_uri(
            '/health_region/' + hr[1] + '/' + hr[0] + '/') , "target": "_top"}}, data_list)

    chart.title = "Cases and Deaths by Health Region on " + report_date 
    chart.x_labels = sorted_groups

    return chart.render_data_uri()  


def hrs_latest_cases_hbar_chart(request):

    data_x_y = {}
            
    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[((row_data["health_region"],row_data["province"]), "cases")
                     ] = int(row_data["cases"])
            report_date = row_data["date_report"]
            
    report_hrs = set()
    for key in data_x_y:
        hr = key[0]
        report_hrs.add(hr)

    sorted_report_hrs = sorted(
        report_hrs, key=lambda hr: -data_x_y.get((hr, "cases"),0) ) 
        
    chart = pygal.HorizontalStackedBar(height=400, show_legend=False,legend_at_bottom=False)
    
    for hr in sorted_report_hrs:
        data_list = []
        for group in ["cases"]:
            if (hr, group) in data_x_y:
                data_list.append({'value': data_x_y[(hr, group)], 'xlink': {"href": request.build_absolute_uri(
                '/health_region/' + hr[1] + '/' + hr[0] + '/') , "target": "_top"}})
            else:
                data_list.append(None)
        chart.add({"title": hr, 'xlink': {"href": request.build_absolute_uri(
            '/health_region/' + hr[1] + '/' + hr[0] + '/') , "target": "_top"}}, data_list)

    chart.title = "Cases by Health Region on " + report_date 
    chart.x_labels = ["cases"]

    return chart.render_data_uri()  

def hrs_latest_mortality_hbar_chart(request):

    data_x_y = {}

    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[((row_data["health_region"],row_data["province"]), "deaths")
                     ] = int(row_data["deaths"])
            report_date = row_data["date_death_report"]
                        
    report_hrs = set()
    for key in data_x_y:
        hr = key[0]
        report_hrs.add(hr)

    sorted_report_hrs = sorted(
        report_hrs, key=lambda hr: - data_x_y.get((hr, "deaths"),0)) 
        
    chart = pygal.HorizontalStackedBar(height=400, show_legend=False,legend_at_bottom=False)
    
    for hr in sorted_report_hrs:
        data_list = []
        for group in ["deaths"]:
            if (hr, group) in data_x_y:
                data_list.append({'value': data_x_y[(hr, group)], 'xlink': {"href": request.build_absolute_uri(
                '/health_region_mortality/' + hr[1] + '/' + hr[0] + '/') , "target": "_top"}})
            else:
                data_list.append(None)
        chart.add({"title": hr, 'xlink': {"href": request.build_absolute_uri(
            '/health_region_mortality/' + hr[1] + '/' + hr[0] + '/') , "target": "_top"}}, data_list)

    chart.title = "Deaths by Health Region on " + report_date 
    chart.x_labels = ["deaths"]

    return chart.render_data_uri()  
    
    
def hrs_mortality_cumulative_hbar_chart(request):

    data_x_y = {}

    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[((row_data["health_region"],row_data["province"]), "deaths")
                     ] = int(row_data["cumulative_deaths"])
            report_date = row_data["date_death_report"]
                        
    report_hrs = set()
    for key in data_x_y:
        hr = key[0]
        report_hrs.add(hr)

    sorted_report_hrs = sorted(
        report_hrs, key=lambda hr: - data_x_y.get((hr, "deaths"),0)) 
        
    chart = pygal.HorizontalStackedBar(height=400, show_legend=False,legend_at_bottom=False)
    
    for hr in sorted_report_hrs:
        data_list = []
        for group in ["deaths"]:
            if (hr, group) in data_x_y:
                data_list.append({'value': data_x_y[(hr, group)], 'xlink': {"href": request.build_absolute_uri(
                '/health_region_mortality/' + hr[1] + '/' + hr[0] + '/') , "target": "_top"}})
            else:
                data_list.append(None)
        chart.add({"title": hr, 'xlink': {"href": request.build_absolute_uri(
            '/health_region_mortality/' + hr[1] + '/' + hr[0] + '/') , "target": "_top"}}, data_list)

    chart.title = "Cumulative Deaths by Health Region"

    return chart.render_data_uri()  
    
def hrs_cases_cumulative_hbar_chart(request):

    data_x_y = {}

    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[((row_data["health_region"],row_data["province"]), "cumulative_cases")
                     ] = int(row_data["cumulative_cases"])
            report_date = row_data["date_report"]
                        
    report_hrs = set()
    for key in data_x_y:
        hr = key[0]
        report_hrs.add(hr)

    sorted_report_hrs = sorted(
        report_hrs, key=lambda hr: - data_x_y.get((hr, "cumulative_cases"),0)) 
        
    chart = pygal.HorizontalStackedBar(height=400, show_legend=False,legend_at_bottom=False)
    
    for hr in sorted_report_hrs:
        data_list = []
        for group in [ "cumulative_cases" ]:
            if (hr, group) in data_x_y:
                data_list.append({'value': data_x_y[(hr, group)], 'xlink': {"href": request.build_absolute_uri(
                '/health_region/' + hr[1] + '/' + hr[0] + '/') , "target": "_top"}})
            else:
                data_list.append(None)
        chart.add({"title": hr, 'xlink': {"href": request.build_absolute_uri(
            '/health_region/' + hr[1] + '/' + hr[0] + '/') , "target": "_top"}}, data_list)

    chart.title = "Cumulative Cases by Health Region"

    return chart.render_data_uri()  
    
def provs_cumulative_cases_stackbar_chart(request):

    data_x_y = {}

    with open("data/Covid19Canada/timeseries_prov/active_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["province"], "active_cases")
                     ] = int(row_data["active_cases"])
            data_x_y[(row_data["province"], "cumulative_deaths")
                     ] = int(row_data["cumulative_deaths"])
            data_x_y[(row_data["province"], "cumulative_cases")
                     ] = int(row_data["cumulative_cases"])
            data_x_y[(row_data["province"], "cumulative_recovered")
                     ] = int(row_data["cumulative_recovered"])

    report_provinces = set()
    for key in data_x_y:
        province = key[0]
        report_provinces.add(province)

    sorted_groups = list(reversed(
        ["cumulative_cases", "cumulative_recovered", "cumulative_deaths", "active_cases"]))
    sorted_report_provinces = sorted(
        report_provinces, key=lambda k: -data_x_y[(k, "cumulative_cases")])
    chart = pygal.HorizontalStackedBar(height=400, 
        legend_at_bottom=True)
    for province in sorted_report_provinces:
        cumulative_data_list = []
        for group in sorted_groups:
            if (province, group) in data_x_y:
                cumulative_data_list.append(data_x_y[(province, group)])
            else:
                cumulative_data_list.append(None)
        chart.add({"title": province, 'xlink': {"href": request.build_absolute_uri(
            '/province_cumulative/' + province + '/') , "target": "_top"}}, cumulative_data_list)

    chart.title = "Active and cumulative cases per Province"
    chart.x_labels = sorted_groups

    return chart.render_data_uri()


def provs_cumulative_cases_stackbar_chart2():

    data_x_y = {}

    with open("data/Covid19Canada/timeseries_prov/active_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["province"], "cumulative_cases")
                     ] = int(row_data["cumulative_cases"])
            data_x_y[(row_data["province"], "active_cases")
                     ] = int(row_data["active_cases"])
            data_x_y[(row_data["province"], "cumulative_recovered")
                     ] = int(row_data["cumulative_recovered"])
            data_x_y[(row_data["province"], "cumulative_deaths")
                     ] = int(row_data["cumulative_deaths"])

    report_provinces = set()
    for key in data_x_y:
        province = key[0]
        report_provinces.add(province)

    sorted_report_provinces = sorted(
        report_provinces, key=lambda k: -data_x_y[(k, "cumulative_cases")])
    chart = pygal.StackedBar(height=400, show_legend=True, 
            legend_at_bottom_columns=3,legend_at_bottom=True)
    for group in ["cumulative_deaths", "active_cases", "cumulative_recovered"]:
        cumulative_data_list = []
        for province in sorted_report_provinces:
            if (province, group) in data_x_y:
                cumulative_data_list.append(data_x_y[(province, group)])
            else:
                cumulative_data_list.append(None)
        chart.add(group, cumulative_data_list)

    chart.title = "Active cases and related cumulative data"
    chart.x_labels = sorted_report_provinces

    return chart.render_data_uri()
    
def provs_cumulative_cases_stackbar_chart3(request):

    data_x_y = {}

    with open("data/Covid19Canada/timeseries_prov/active_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["province"], "active_cases")
                     ] = int(row_data["active_cases"])
            data_x_y[(row_data["province"], "cumulative_deaths")
                     ] = int(row_data["cumulative_deaths"])
            data_x_y[(row_data["province"], "cumulative_cases")
                     ] = int(row_data["cumulative_cases"])
            data_x_y[(row_data["province"], "cumulative_recovered")
                     ] = int(row_data["cumulative_recovered"])

    report_provinces = set()
    for key in data_x_y:
        province = key[0]
        report_provinces.add(province)

    sorted_groups = ["cumulative_cases", "cumulative_recovered", "cumulative_deaths", "active_cases"]
    sorted_report_provinces = sorted(
        report_provinces, key=lambda k: -data_x_y[(k, "cumulative_cases")])
    chart = pygal.StackedBar(height=400, legend_at_bottom=True)
    for province in sorted_report_provinces:
        cumulative_data_list = []
        for group in sorted_groups:
            if (province, group) in data_x_y:
                cumulative_data_list.append(data_x_y[(province, group)])
            else:
                cumulative_data_list.append(None)
        chart.add({"title": province, 'xlink': {"href": request.build_absolute_uri(
            '/province_cumulative/' + province + '/'), "target": "_top"}}, cumulative_data_list)

    chart.title = "Active and cumulative cases per Province"
    chart.x_labels = sorted_groups

    return chart.render_data_uri()


def provs_cumulative_cases_line_chart(request):

    with open("data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        data_x_y = {}
        provinces_list = {}
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_report"], row_data["province"])
                     ] = int(row_data["cumulative_cases"])
            provinces_list[row_data["province"]] = int(
                row_data["cumulative_cases"])

    days_report = set()
    for key in data_x_y:
        day = key[0]
        days_report.add(day)

    sorted_provinces = sorted(provinces_list.keys(),
                              key=lambda k: -provinces_list[k])
    sorted_report_days = sorted(list(days_report), key=day_month_year)
    chart = pygal.Line(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, 
        legend_at_bottom=True)
    for province in sorted_provinces:
        province_cases_per_day = []
        for day in sorted_report_days:
            if (day, province) in data_x_y:
                province_cases_per_day.append(data_x_y[(day, province)])
            else:
                province_cases_per_day.append(None)
        chart.add({"title": province, 'xlink': {"href": request.build_absolute_uri(
            '/province_hrs/' + province + '/') , "target": "_top"}}, province_cases_per_day)
    chart.title = "cumulative cases by province"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()


def provs_mortality_cumulative_line_chart():

    with open("data/Covid19Canada/timeseries_prov/mortality_timeseries_prov.csv", 'r') as file:
        data_x_y = {}
        provinces_list = {}
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_death_report"], row_data["province"])] = int(
                row_data["cumulative_deaths"])
            provinces_list[row_data["province"]] = int(
                row_data["cumulative_deaths"])

    days_report = set()
    for key in data_x_y:
        day = key[0]
        days_report.add(day)

    sorted_provinces = sorted(provinces_list.keys(),
                              key=lambda k: -provinces_list[k])
    sorted_report_days = sorted(list(days_report), key=day_month_year)
    chart = pygal.Line(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, 
                        show_legend=False, legend_at_bottom=True)
    for province in sorted_provinces:
        province_cases_per_day = []
        for day in sorted_report_days:
            if (day, province) in data_x_y:
                province_cases_per_day.append(data_x_y[(day, province)])
            else:
                province_cases_per_day.append(None)
        chart.add(province, province_cases_per_day)
    chart.title = "Cumulative COVID-19 deaths per Province"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()
    
def provs_cases_cumulative_line_chart():

    with open("data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        data_x_y = {}
        provinces_list = {}
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_report"], row_data["province"])] = int(
                row_data["cumulative_cases"])
            provinces_list[row_data["province"]] = int(
                row_data["cumulative_cases"])

    days_report = set()
    for key in data_x_y:
        day = key[0]
        days_report.add(day)

    sorted_provinces = sorted(provinces_list.keys(),
                              key=lambda k: -provinces_list[k])
    sorted_report_days = sorted(list(days_report), key=day_month_year)
    chart = pygal.Line(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, 
                        show_legend=False, legend_at_bottom=True)
    for province in sorted_provinces:
        province_cases_per_day = []
        for day in sorted_report_days:
            if (day, province) in data_x_y:
                province_cases_per_day.append(data_x_y[(day, province)])
            else:
                province_cases_per_day.append(None)
        chart.add(province, province_cases_per_day)
    chart.title = "Cumulative Cases per Province"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()


def provs_testing_compared_line_chart():

    with open("data/Covid19Canada/timeseries_prov/testing_timeseries_prov.csv", 'r') as file:
        data_x_y = {}
        provinces_list = {}
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_testing"], row_data["province"])] = int(
                row_data["cumulative_testing"])
            provinces_list[row_data["province"]] = int(
                row_data["cumulative_testing"])

    days_report = set()
    for key in data_x_y:
        day = key[0]
        days_report.add(day)

    sorted_provinces = sorted(provinces_list.keys(),
                              key=lambda k: -provinces_list[k])
    sorted_report_days = sorted(list(days_report), key=day_month_year)
    chart = pygal.Line(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, legend_at_bottom=True)
    for province in sorted_provinces:
        province_cases_per_day = []
        for day in sorted_report_days:
            if (day, province) in data_x_y:
                province_cases_per_day.append(data_x_y[(day, province)])
            else:
                province_cases_per_day.append(None)
        chart.add(province, province_cases_per_day)
    chart.title = "cumulative testing by province"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()


@cache_page(60 * 15)
def provinces_recovered_view(request):

    chart1 = pie_chart_cumulative_recovered_cases_by_provinces()
    chart2 = line_chart_cumulative_recovered_cases_by_provinces()
    charts = [chart1, chart2]

    context = {
        "charts": charts,
        "title":  "Coronavirus Cases in Canada"
    }

    return render(request, "chart/charts.html", context)


def pie_chart_cumulative_recovered_cases_by_provinces():

    with open("data/Covid19Canada/timeseries_prov/recovered_timeseries_prov.csv", 'r') as file:
        provinces_recovered = {}
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            provinces_recovered[row_data["province"]] = int(
                row_data["cumulative_recovered"])

        sorted_provinces = sorted(
            provinces_recovered.keys(), key=lambda k: -provinces_recovered[k])
        chart = pygal.Pie(height=300, show_legend=False)
        for k in sorted_provinces:
            chart.add(k, [provinces_recovered[k]])
        chart.title = "cumulative recovered by province"

    return chart.render_data_uri()


def line_chart_cumulative_recovered_cases_by_provinces():

    with open("data/Covid19Canada/timeseries_prov/recovered_timeseries_prov.csv", 'r') as file:
        data_x_y = {}
        provinces_recovered = {}
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_recovered"], row_data["province"])] = int(
                row_data["cumulative_recovered"])
            provinces_recovered[row_data["province"]] = int(
                row_data["cumulative_recovered"])

        report_day_set = set()
        for key in data_x_y:
            day = key[0]
            report_day_set.add(day)

        sorted_provinces = sorted(
            provinces_recovered.keys(), key=lambda k: -provinces_recovered[k])
        sorted_report_days = sorted(list(report_day_set), key=day_month_year)
        chart = pygal.Line(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01,
                           legend_at_bottom=True)
        for province in sorted_provinces:
            province_cases_per_day = []
            for day in sorted_report_days:
                if (day, province) in data_x_y:
                    province_cases_per_day.append(data_x_y[(day, province)])
                else:
                    province_cases_per_day.append(None)
            chart.add(province, province_cases_per_day)
        chart.title = ""
        chart.x_labels = sorted_report_days
        chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]

    return chart.render_data_uri()


def province_hrs_view(request, province):

    chart1 = prov_hrs_cases_weekly_bar_chart(request, province)
    chart4 = prov_hrs_cases_cumulative_line_chart(province)
    chart3 = prov_hrs_cumulative_cases_hbar_chart(request, province)
    chart2 = prov_hrs_cases_daily_bar_chart(request, province)
    charts = [chart1, chart2, chart3, chart4]

    context = {
        "charts": charts,
        "title":  "Coronavirus Cases in " + province
    }

    return render(request, "chart/charts.html", context)
    
def province_mortality_hrs_view(request, province):

    chart1 = prov_hrs_mortality_weekly_bar_chart(request, province)
    chart4 = prov_hrs_mortality_cumulative_line_chart(province)
    chart3 = prov_hrs_mortality_cumulative_hbar_chart(request, province)
    chart2 = prov_hrs_mortality_daily_bar_chart(request, province)
    charts = [chart1, chart2, chart3, chart4]

    context = {
        "charts": charts,
        "title":  "Coronavirus Cases in " + province
    }

    return render(request, "chart/charts.html", context)
    
    
def canada_mortality_provs_view(request, province):

    chart1 = provs_mortality_weekly_bar_chart(request, province)
    chart2 = provs_mortality_cumulative_line_chart(province)
    chart3 = provs_mortality_cumulative_bar_chart(request, province)
    chart4 = provs_mortality_daily_bar_chart(request, province)
    charts = [chart1, chart2, chart3, chart4]

    context = {
        "charts": charts,
        "title":  "Coronavirus Cases in " + province
    }

    return render(request, "chart/charts.html", context)
    

def prov_hrs_mortality_bar_chart(province):

    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        data_x_y = {}
        hrs_list = {}
        hrs_cumulative = {}
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_death_report"], row_data["health_region"])] = int(
                    row_data["deaths"])
                hrs_list[row_data["health_region"]] = int(row_data["deaths"])
                hrs_cumulative[row_data["health_region"]] = int(
                    row_data["cumulative_deaths"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_hrs = sorted(hrs_list.keys(), key=lambda k: -hrs_cumulative[k])
    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Bar(
        height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, show_legend=True, 
            legend_at_bottom=True,style=DarkSolarizedStyle)
    for hr in sorted_hrs:
        series_data_list = []
        for day in sorted_report_days:
            if (day, hr) in data_x_y:
                series_data_list.append(data_x_y[(day, hr)])
            else:
                series_data_list.append(None)
        chart.add(hr, series_data_list)
    chart.title = province + " COVID-19 deaths per Health Region"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()


def prov_hrs_cases_bar_chart(province):

    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        data_x_y = {}
        hrs_list = {}
        hrs_cumulative = {}
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_report"], row_data["health_region"])] = int(
                    row_data["cases"])
                hrs_list[row_data["health_region"]] = int(row_data["cases"])
                hrs_cumulative[row_data["health_region"]] = int(
                    row_data["cumulative_cases"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_hrs = sorted(hrs_list.keys(), key=lambda k: -hrs_cumulative[k])
    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Bar(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, show_legend=True,
        legend_at_bottom=True,explicit_size=False,style=DarkSolarizedStyle)
    for hr in sorted_hrs:
        series_data_list = []
        for day in sorted_report_days:
            if (day, hr) in data_x_y:
                series_data_list.append(data_x_y[(day, hr)])
            else:
                series_data_list.append(None)
        chart.add(hr, series_data_list)
    chart.title = province + " New Reported Cases by Health Region"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()


def province_hrs_cumulative_view(request, province):

    chart1 = prov_hrs_cases_line_chart(province)
    chart2 = prov_hrs_cumulative_cases_bar_chart(request, province)
    chart3 = prov_hrs_mortality_line_chart(province)
    chart4 = prov_hrs_mortality_cumulative_hbar_chart(request, province)
    charts = [chart1, chart2, chart3, chart4]

    context = {
        "charts": charts,
        "title":  "Coronavirus Cases in " + province
    }

    return render(request, "chart/charts.html", context)
    

def prov_hrs_cumulative_cases_and_mortality_stacked_bar_chart(request, province):

    hrs_data = {}

    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                hr = row_data["health_region"]
                hrs_data[(hr,"cumulative_cases")] = int(row_data["cumulative_cases"])
                
    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                hr = row_data["health_region"]
                hrs_data[(hr,"cumulative_deaths")] = int(row_data["cumulative_deaths"])
                
    chart = pygal.HorizontalStackedBar(height=400, legend_at_bottom=True)
    
    
    report_hrs = set()
    for key in hrs_data:
        hr = key[0]
        report_hrs.add(hr)
    
    sorted_groups = list(reversed(["cumulative_cases", "cumulative_deaths"]))
    sorted_report_hrs = sorted(
        report_hrs, key=lambda hr: -hrs_data.get((hr,"cumulative_cases"),0) - hrs_data.get((hr,"cumulative_deaths"),0))
        
    chart = pygal.HorizontalStackedBar(height=400, legend_at_bottom=True, show_x_labels=True)
    for hr in sorted_report_hrs:
        data_list = []
        for group in sorted_groups:
            if (hr, group) in hrs_data:
                data_list.append(hrs_data[(hr, group)])
            else:
                data_list.append(None)
        chart.add({"title": hr, 'xlink': {"href": request.build_absolute_uri(
            '/health_region/' + province + '/' + hr + '/'), "target": "_top"}}, data_list)

    chart.x_labels = sorted_groups
    chart.title = province + " Cumulative Cases and Deaths by Health Region"
    return chart.render_data_uri()    


def prov_hrs_cumulative_cases_hbar_chart(request, province):

    hrs_data = {}
    groups_list = {}
    hrs_latest_report_date = {}

    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                hr = row_data["health_region"]
                hrs_data[hr] = int(row_data["cumulative_cases"])
                hrs_latest_report_date[hr] = row_data["date_report"]

    chart = pygal.HorizontalStackedBar(height=400, legend_at_bottom=True)

    sorted_hr = sorted(hrs_data.keys(), key=lambda hr: -hrs_data[hr])
    for hr in sorted_hr:
        chart.add({"title": hr, 'xlink': {"href": request.build_absolute_uri(
            '/health_region/' + province + '/' + hr + '/') , "target": "_top"}}, [ {"value": hrs_data[hr],'xlink': {"href": request.build_absolute_uri(
            '/health_region/' + province + '/' + hr + '/') , "target": "_top"} }])
    chart.title = province + " cumulative cases per Health Region"
    return chart.render_data_uri()
    


def prov_hrs_latest_cases_and_mortality_bar_chart(request, province):

    hrs_data = {}
    hrs_latest_cases_report_date = ""
    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                hr = row_data["health_region"]
                hrs_data[(hr,"cases")] = int(row_data["cases"])
                hrs_latest_cases_report_date = row_data["date_report"]

    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                hr = row_data["health_region"]
                hrs_data[(hr,"deaths")] = int(row_data["deaths"])
                hrs_latest_death_report_date = row_data["date_death_report"]
                
                
    report_hrs = set()
    for key in hrs_data:
        hr = key[0]
        report_hrs.add(hr)
    
    sorted_groups = list(reversed(["cases", "deaths"]))
    sorted_report_hrs = sorted(
        report_hrs, key=lambda hr: -hrs_data.get((hr,"cases"),0) - hrs_data.get((hr,"deaths"),0))
    chart = pygal.HorizontalStackedBar(height=400, legend_at_bottom=True, show_x_labels=True)
    for hr in sorted_report_hrs:
        data_list = []
        for group in sorted_groups:
            if (hr, group) in hrs_data:
                data_list.append({"value": hrs_data[(hr, group)], 'xlink': { "href": request.build_absolute_uri('/health_region/' + province + '/' + hr + '/'), "target": "_top" }})
            else:
                data_list.append(None)
        chart.add({"title": hr, 'xlink': { "href": request.build_absolute_uri(
            '/health_region/' + province + '/' + hr + '/'), "target": "_top" }}, data_list)

    chart.title = province + " Cases and Deaths on " + hrs_latest_cases_report_date
    chart.x_labels = sorted_groups
    return chart.render_data_uri()

def prov_hrs_mortality_cumulative_hbar_chart(request, province):

    hrs_data = {}
    groups_list = {}
    hrs_latest_report_date = {}

    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                hr = row_data["health_region"]
                hrs_data[hr] = int(row_data["cumulative_deaths"])
                hrs_latest_report_date[hr] = row_data["date_death_report"]

    chart = pygal.HorizontalStackedBar(height=400, legend_at_bottom=True)

    sorted_hr = sorted(hrs_data.keys(), key=lambda hr: -hrs_data[hr])
    for hr in sorted_hr:
        chart.add({"title": hr, 'xlink': {"href": request.build_absolute_uri(
            '/health_region_mortality/' + province + '/' + hr + '/'), "target": "_top"}}, [hrs_data[hr]])
    chart.title = province + " cumulative deaths per Health Region"
    chart.x_labels = ["cumulative_deaths"]
    return chart.render_data_uri()

def prov_cases_and_mortality_bar_chart(request, province):

    data_x_y = {}
    
    with open("data/Covid19Canada/timeseries_prov/mortality_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_death_report"], "deaths")] = int(
                    row_data["deaths"])
    
    with open("data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_report"], "cases")
                         ] = int(row_data["cases"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Bar(height=400, 
        show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, 
        legend_at_bottom=True, show_legend=True)
        
    xlinks = {"cases": "province_hrs", "deaths": "province_mortality_hrs"}    
    for group in [ "deaths" ,"cases"]:
        data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                data_list.append(data_x_y[(day, group)])
            else:
                data_list.append(None)
        chart.add({"title": group ,'xlink': {"href": request.build_absolute_uri(
            '/'+ xlinks[group] + '/' + province + '/'), "target": "_top"}} , data_list)

    chart.title = "Cases and Deaths in {}".format(province)
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()
    
def prov_cases_and_mortality_weekly_bar_chart(request, province):

    data_x_y = {}
    
    with open("data/Covid19Canada/timeseries_prov/mortality_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                year_week = report_date_to_year_week(row_data["date_death_report"])
                if (year_week,"deaths") not in data_x_y:
                    data_x_y[(year_week,"deaths")] = 0
                data_x_y[(year_week,"deaths")] += int(row_data["deaths"])
                    
    with open("data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                year_week = report_date_to_year_week(row_data["date_report"])
                if (year_week,"cases") not in data_x_y:
                    data_x_y[(year_week,"cases")] = 0
                data_x_y[(year_week,"cases")] += int(row_data["cases"])

    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart = pygal.Bar(height=400,legend_at_bottom=True, x_title="Week number")
    xlinks = {"cases": "province_hrs", "deaths": "province_mortality_hrs"}
    for group in ["deaths", "cases"]:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week,group) in data_x_y:
                timeseries_data.append(data_x_y[(week,group)])
            else:
                timeseries_data.append(None)
        chart.add({"title": group , 'xlink': {"href": request.build_absolute_uri(
            '/'+ xlinks[group] + '/' + province + '/'), "target": "_top"} } , timeseries_data)

    chart.title = "Weekly New Cases and Deaths in {}".format(province)
    chart.x_labels = [ w[1] for w in sorted_report_weeks ] 
  
    return chart.render_data_uri()
    
def prov_cases_and_testing_weekly_bar_chart(province):

    data_x_y = {}
    
    with open("data/Covid19Canada/timeseries_prov/testing_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                year_week = report_date_to_year_week(row_data["date_testing"])
                if (year_week,"testing") not in data_x_y:
                    data_x_y[(year_week,"testing")] = 0
                data_x_y[(year_week,"testing")] += int(row_data["testing"])
                    
    with open("data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                year_week = report_date_to_year_week(row_data["date_report"])
                if (year_week,"cases") not in data_x_y:
                    data_x_y[(year_week,"cases")] = 0
                data_x_y[(year_week,"cases")] += int(row_data["cases"])

    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart = pygal.Bar(height=400,legend_at_bottom=True, x_title ="Week Number")
    for group in ["testing", "cases"]:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week,group) in data_x_y:
                timeseries_data.append(data_x_y[(week,group)])
            else:
                timeseries_data.append(None)
        chart.add(group, timeseries_data)

    chart.title = "Weekly Cases and Testing in {}".format(province)
    chart.x_labels = [ w[1] for w in sorted_report_weeks ] 
  
    return chart.render_data_uri()
        

def prov_cases_bar_chart(province):

    data_x_y = {}
    groups_list = {}
    

    with open("data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_report"], "cases")
                         ] = int(row_data["cases"])
                groups_list["cases"] = int(row_data["cases"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_groups = sorted(groups_list.keys(), key=lambda k: -groups_list[k])
    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Bar(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, show_legend=False)
    for group in sorted_groups:
        data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                data_list.append(data_x_y[(day, group)])
            else:
                data_list.append(None)
        chart.add("", data_list)

    chart.title = "Cases in {} by Reported Date".format(province)
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()
    

def prov_testing_bar_chart(province):

    with open("data/Covid19Canada/timeseries_prov/testing_timeseries_prov.csv", 'r') as file:
        data_x_y = {}
        provinces_list = {}
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_testing"], row_data["province"])] = int(
                    row_data["testing"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Bar(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, show_legend=False)
    province_series_data = []
    for day in sorted_report_days:
        if (day, province) in data_x_y:
            province_series_data.append(data_x_y[(day, province)])
        else:
            province_series_data.append(None)
    chart.add(province, province_series_data)
    chart.title = "Daily testing in " + province
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()


def prov_cases_and_testing_bar_chart(province):

    data_x_y = {}
    groups_list = {}

    with open("data/Covid19Canada/timeseries_prov/testing_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_testing"], "testing")
                         ] = int(row_data["testing"])

    with open("data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_report"], "cases")
                         ] = int(row_data["cases"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Bar(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, legend_at_bottom=True)
    for group in ["cases", "testing"]:
        data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                data_list.append(data_x_y[(day, group)])
            else:
                data_list.append(None)
        chart.add(group, data_list)

    chart.title = province + " Cases and Testing"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]

    return chart.render_data_uri()
    

def prov_cumulative_cases_lines_chart(province):

    data_x_y = {}

    with open("data/Covid19Canada/timeseries_prov/active_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_active"], "active_cases")
                         ] = int(row_data["active_cases"])
                data_x_y[(row_data["date_active"], "cumulative_cases")] = int(
                    row_data["cumulative_cases"])
                data_x_y[(row_data["date_active"], "cumulative_recovered")] = int(
                    row_data["cumulative_recovered"])
                data_x_y[(row_data["date_active"], "cumulative_deaths")] = int(
                    row_data["cumulative_deaths"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Line(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, legend_at_bottom=True)
    for group in ["cumulative_deaths", "cumulative_cases", "cumulative_recovered", "active_cases"]:
        cumulative_data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                cumulative_data_list.append(data_x_y[(day, group)])
            else:
                cumulative_data_list.append(None)
        chart.add(group, cumulative_data_list)

    chart.title = province + " cumulative cases data"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]

    return chart.render_data_uri()


def prov_cumulative_testing_line_chart(province):
    with open("data/Covid19Canada/timeseries_prov/testing_timeseries_prov.csv", 'r') as file:
        data_x_y = {}
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_testing"], row_data["province"])] = int(
                    row_data["cumulative_testing"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Line(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, show_legend=False)
    province_series_data = []
    for day in sorted_report_days:
        if (day, province) in data_x_y:
            province_series_data.append(data_x_y[(day, province)])
        else:
            province_series_data.append(None)
    chart.add(province + " cumulative testing", province_series_data)
    chart.title = "Cumulative testing in " + province
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()


def prov_hrs_cumulative_mortality_line_chart(province):

    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        data_x_y = {}
        hrs_list = {}
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_death_report"], row_data["health_region"])] = int(
                    row_data["cumulative_deaths"])
                hrs_list[row_data["health_region"]] = int(
                    row_data["cumulative_deaths"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_hrs = sorted(hrs_list.keys(), key=lambda k: -hrs_list[k])
    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Line(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, dots_size=2,
        legend_at_bottom=True,style=DarkSolarizedStyle)
    for hr in sorted_hrs:
        series_data_list = []
        for day in sorted_report_days:
            if (day, hr) in data_x_y:
                series_data_list.append(data_x_y[(day, hr)])
            else:
                series_data_list.append(None)
        chart.add(hr, series_data_list)
    chart.title = "Cumulative deaths for Health Regions in " + province
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()


def prov_hrs_cases_cumulative_line_chart(province):

    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        data_x_y = {}
        hrs_list = {}
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_report"], row_data["health_region"])] = int(
                    row_data["cumulative_cases"])
                hrs_list[row_data["health_region"]] = int(
                    row_data["cumulative_cases"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_hrs = sorted(hrs_list.keys(), key=lambda k: -hrs_list[k])
    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Line(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, dots_size=2,
        show_legend=False)
    for hr in sorted_hrs:
        series_data_list = []
        for day in sorted_report_days:
            if (day, hr) in data_x_y:
                series_data_list.append(data_x_y[(day, hr)])
            else:
                series_data_list.append(None)
        chart.add(hr, series_data_list)
    chart.title = "Cumulative cases for health regions in " + province
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()
    
    
def canada_hrs_cases_cumulative_line_chart(request):

    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        data_x_y = {}
        hrs_list = {}
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            hr = (row_data["health_region"],row_data["province"])
            data_x_y[(row_data["date_report"], hr)] = int(
                row_data["cumulative_cases"])
            hrs_list[hr] = int(row_data["cumulative_cases"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_hrs = sorted(hrs_list.keys(), key=lambda k: -hrs_list[k])
    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Line(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, dots_size=2,
        show_legend=True,legend_at_bottom=True)
    for hr in sorted_hrs[:10]:
        series_data_list = []
        for day in sorted_report_days:
            if (day, hr) in data_x_y:
                series_data_list.append(data_x_y[(day, hr)])
            else:
                series_data_list.append(None)
        chart.add(hr[0], series_data_list)
    chart.title = "Cumulative cases for health regions"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()    
    
def prov_hrs_mortality_cumulative_line_chart(province):

    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        data_x_y = {}
        hrs_list = {}
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_death_report"], row_data["health_region"])] = int(
                    row_data["cumulative_deaths"])
                hrs_list[row_data["health_region"]] = int(
                    row_data["cumulative_deaths"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_hrs = sorted(hrs_list.keys(), key=lambda k: -hrs_list[k])
    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Line(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, dots_size=2,
        show_legend=False)
    for hr in sorted_hrs:
        series_data_list = []
        for day in sorted_report_days:
            if (day, hr) in data_x_y:
                series_data_list.append(data_x_y[(day, hr)])
            else:
                series_data_list.append(None)
        chart.add(hr, series_data_list)
    chart.title = "Cumulative deaths for health regions in " + province
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()

@cache_page(60 * 15)
def health_region_view(request, province, health_region):


    chart1 = hr_cases_and_mortality_weekly_bar_chart(province, health_region)
    chart2 = hr_cases_and_mortality_bar_chart(province, health_region)
    chart3 = hr_cumulative_hbar_chart(request, province, health_region)
    chart4 = hr_cumulative_line_chart(request, province, health_region)

    charts = [chart1, chart2, chart3, chart4]

    context = {
        "charts": charts,
        "title":  "Coronavirus in " + health_region + ' (' + province + ')'
    }

    return render(request, "chart/charts.html", context)
    

@cache_page(60 * 15)
def health_region_mortality_view(request, province, health_region):

    chart1 = hr_mortality_weekly_bar_chart(province, health_region)
    chart2 = hr_mortality_bar_chart(province, health_region)
    chart3 = hr_mortality_hbar_chart(province, health_region)
    chart4 = hr_mortality_cumulative_line_chart(province, health_region)

    charts = [chart1, chart2, chart3, chart4]

    context = {
        "charts": charts,
        "title":  "Coronavirus mortality in " + health_region + ' (' + province + ')'
    }

    return render(request, "chart/charts.html", context)


def hr_cases_and_mortality_bar_chart(province, health_region):

    data_x_y = {}
    
    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y[(row_data["date_death_report"], "deaths")] = int(
                    row_data["deaths"])

    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y[(row_data["date_report"], "cases")
                         ] = int(row_data["cases"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Bar(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, 
        legend_at_bottom=True, show_legend=True)
    for group in [ "deaths", "cases"]:
        data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                data_list.append(data_x_y[(day, group)])
            else:
                data_list.append(None)
        chart.add(group, data_list)

    chart.title = health_region + " (" + province + ") new cases and deaths by date"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()
    
    
def hr_mortality_bar_chart(province, health_region):

    data_x_y = {}
    
    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y[(row_data["date_death_report"], "deaths")] = int(
                    row_data["deaths"])


    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Bar(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, 
        legend_at_bottom=True, show_legend=True)
    for group in [ "deaths" ]:
        data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                data_list.append(data_x_y[(day, group)])
            else:
                data_list.append(None)
        chart.add(group, data_list)

    chart.title = health_region + " (" + province + ")  deaths by date"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()
    

def hr_cases_and_mortality_weekly_bar_chart(province, health_region):

    data_x_y = {}
    
    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                year_week = report_date_to_year_week(row_data["date_death_report"])
                if (year_week,"deaths") not in data_x_y:
                    data_x_y[(year_week,"deaths")] = 0
                data_x_y[(year_week,"deaths")] += int(row_data["deaths"])
                    
    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                year_week = report_date_to_year_week(row_data["date_report"])
                if (year_week,"cases") not in data_x_y:
                    data_x_y[(year_week,"cases")] = 0
                data_x_y[(year_week,"cases")] += int(row_data["cases"])

    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart = pygal.Bar(height=400,legend_at_bottom=True, x_title="Week Number")
    for group in [ "deaths", "cases"]:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week,group) in data_x_y:
                timeseries_data.append(data_x_y[(week,group)])
            else:
                timeseries_data.append(None)
        chart.add(group, timeseries_data)

    chart.title = health_region + " (" + province + ") Weekly cumulative Cases and Deaths"
    chart.x_labels = [ w[1] for w in sorted_report_weeks ] 
    return chart.render_data_uri()   
    
def hr_mortality_weekly_bar_chart(province, health_region):

    data_x_y = {}
    
    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                year_week = report_date_to_year_week(row_data["date_death_report"])
                if (year_week,"deaths") not in data_x_y:
                    data_x_y[(year_week,"deaths")] = 0
                data_x_y[(year_week,"deaths")] += int(row_data["deaths"])
                    

    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart = pygal.Bar(height=400,legend_at_bottom=True)
    
    for group in ["deaths"]:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week,group) in data_x_y:
                timeseries_data.append(data_x_y[(week,group)])
            else:
                timeseries_data.append(None)
        chart.add(group, timeseries_data)

    chart.title = health_region + " (" + province + ") Weekly cumulative Deaths"
    chart.x_labels = [ w[1] for w in sorted_report_weeks ] 
    return chart.render_data_uri()   
        

def hr_cases_bar_chart(province, health_region):

    data_x_y = {}
    
    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y[(row_data["date_report"], "cases")
                         ] = int(row_data["cases"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Bar(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, 
         show_legend=False)
        
    for group in ["cases"]:
        data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                data_list.append(data_x_y[(day, group)])
            else:
                data_list.append(None)
        chart.add(group, data_list)

    chart.title = health_region + " (" + province + ") daily cases"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()


def hr_mortality_bar_chart(province, health_region):

    data_x_y = {}
    
    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y[(row_data["date_report"], "cases")
                         ] = int(row_data["cases"])
    
    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y[(row_data["date_death_report"], "deaths")] = int(
                    row_data["deaths"])
            
    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Bar(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, show_legend=False)
    for group in [ "deaths"]:
        data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                data_list.append(data_x_y[(day, group)])
            else:
                data_list.append(None)
        chart.add(group, data_list)

    chart.title = health_region + " (" + province + ") deaths"
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()


def hr_cumulative_line_chart(request, province, health_region):

    data_x_y = {}

    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y[(row_data["date_death_report"], "cumulative_deaths")] = int(
                    row_data["cumulative_deaths"])

    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y[(row_data["date_report"], "cumulative_cases")] = int(
                    row_data["cumulative_cases"])

    report_day_set = set()
    for key in data_x_y:
        day = key[0]
        report_day_set.add(day)

    sorted_report_days = sorted(list(report_day_set), key=day_month_year)
    chart = pygal.Line(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, legend_at_bottom=True)
    for group in [ "cumulative_deaths" , "cumulative_cases" ]:
        cumulative_data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                cumulative_data_list.append(data_x_y[(day, group)])
            else:
                cumulative_data_list.append(None)
        if group == "cumulative_cases":
            chart.add(group, cumulative_data_list)
        elif group == "cumulative_deaths":
            chart.add({"title": group, 'xlink': {"href": request.build_absolute_uri(
            '/health_region_mortality/' + province + '/' + health_region + '/'), "target": "_top"}}, cumulative_data_list)
            

    chart.title = health_region + " (" + province + ") cumulative cases data"

    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()


def hr_mortality_cumulative_line_chart(province, health_region):

    data_x_y = {}

    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y[(row_data["date_death_report"], "cumulative_deaths")] = int(
                    row_data["cumulative_deaths"])

    report_day_set = set()
    for key in data_x_y:
        day = key[0]
        report_day_set.add(day)

    sorted_report_days = sorted(list(report_day_set), key=day_month_year)
    chart = pygal.Line(height=400, show_x_labels=True, show_minor_x_labels=False, x_label_rotation=0.01, legend_at_bottom=True)
    for group in [ "cumulative_deaths"  ]:
        cumulative_data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                cumulative_data_list.append(data_x_y[(day, group)])
            else:
                cumulative_data_list.append(None)
        chart.add(group, cumulative_data_list)

    chart.title = health_region + " (" + province + ") cumulative deaths"

    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    return chart.render_data_uri()


def hr_cumulative_hbar_chart(request, province, health_region):

    data_x_y = {}

    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y["cumulative_deaths"] = int(row_data["cumulative_deaths"])

    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y["cumulative_cases"] = int(row_data["cumulative_cases"])

    chart = pygal.HorizontalBar(height=400, show_x_labels=True, legend_at_bottom=True)
    for group in [ "cumulative_deaths" , "cumulative_cases" ]:
        cumulative_data_list = []
        if group in data_x_y:
            cumulative_data_list.append(data_x_y[group])
        else:
            cumulative_data_list.append(None)
        if group == "cumulative_cases":
            chart.add(group, cumulative_data_list)
        elif group == "cumulative_deaths":
            chart.add({"title": group, 'xlink': {"href": request.build_absolute_uri(
            '/health_region_mortality/' + province + '/' + health_region + '/'), "target": "_top"}}, cumulative_data_list)

    chart.title = health_region + " (" + province + ") cumulative Caaes and Deaths"

    return chart.render_data_uri()
    

def hr_mortality_hbar_chart(province, health_region):

    data_x_y = {}

    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y["cumulative_deaths"] = int(row_data["cumulative_deaths"])


    chart = pygal.HorizontalBar(height=400, show_x_labels=True, legend_at_bottom=True)
    for group in [ "cumulative_deaths" ]:
        cumulative_data_list = []
        if group in data_x_y:
            cumulative_data_list.append(data_x_y[group])
        else:
            cumulative_data_list.append(None)
        chart.add(group, cumulative_data_list)

    chart.title = health_region + " (" + province + ") cumulative Deaths"

    return chart.render_data_uri()


@cache_page(60 * 15)
def canada_hrs_view(request):

    #chart3 = hrs_latest_cases_and_mortality_stackbar_chart(request)
    chart1 = hrs_latest_mortality_hbar_chart(request)
    chart3 = hrs_latest_cases_hbar_chart(request)
    chart2 = hrs_mortality_cumulative_hbar_chart(request)
    chart4 = hrs_cases_cumulative_hbar_chart(request)
    charts = [chart1, chart2, chart3, chart4]

    context = {
        "charts": charts,
        "title":  "Coronavirus Cases in Canada"
    }

    return render(request, "chart/charts.html", context)


def provs_hrs_cases_pie_chart(request):

    hrs_data = {}
    hrs_latest_reprt_date = {}
    prov_hrs = {}

    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            hrs_data[(row_data["province"], row_data["health_region"])] = int(
                row_data["cases"])
            hrs_latest_reprt_date[(
                row_data["province"], row_data["health_region"])] = row_data["date_report"]
            province = row_data["province"]
            if province not in prov_hrs:
                prov_hrs[province] = set()
            else:
                prov_hrs[province].add(row_data["health_region"])

    sorted_provs = sorted(prov_hrs.keys(), key=lambda province: -sum([
        hrs_data[province, hr] for hr in prov_hrs[province]]))

    chart = pygal.Pie(height=400,legend_box_size=18)

    for province in sorted_provs:
        prov_hrs_data = []
        for hr in prov_hrs[province]:
            prov_hrs_data.append({'value': hrs_data[(province, hr)], 'label': hr, 'xlink': request.build_absolute_uri(
                '/health_region/' + province + '/' + hr + '/')})
        chart.add({"title": province, 'xlink': { "href": request.build_absolute_uri(
            '/province_hrs/' + province + '/') , "target": "_top"}}, sorted(prov_hrs_data, key=lambda hr: -hr["value"]))
    chart.title = "Latest new cases on " + \
        str(set(hrs_latest_reprt_date.values())) + " per Health Region"
    return chart.render_data_uri()


def provs_hrs_cumulative_cases_pie_chart(request):

    hrs_data = {}
    hrs_latest_reprt_date = {}
    prov_hrs = {}

    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            hrs_data[(row_data["province"], row_data["health_region"])] = int(
                row_data["cumulative_cases"])
            hrs_latest_reprt_date[(
                row_data["province"], row_data["health_region"])] = row_data["date_report"]
            province = row_data["province"]
            if province not in prov_hrs:
                prov_hrs[province] = set()
            else:
                prov_hrs[province].add(row_data["health_region"])

    sorted_provs = sorted(prov_hrs.keys(), key=lambda province: -sum([
        hrs_data[province, hr] for hr in prov_hrs[province]]))

    chart = pygal.Pie(height=400, show_legend=True, truncate_legend=-1)

    for province in sorted_provs:
        prov_hrs_data = []
        for hr in prov_hrs[province]:
            prov_hrs_data.append({'value': hrs_data[(province, hr)], 'label': hr, 'xlink': {"href": request.build_absolute_uri(
                '/health_region/' + province + '/' + hr + '/') , "target": "_top"}})
        chart.add({"title": province, 'xlink': { "href": request.build_absolute_uri(
            '/province_hrs/' + province + '/'), "target": "_top"}}, sorted(prov_hrs_data, key=lambda hr: -hr["value"]))
    chart.title = "Cumulative cases per Province and Health Region"
    return chart.render_data_uri()


@cache_page(60 * 15)
def provs_simple_view(request):

    chart1 = provs_new_cases_bar_chart(request)
    #chart2 = provs_cumulative_cases_pie_chart(request)
    charts = [chart1]

    context = {
        "charts": charts,
        "title":  "Coronavirus New Cases Upadte"
    }

    return render(request, "chart/charts.html", context)


def provs_cumulative_cases_pie_chart(request):

    provs_data = {}
    groups_list = {}
    provs_latest_report_date = {}

    with open("data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            province = row_data["province"]
            provs_data[province] = int(row_data["cumulative_cases"])
            provs_latest_report_date[province] = row_data["date_report"]

    chart = pygal.Pie(height=400)

    sorted_provs = sorted(
        provs_data.keys(), key=lambda province: -provs_data[province])
    for province in sorted_provs:
        if provs_data[province] != 0:
            chart.add({"title": province, 'xlink': { "href": request.build_absolute_uri('/province/' + province + '/'), "target": "_top"}},
                      [{"value": provs_data[province], 'xlink': { "href": request.build_absolute_uri('/province/' + province + '/'), "target": "_top"}}])
    chart.title = "Cumulative cases per Province"
    return chart.render_data_uri()


def provs_new_cases_bar_chart(request):

    provs_data = {}
    provs_latest_report_date = {}

    with open("data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            province = row_data["province"]
            provs_data[province] = int(row_data["cases"])
            provs_latest_report_date[province] = row_data["date_report"]

    chart = pygal.Bar(height=400, legend_at_bottom=True)

    sorted_provs = sorted(
        provs_data.keys(), key=lambda province: -provs_data[province])
    for province in sorted_provs:
        chart.add({"title": province, 'xlink': { "href": request.build_absolute_uri(
            '/province/' + province + '/'), "target": "_top"}}, [{"value": provs_data[province]}])
    chart.title = "New cases per Province on " + \
        str(set(provs_latest_report_date.values()))[2:-2]
    return chart.render_data_uri()


def day_month_year(date):
    l = date.split("-")
    return l[2] + l[1] + l[0]


def display_month_day(date):
    l = date.split("-")
    return date
    
def report_date_to_year_week(date):
    l = date.split("-")
    d = datetime.date(int(l[2]),int(l[1]),int(l[0]))
    cal = d.isocalendar()
    return cal[:2] 
