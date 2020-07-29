import pygal
import csv
from collections import Counter
from django.shortcuts import render
from django.views.decorators.cache import cache_page
import datetime


@cache_page(60 * 15)
def home_view(request):

    chart1 = canada_cases_bar_chart()
    chart2 = canada_cases_and_testing_bar_chart()
    chart3 = canada_cumulative_cases_lines_chart()
    charts = [chart1]

    context = {
        "charts": charts,
        "title":  "Coronavirus Cases in CANADA"
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
    chart = pygal.Bar(height=320, show_x_labels=False, show_legend=False)
    for group in sorted_groups:
        data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                data_list.append(data_x_y[(day, group)])
            else:
                data_list.append(None)
        chart.add("", data_list)

    chart.title = "Cases in Canada by Reported Date"
    chart.x_labels = sorted_report_days
    return chart.render_data_uri()


def canada_cases_and_testing_bar_chart():

    data_x_y = {}
    groups_list = {}

    with open("data/Covid19Canada/timeseries_canada/testing_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_testing"], "testing")
                     ] = int(row_data["testing"])
            groups_list["testing"] = int(row_data["testing"])

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
    chart = pygal.Bar(height=300, show_x_labels=False, legend_at_bottom=True)
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
    chart = pygal.Bar(height=320, show_x_labels=False, show_legend=False)
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
    chart = pygal.Line(height=320, show_x_labels=False, show_legend=False)
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
    chart = pygal.Line(height=300, show_x_labels=False, legend_at_bottom=True)
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

    return chart.render_data_uri()


@cache_page(60 * 15)
def province_cases_view(request, province):

    chart1 = prov_cases_bar_chart(province)
    chart2 = prov_cases_and_testing_bar_chart(province)

    charts = [chart1, chart2]

    context = {
        "charts": charts,
        "title":  "Province cases view by Reported Date"
    }

    return render(request, "chart/charts.html", context)


@cache_page(60 * 15)
def province_cumulative_view(request, province):

    chart1 = prov_cumulative_cases_lines_chart(province)
    chart2 = prov_hrs_cases_cumulative_line_chart(province)
    chart3 = prov_cumulative_testing_line_chart(province)

    charts = [chart1, chart2, chart3]

    context = {
        "charts": charts,
        "title":  "Province cumulative view"
    }

    return render(request, "chart/charts.html", context)


@cache_page(60 * 15)
def provinces_testing_view(request):

    chart1 = provs_testing_stacked_bar_chart()
    chart2 = provs_testing_compared_line_chart()
    charts = [chart1, chart2]

    context = {
        "charts": charts,
        "title":  "Coronavirus Testing in CANADA"
    }

    return render(request, "chart/charts.html", context)


@cache_page(60 * 15)
def provinces_view(request):

    chart1 = provs_cases_line_chart(request)
    chart2 = provs_cumulative_cases_line_chart(request)
    chart3 = provs_cumulative_cases_stackbar_chart(request)
    chart4 = provs_cumulative_cases_stackbar_chart2()

    charts = [chart1, chart2, chart3, chart4]

    context = {
        "charts": charts,
        "title":  "Coronavirus Cases per Province"
    }

    return render(request, "chart/charts.html", context)


@cache_page(60 * 15)
def provinces_mortality_view(request):

    chart1 = provs_mortality_cumulative_line_chart()
    chart2 = provs_mortality_cumulative_bar_chart(request)

    charts = [chart1, chart2]

    context = {
        "charts": charts,
        "title":  "Coronavirus mortality per Province"
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

    chart = pygal.Bar(height=260, legend_at_bottom=True)

    sorted_provs = sorted(
        provs_data.keys(), key=lambda province: -provs_data[province])
    for province in sorted_provs:
        chart.add({"title": province, 'xlink': request.build_absolute_uri(
            '/province/' + province + '/')}, [provs_data[province]])
    chart.title = "Cumulative reported cases per Province"
    return chart.render_data_uri()


def provs_mortality_cumulative_bar_chart(request):

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

    chart = pygal.Bar(height=320, legend_at_bottom=True)

    sorted_provs = sorted(
        provs_data.keys(), key=lambda province: -provs_data[province])
    for province in sorted_provs:
        chart.add(province, [provs_data[province]])
    chart.title = "cumulative mortality per Province"
    return chart.render_data_uri()


def provs_testing_stacked_bar_chart():

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
    chart = pygal.Line(height=300, show_x_labels=False,
                       show_legend=False, show_dots=True, dots_size=2)
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
    chart = pygal.Line(height=320, show_x_labels=False,
                       legend_at_bottom=True, show_dots=True, dots_size=1)
    for province in sorted_provinces:
        province_cases_per_day = []
        for day in sorted_report_days:
            if (day, province) in data_x_y:
                province_cases_per_day.append(data_x_y[(day, province)])
            else:
                province_cases_per_day.append(None)
        chart.add({"title": province, 'xlink': request.build_absolute_uri(
            '/province_cases/' + province + '/')}, province_cases_per_day)
    chart.title = "Daily reported cases by province"
    chart.x_labels = sorted_report_days
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
        height=360, show_x_labels=False, legend_at_bottom=False)
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
        ["cumulative_cases", "cumulative_deaths", "cumulative_recovered", "active_cases"]))
    sorted_report_provinces = sorted(
        report_provinces, key=lambda k: -data_x_y[(k, "cumulative_cases")])
    chart = pygal.HorizontalStackedBar(height=260, legend_at_bottom=True)
    for province in sorted_report_provinces:
        cumulative_data_list = []
        for group in sorted_groups:
            if (province, group) in data_x_y:
                cumulative_data_list.append(data_x_y[(province, group)])
            else:
                cumulative_data_list.append(None)
        chart.add({"title": province, 'xlink': request.build_absolute_uri(
            '/province_cumulative/' + province + '/')}, cumulative_data_list)

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
    chart = pygal.StackedBar(
        height=280, show_legend=True, legend_at_bottom=True)
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
    chart = pygal.Line(height=300, show_x_labels=False, legend_at_bottom=True)
    for province in sorted_provinces:
        province_cases_per_day = []
        for day in sorted_report_days:
            if (day, province) in data_x_y:
                province_cases_per_day.append(data_x_y[(day, province)])
            else:
                province_cases_per_day.append(None)
        chart.add({"title": province, 'xlink': request.build_absolute_uri(
            '/province/' + province + '/')}, province_cases_per_day)
    chart.title = "cumulative cases by province"
    chart.x_labels = sorted_report_days
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
    chart = pygal.Line(height=260, show_x_labels=False, show_legend=False)
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
    chart = pygal.Line(height=360, show_x_labels=False, legend_at_bottom=True)
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
        chart = pygal.Line(height=360, show_x_labels=False,
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

    return chart.render_data_uri()


@cache_page(60 * 15)
def province_view(request, province):

    chart1 = prov_cumulative_cases_lines_chart(province)
    chart2 = prov_cumulative_testing_line_chart(province)
    chart3 = prov_hrs_cases_cumulative_line_chart(province)
    chart4 = prov_hrs_cumulative_mortality_line_chart(province)

    charts = [chart1, chart2, chart3, chart4]

    context = {
        "charts": charts,
        "title":  "Coronavirus Cases in " + province
    }

    return render(request, "chart/charts.html", context)


def province_hrs_view(request, province):

    chart1 = prov_hrs_cases_bar_chart(province)
    chart2 = prov_hrs_cumulative_cases_bar_chart(request, province)
    chart3 = prov_hrs_mortality_bar_chart(province)
    chart4 = prov_hrs_mortality_cumulative_bar_chart(request, province)
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
    chart = pygal.StackedBar(
        height=320, show_x_labels=False, show_legend=False)
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
    chart = pygal.StackedBar(
        height=320, show_x_labels=False, show_legend=False)
    for hr in sorted_hrs:
        series_data_list = []
        for day in sorted_report_days:
            if (day, hr) in data_x_y:
                series_data_list.append(data_x_y[(day, hr)])
            else:
                series_data_list.append(None)
        chart.add(hr, series_data_list)
    chart.title = province + " cases per Health Region"
    chart.x_labels = sorted_report_days
    return chart.render_data_uri()


def province_hrs_cumulative_view(request, province):

    chart1 = prov_hrs_cases_compared_line_chart(province)
    chart2 = prov_hrs_cumulative_cases_bar_chart(request, province)
    chart3 = prov_hrs_mortality_compared_line_chart(province)
    chart4 = prov_hrs_mortality_cumulative_bar_chart(request, province)
    charts = [chart1, chart2, chart3, chart4]

    context = {
        "charts": charts,
        "title":  "Coronavirus Cases in " + province
    }

    return render(request, "chart/charts.html", context)


def prov_hrs_cumulative_cases_bar_chart(request, province):

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

    chart = pygal.Bar(height=380, legend_at_bottom=True)

    sorted_hr = sorted(hrs_data.keys(), key=lambda hr: -hrs_data[hr])
    for hr in sorted_hr:
        chart.add({"title": hr, 'xlink': request.build_absolute_uri(
            '/health_region/' + province + '/' + hr + '/')}, [hrs_data[hr]])
    chart.title = province + " cumulative cases per Health Region"
    return chart.render_data_uri()


def prov_hrs_mortality_cumulative_bar_chart(request, province):

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

    chart = pygal.Bar(height=380, legend_at_bottom=True)

    sorted_hr = sorted(hrs_data.keys(), key=lambda hr: -hrs_data[hr])
    for hr in sorted_hr:
        chart.add({"title": hr, 'xlink': request.build_absolute_uri(
            '/health_region/' + province + '/' + hr + '/')}, [hrs_data[hr]])
    chart.title = province + " cumulative deaths per Health Region"
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
    chart = pygal.Bar(height=260, show_x_labels=False, show_legend=False)
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
    chart = pygal.Bar(height=360, show_x_labels=False, show_legend=False)
    province_series_data = []
    for day in sorted_report_days:
        if (day, province) in data_x_y:
            province_series_data.append(data_x_y[(day, province)])
        else:
            province_series_data.append(None)
    chart.add(province, province_series_data)
    chart.title = "Daily testing in " + province
    chart.x_labels = sorted_report_days
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
    chart = pygal.Bar(height=320, show_x_labels=False, legend_at_bottom=True)
    for group in ["cases", "testing"]:
        data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                data_list.append(data_x_y[(day, group)])
            else:
                data_list.append(None)
        chart.add(group, data_list)

    chart.title = province + " daily cases vs testing"
    chart.x_labels = sorted_report_days

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
    chart = pygal.Line(height=360, show_x_labels=False, legend_at_bottom=True)
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
    chart = pygal.Line(height=260, show_x_labels=False, show_legend=False)
    province_series_data = []
    for day in sorted_report_days:
        if (day, province) in data_x_y:
            province_series_data.append(data_x_y[(day, province)])
        else:
            province_series_data.append(None)
    chart.add(province + " cumulative testing", province_series_data)
    chart.title = "Cumulative testing in " + province
    chart.x_labels = sorted_report_days
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
    chart = pygal.Line(height=300, show_x_labels=False, legend_at_bottom=True)
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
    chart = pygal.Line(height=320, show_x_labels=False, legend_at_bottom=True)
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
    return chart.render_data_uri()


@cache_page(60 * 15)
def health_region_view(request, province, health_region):

    chart1 = hr_cases_bar_chart(province, health_region)
    chart2 = hr_cumulative_cases_lines_chart(province, health_region)

    charts = [chart1, chart2]

    context = {
        "charts": charts,
        "title":  "Coronavirus in " + health_region + ' (' + province + ')'
    }

    return render(request, "chart/charts.html", context)


def hr_cases_bar_chart(province, health_region):

    data_x_y = {}
    groups_list = {}

    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y[(row_data["date_report"], "cases")
                         ] = int(row_data["cases"])
                groups_list["cases"] = int(row_data["cases"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_groups = sorted(groups_list.keys(), key=lambda k: -groups_list[k])
    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Bar(height=320, show_x_labels=False, show_legend=False)
    for group in sorted_groups:
        data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                data_list.append(data_x_y[(day, group)])
            else:
                data_list.append(None)
        chart.add("Cases", data_list)

    chart.title = health_region + " (" + province + ") daily cases"
    chart.x_labels = sorted_report_days
    return chart.render_data_uri()


def hr_cumulative_cases_lines_chart(province, health_region):

    data_x_y = {}
    groups_list = {}

    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y[(row_data["date_death_report"], "cumulative_deaths")] = int(
                    row_data["cumulative_deaths"])
                groups_list["cumulative_deaths"] = int(
                    row_data["cumulative_deaths"])

    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y[(row_data["date_report"], "cumulative_cases")] = int(
                    row_data["cumulative_cases"])
                groups_list["cumulative_cases"] = int(
                    row_data["cumulative_cases"])

    report_day_set = set()
    for key in data_x_y:
        day = key[0]
        report_day_set.add(day)

    sorted_groups = sorted(groups_list.keys(), key=lambda k: -groups_list[k])
    sorted_report_days = sorted(list(report_day_set), key=day_month_year)
    chart = pygal.Line(height=320, show_x_labels=False, legend_at_bottom=True)
    for group in sorted_groups:
        cumulative_data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                cumulative_data_list.append(data_x_y[(day, group)])
            else:
                cumulative_data_list.append(None)
        chart.add(group, cumulative_data_list)

    chart.title = health_region + " (" + province + ") cumulative cases data"

    chart.x_labels = sorted_report_days
    return chart.render_data_uri()


def prov_hrs_cumulative_cases_line_chart(province):

    data_x_y = {}
    groups_list = {}

    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_death_report"], "cumulative_deaths")] = int(
                    row_data["cumulative_deaths"])
                groups_list["cumulative_deaths"] = int(
                    row_data["cumulative_deaths"])

    with open("data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_report"], "cumulative_cases")] = int(
                    row_data["cumulative_cases"])
                groups_list["cumulative_cases"] = int(
                    row_data["cumulative_cases"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_groups = sorted(groups_list.keys(), key=lambda k: -groups_list[k])
    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.Line(height=320, show_x_labels=False, legend_at_bottom=True)
    for group in sorted_groups:
        cumulative_data_list = []
        for day in sorted_report_days:
            if (day, group) in data_x_y:
                cumulative_data_list.append(data_x_y[(day, group)])
            else:
                cumulative_data_list.append(None)
        chart.add(group, cumulative_data_list)

    chart.title = health_region + " (" + province + ") cumulative cases data"

    chart.x_labels = sorted_report_days
    return chart.render_data_uri()


@cache_page(60 * 15)
def hrs_view(request):

    chart1 = provs_hrs_cases_pie_chart(request)
    chart2 = provs_hrs_cumulative_cases_pie_chart(request)
    charts = [chart1, chart2]

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

    chart = pygal.Pie(height=360)

    for province in sorted_provs:
        prov_hrs_data = []
        for hr in prov_hrs[province]:
            prov_hrs_data.append({'value': hrs_data[(province, hr)], 'label': hr, 'xlink': request.build_absolute_uri(
                '/health_region/' + province + '/' + hr + '/')})
        chart.add({"title": province, 'xlink': request.build_absolute_uri(
            '/province_hrs/' + province + '/')}, sorted(prov_hrs_data, key=lambda hr: -hr["value"]))
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

    chart = pygal.Pie(height=360, show_legend=True)

    for province in sorted_provs:
        prov_hrs_data = []
        for hr in prov_hrs[province]:
            prov_hrs_data.append({'value': hrs_data[(province, hr)], 'label': hr, 'xlink': request.build_absolute_uri(
                '/health_region/' + province + '/' + hr + '/')})
        chart.add({"title": province, 'xlink': request.build_absolute_uri(
            '/province_hrs_cumulative/' + province + '/')}, sorted(prov_hrs_data, key=lambda hr: -hr["value"]))
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

    chart = pygal.Pie(height=360)

    sorted_provs = sorted(
        provs_data.keys(), key=lambda province: -provs_data[province])
    for province in sorted_provs:
        if provs_data[province] != 0:
            chart.add({"title": province, 'xlink': request.build_absolute_uri('/province/' + province + '/')},
                      [{"value": provs_data[province], 'xlink': request.build_absolute_uri('/province/' + province + '/')}])
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

    chart = pygal.Bar(height=320, legend_at_bottom=True)

    sorted_provs = sorted(
        provs_data.keys(), key=lambda province: -provs_data[province])
    for province in sorted_provs:
        chart.add({"title": province, 'xlink': request.build_absolute_uri(
            '/province/' + province + '/')}, [{"value": provs_data[province]}])
    chart.title = "New cases per Province on " + \
        str(set(provs_latest_report_date.values()))[2:-2]
    return chart.render_data_uri()


def day_month_year(date):
    l = date.split("-")
    # year:month:day
    return l[2] + l[1] + l[0]


def display_month_day(date):
    l = date.split("-")
    # return l[1] + "-" + l[0]
    return date
