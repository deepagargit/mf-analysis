

import csv
from datetime import datetime
from datetime import date
import calendar

BENCHMARK_FILENAME = "BSE100.csv"
MF_FILENAME = "sbi_bluechip_regular_growth.csv"
SIP_AMOUNT = 10000


def read_benchmark(filename):

    try:
        with open(filename) as f:
            reader = csv.reader(f)
            next(reader) # skip header
            data = [r for r in reader]
        
        return data
    except Exception as e:
        print('Exception :{}'.format(e))
        

def clean_benchmark_data(data):
    try:
        print('Data length : {}'.format(len(data)))
        print('Data item length : {}'.format(len(data[0])))
        print('Data item :{}'.format(data[0]))
        
        data_cleaned = {}
        dateitemlast = data[0]
        dateitemlast.append(0.0)
        
        iterdata = iter(data)
        next(iterdata)
        for dateitem in iterdata:
            datestring = dateitem[0]
            #print('Date string :{}'.format(datestring))
            dt = datetime.strptime(datestring, '%d-%B-%Y')
            datenormalized = dt.strftime("%Y%m%d")
            #print('Date string :{}  Close :{}'.format(datenormalized, dateitem[4]))
            
            gain = round(float(dateitem[4])- float(dateitemlast[4]), 2)
            dateitem.append(gain)
            #print('Data Last string :{}'.format(dateitemlast))
            #print('Data string :{}'.format(dateitem))
            
            data_cleaned[datenormalized] = round(((gain * 100)/ float(dateitemlast[4])), 2)
            dateitemlast = dateitem
            
            
        return data_cleaned
    except Exception as e:
        print('Exception :{}'.format(e))
        
    
def clean_mf_data(data):
    try:
        print('Data length : {}'.format(len(data)))
        print('Data item length : {}'.format(len(data[0])))
        print('Data item :{}'.format(data[0]))
        
        
        data_cleaned = {}
        
        for dateitem in data:
            datestring = dateitem[0]
            #print('Date string :{}'.format(datestring))
            dt = datetime.strptime(datestring, '%d-%m-%Y')
            datenormalized = dt.strftime("%Y%m%d")
            #print('Date string :{}  Nav :{}'.format(datenormalized, dateitem[1]))
            
            nav = round(float(dateitem[1]), 2)
            
            data_cleaned[datenormalized] = nav
            #print('Date :{}  Nav :{}'.format(datenormalized, nav))
            
        return data_cleaned
        
    except Exception as e:
        print('Exception :{}'.format(e))

def get_input():
    input_data = [{'year': 2018, 'month': 1}, {'year': 2018, 'month': 2}, {'year': 2018, 'month': 3}]
    #input_data = []
    
    for year in range(2007,2018):
        for month in range(1,13):
            item = {}
            item['year'] = year
            item['month'] = month
            input_data.append(item)
            
    print('input_data:{}'.format(input_data))
    
    return input_data

def get_nav(year, month, day, mf_data_cleaned):
    try:
        dt = date(year,month, day)
        datenormalized = dt.strftime("%Y%m%d")
        nav = mf_data_cleaned.get(datenormalized)
        
        '''
        if nav is None:
            print('year:{} month:{} day:{} nav:{} datenormalized:{}'.format(year, month, day, nav, datenormalized))
        '''
        
        return nav
    except Exception as e:
        print('Exception :{} year:{} month:{} day:{}'.format(e, year,month, day))
        
    return None
        

def get_benchmark_gain(year, month, day, becnhmark_data_cleaned):
    dt = date(year,month, day)
    datenormalized = dt.strftime("%Y%m%d")
    gain = becnhmark_data_cleaned.get(datenormalized)
    
    return gain

def get_sip_nav(year, month, day, mf_data_cleaned):
    max_days = calendar.monthrange(year, month)[1]
    
    if day > max_days:
        month += 1
        day = 1
        
    nav = get_nav(year, month, day, mf_data_cleaned)
    if nav:
        return nav
    
    day += 1
    if day > max_days:
        month += 1
        day = 1
    nav = get_nav(year, month, day, mf_data_cleaned)
    if nav:
        return nav
    
    day += 1
    if day > max_days:
        month += 1
        day = 1
    nav = get_nav(year, month, day, mf_data_cleaned)
    if nav:
        return nav
    
    day += 1
    if day > max_days:
        month += 1
        day = 1
    nav = get_nav(year, month, day, mf_data_cleaned)
    if nav:
        return nav
    
    day += 1
    if day > max_days:
        month += 1
        day = 1
    nav = get_nav(year, month, day, mf_data_cleaned)
    if nav:
        return nav
    
    return None

def to_invest(year, month, day, becnhmark_data_cleaned, mf_data_cleaned):
    nav = get_nav(year, month, day, mf_data_cleaned)
    gain = get_benchmark_gain(year, month, day, becnhmark_data_cleaned)
    
    if nav is None or gain is None:
        #print('year:{} month:{} day:{} nav:{} gain:{}'.format(year, month, day, nav, gain))
        return None, None
    
    invest = (gain * 20 * SIP_AMOUNT)/100 * (-1)
    
    return invest, nav
    
    

def get_sip_investment(item, becnhmark_data_cleaned, mf_data_cleaned, amount, sip_tag, sip_dates):
    days = item.get('days')
    
    # Calculate sip nav allocation count
    sip_nav_count = 0
    sip_amount = amount/len(sip_dates)
    
    for sip_date in sip_dates:
        nav = get_sip_nav(item.get('year'),item.get('month'), sip_date, mf_data_cleaned)
        if nav is  None:
           print('sip nav none for {} {} {}'.format(item.get('year'),item.get('month'), sip_date))
           return
        
        sip_nav_count += sip_amount/nav
    
    item[sip_tag] = {'nav_count': round(sip_nav_count, 4)}


def get_mysip_investment(item, becnhmark_data_cleaned, mf_data_cleaned, amount):
    days = item.get('days')
    
    # Calculate my nav allocation count
    my_nav_count = 0
    my_invested = 0
    for day in range(1,days+1):
        invest, nav = to_invest(item.get('year'),item.get('month'), day, becnhmark_data_cleaned, mf_data_cleaned)
        
        if invest is None or nav is None:
            continue
        
        if day >= 15 and amount > 10000/2:
            invest += amount - 10000/2
        
        if day >= 28 and amount > 0:
            invest += amount
            
        if invest >= 1000 and amount >= 1000:
            amount -= invest
            if amount < 1000:
                invest += amount
                amount = 0
                
            nav_count = round(invest/nav, 4)
            my_nav_count += nav_count
            my_invested += invest
    
    item['mysip'] = {'nav_count': round(my_nav_count, 4)}
    

def sip_cagr():
    becnhmark_data = read_benchmark(BENCHMARK_FILENAME)
    becnhmark_data_cleaned = clean_benchmark_data(becnhmark_data)
    
    mf_data = read_benchmark(MF_FILENAME)
    mf_data_cleaned = clean_mf_data(mf_data)
    
    input_data = get_input()
    sip_1_15_nav_count_total = 0
    sip_10_25_nav_count_total = 0
    sip_1_10_20_nav_count_total = 0
    sip_1_8_15_22_nav_count_total = 0
    mysip_nav_count_total = 0
    total_investment = SIP_AMOUNT * len(input_data)
    
    for item in input_data:
        max_days = calendar.monthrange(item.get('year'), item.get('month'))[1]
        item['days'] = max_days
        
        get_sip_investment(item, becnhmark_data_cleaned, mf_data_cleaned, SIP_AMOUNT, "sip_1_15", [1,15])
        sip_1_15_nav_count_total += (item.get("sip_1_15")).get('nav_count')
        
        get_sip_investment(item, becnhmark_data_cleaned, mf_data_cleaned, SIP_AMOUNT, "sip_10_25", [10,25])
        sip_10_25_nav_count_total += (item.get("sip_10_25")).get('nav_count')
        
        get_sip_investment(item, becnhmark_data_cleaned, mf_data_cleaned, SIP_AMOUNT, "sip_1_10_20", [1,10,20])
        sip_1_10_20_nav_count_total += (item.get("sip_1_10_20")).get('nav_count')
        
        get_sip_investment(item, becnhmark_data_cleaned, mf_data_cleaned, SIP_AMOUNT, "sip_1_8_15_22", [1,8,15,22])
        sip_1_8_15_22_nav_count_total += (item.get("sip_1_8_15_22")).get('nav_count')
        
        get_mysip_investment(item, becnhmark_data_cleaned, mf_data_cleaned, SIP_AMOUNT)
        mysip_nav_count_total += (item.get('mysip')).get('nav_count')
    
    CAGR = (sip_1_15_nav_count_total*39.7883/total_investment)**(1/5.25)-1
    print('total_investment :{} CAGR:{}'.format(total_investment, round(CAGR*100,2)))
    print('sip_1_15_nav_count_total :{} value:{}'.format(sip_1_15_nav_count_total, sip_1_15_nav_count_total*39.7883))
    print('sip_10_25_nav_count_total :{} value:{}'.format(sip_10_25_nav_count_total, sip_10_25_nav_count_total*39.7883))
    print('sip_1_10_20_nav_count_total :{} value:{}'.format(sip_1_10_20_nav_count_total, sip_1_10_20_nav_count_total*39.7883))
    print('sip_1_8_15_22_nav_count_total :{} value:{}'.format(sip_1_8_15_22_nav_count_total, sip_1_8_15_22_nav_count_total*39.7883))
    print('mysip_nav_count_total :{}'.format(mysip_nav_count_total, mysip_nav_count_total*39.7883))
    #print('input_data: {}'.format(input_data))


def get_cagr(first_value, last_value, num_years):
    CAGR = (last_value/first_value)**(1/num_years)-1
    return CAGR

def trailing_cagr():

    mf_data = read_benchmark(MF_FILENAME)
    mf_data_cleaned = clean_mf_data(mf_data)

    start_nav = get_sip_nav(2006, 2, 14, mf_data_cleaned)
    year_count = 1

    for i in range(2007, 2019):
        last_nav = get_sip_nav(i, 4, 4, mf_data_cleaned)
        cagr = get_cagr(start_nav, last_nav, year_count)
        year_count = year_count + 1

        print('year={}  cagr={:.2%}'.format(i, cagr))


    
trailing_cagr()

#sip_cagr()
