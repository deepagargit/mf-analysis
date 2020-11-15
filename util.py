
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

        data_cleaned = {}

        iterdata = iter(data)
        #next(iterdata)
        for dateitem in iterdata:
            #print("cur " + dateitem[0] + " next Monday " + get_next_date(dateitem[0], calendar.MONDAY))
            #break
            data_cleaned[dateitem[0]] = get_norm_nav(dateitem[1])

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
    nextdays = 7 - curday + weekday

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

    return guess - 1