
import csv
import datetime
from datetime import timedelta
from datetime import date

import calendar

DATE_CSV_FORMAT = '%d-%m-%Y'
DATE_NORMALISED_FORMAT = '%Y%m%d'

def read_data(filename):
    try:
        with open(filename) as f:
            reader = csv.reader(f)
            for i in range(5):
                next(reader)  # skip header
            data = [r for r in reader]

        return data
    except Exception as e:
        print('Exception :{}'.format(e))

def clean_data(data):
    try:
        #print('Data length : {}'.format(len(data)))
        #print('Data item length : {}'.format(len(data[0])))
        #print('Data item :{}'.format(data[0]))

        nav_list = data.nav_dict

        data_cleaned = {}

        iterdata = iter(nav_list)

        navsum20 = 0.0
        for i in range(20):
            navsum20 += get_norm_nav(nav_list[i][1])

        navsum200 = 0.0
        for i in range(200):
            navsum200 += get_norm_nav(nav_list[i][1])

        #next(iterdata)
        index = 0
        for dateitem in iterdata:
            #print("cur " + dateitem[0] + " next Monday " + get_next_date(dateitem[0], calendar.MONDAY))
            #break
            #print('dateitem:{}'.format(data[0][0]))
            #print('dateitem:{}'.format(data[1][1]))
            #break

            nav = get_norm_nav(dateitem[1])
            data_cleaned[dateitem[0]] = nav

            #if index < 5:
            #    print('date:{} nav:{}'.format(dateitem[0], nav))
            #    print('navsum20: {} navsum200: {}'.format(navsum20, navsum200))

            data.dma20_dict[dateitem[0]] = round(navsum20/20, 4)
            data.dma200_dict[dateitem[0]] = round(navsum200/200, 4)

            #if data.filename == "sc-kotak.csv":
            #    print('clean {} date: {} nav: {} navsum20: {} navsum200: {}'.format(data.filename, dateitem[1], dateitem[0], data.dma20_dict.get(dateitem[0]), data.dma200_dict.get(dateitem[0])))

            if (index+20) < len(nav_list):
                navsum20 -= get_norm_nav(nav_list[index][1])
                navsum20 += get_norm_nav(nav_list[index+20][1])
            else:
                navsum20 = 0.0

            if (index + 200) < len(nav_list):
                navsum200 -= get_norm_nav(nav_list[index][1])
                navsum200 += get_norm_nav(nav_list[index + 200][1])
            else:
                navsum200 = 0.0

            index += 1

        #print(data.dma20_dict)
        #print(data.dma200_dict)

        #    print('date:{} nav:'.format(dateitem))

        return data_cleaned
    except Exception as e:
        print('Exception :{}'.format(e))


def get_date(date_str):
    dt = datetime.datetime.strptime(date_str, DATE_CSV_FORMAT).date()
    return dt

def get_datetime(date_str):
    dt = datetime.datetime.strptime(date_str, DATE_CSV_FORMAT)
    return dt

def get_next_date(date_str): # date_str dd-mm-yyyy
    try:
        next_date_str = (datetime.datetime.strptime(date_str, DATE_CSV_FORMAT) + timedelta(days=1)).strftime(DATE_CSV_FORMAT)
        return next_date_str
    except Exception as e:
        print('Exception :{}'.format(e))

    return None

def get_next_date_weekday(date_str, weekday): # date_str dd-mm-yyyy weekday is 0 for Monday

    curday = datetime.datetime.strptime(date_str, DATE_CSV_FORMAT).weekday()
    #nextdays = 7 - curday + weekday
    nextdays = 7 - curday + weekday + 21 + 330


    try:
        next_date_str = (datetime.datetime.strptime(date_str, DATE_CSV_FORMAT) + timedelta(days=nextdays)).strftime \
            (DATE_CSV_FORMAT)
        return next_date_str
    except Exception as e:
        print('Exception :{}'.format(e))

    return None

def get_norm_date(date_str): # date_str dd-mm-yyyy norm_date_str yyyymmdd
    try:
        norm_date_str = (datetime.datetime.strptime(date_str, DATE_CSV_FORMAT)).strftime(DATE_NORMALISED_FORMAT)
        return norm_date_str
    except Exception as e:
        print('Exception :{}'.format(e))

    return None

def get_norm_nav(nav): # str to float
    try:
        return round(float(nav), 4)
    except Exception as e:
        print('Exception :{}'.format(e))

    return None

def get_cagr(investment, value, period):
    period = period/2

    cagr = (((value/investment)**(1/period)-1) * 100, 2)

    return cagr

def get_xirr(cashflows):
    years = [(ta[0] - cashflows[0][0]).days / 365. for ta in cashflows]
    residual = 1.0
    step = 0.05
    guess = 0.05
    epsilon = 0.0001
    limit = 10000
    while abs(residual) > epsilon and limit > 0:
        limit -= 1
        residual = 0.0
        for i, trans in enumerate(cashflows):
            residual += trans[1] / pow(guess, years[i])
        if abs(residual) > epsilon:
            if residual > 0:
                guess += step
            else:
                guess -= step
                step /= 2.0

    xirr = guess - 1

    return round(xirr * 100, 2)