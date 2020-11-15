
from data import MFData
from data import MFPortfolio
from util import *

#from dateutil.relativedelta import relativedelta

portfolio = MFPortfolio()

DATE_START = '01-03-2005'
#DATE_CUR = '25-03-2005'
DATE_CUR = '25-01-2018'
#DATE_CUR = '14-11-2020'

DATE_END = '14-11-2020'

def print_returns():
    period = None #get_years()
    total_transaction_list = list()

    for filename, data in portfolio.get_mf_data().items():
        investmemt = int(data.invested)
        value = int(data.units * data.last_nav)

        cagr = None #get_cagr(investmemt, value, period)

        total_transaction_list.extend(data.transaction_list)
        trans = (get_date(data.last_date), value)
        data.transaction_list.append(trans)

        xirr = round(get_xirr(data.transaction_list)*100, 2)

        print("filename :" + str(filename) + " investment :" + str(investmemt) + " value: " + str(int(value)) + " period :" + str(period) + " cagr :" + str(cagr) + " xirr :" + str(xirr))



    investmemt = portfolio.get_investment()
    value = portfolio.get_investment_value()

    cagr = None #get_cagr(investmemt, value, period)

    trans = (get_date(DATE_END), value)
    total_transaction_list.append(trans)

    xirr = round(get_xirr(total_transaction_list) * 100, 2)

    print(
        "total " + " investment :" + str(investmemt) + " value: " + str(value) + " period :" + str(
            period) + " cagr :" + str(cagr) + " xirr :" + str(xirr))


def get_years():
    date_start = get_datetime(DATE_START)
    date_end = get_datetime(DATE_CUR)

    delta = date_end - date_start
    return round(float(delta.days/365), 2)


def invest_sip(amount, date_str, date_end_str):
    print("**Sip**")

    mf_count = portfolio.get_mf_count()
    #amount_per_mf = int(amount / mf_count)
    amount_per_mf = 1000

    date_start_str = get_next_date_weekday(date_str, calendar.MONDAY)

    date_start = get_datetime(date_start_str)
    date_end = get_datetime(date_end_str)

    while(date_start < date_end):

        for filename, data in portfolio.get_mf_data().items():
            #print("filename :" + str(filename) + " date_start_str :" +  str(date_start_str) + "data :" + str(data))
            data.buy(amount_per_mf, date_start_str)

        date_start_str = get_next_date_weekday(date_start_str, calendar.MONDAY)
        date_start = get_datetime(date_start_str)

def invest_custom(amount, date_str, date_end_str):
    print("**Custom**")

    mf_count = portfolio.get_mf_count()

    date_start_str = get_next_date_weekday(date_str, calendar.MONDAY)

    date_start = get_datetime(date_start_str)
    date_end = get_datetime(date_end_str)

    while(date_start < date_end):

        '''
        investmemt = portfolio.get_date_investment_value(date_start_str)
        target_amount_per_mf = int((investmemt + amount) / mf_count)

        #print("amount :" + str(amount) + " cur_value: " + str(investmemt) + " to_invest :" + str(target_amount_per_mf * mf_count - investmemt))


        for filename, data in portfolio.get_mf_data().items():
            cur_value = data.get_cur_value(date_start_str)
            if target_amount_per_mf > cur_value:
            #print("filename :" + str(filename) + " date_start_str :" +  str(date_start_str) + "data :" + str(data))
                data.buy(int(target_amount_per_mf-cur_value), date_start_str)
            else:
                data.sell(int(cur_value - target_amount_per_mf), date_start_str)
        '''

        rebalance(amount, date_start_str)

        date_start_str = get_next_date_weekday(date_start_str, calendar.MONDAY)
        date_start = get_datetime(date_start_str)


def rebalance(amount, date_start_str):
    mf_count = portfolio.get_mf_count()

    investmemt = portfolio.get_date_investment_value(date_start_str)
    target_amount_per_mf = int((investmemt + amount) / mf_count)

    # print("amount :" + str(amount) + " cur_value: " + str(investmemt) + " to_invest :" + str(target_amount_per_mf * mf_count - investmemt))

    for filename, data in portfolio.get_mf_data().items():
        cur_value = data.get_cur_value(date_start_str)
        if target_amount_per_mf > cur_value:
            # print("filename :" + str(filename) + " date_start_str :" +  str(date_start_str) + "data :" + str(data))
            data.buy(int(target_amount_per_mf - cur_value), date_start_str)
        else:
            data.sell(int(cur_value - target_amount_per_mf), date_start_str)


def should_rebalance():
    rebalance = False
    investmemt = portfolio.get_investment_value()

    max = 0
    min = int(0xFFFFFFFF)

    for filename, data in portfolio.get_mf_data().items():
        cur_value = round(data.last_nav * data.units, 2)
        if cur_value > max:
            max = cur_value

        if cur_value < min:
            min = cur_value

        #print("filename" + str(filename) + " cur_value:" + str(cur_value) + " min:" + str(min) + " max:" + str(max))

    if max > ((max+min)*53/100):
        rebalance = True

    #print("rebalance :" + str(rebalance))

    return rebalance




def invest_rebalance(amount, date_str, date_end_str):

    print("**Rebalance**")

    mf_count = portfolio.get_mf_count()
    amount_per_mf = int(amount / mf_count)

    date_start_str = get_next_date_weekday(date_str, calendar.MONDAY)

    date_start = get_datetime(date_start_str)
    date_end = get_datetime(date_end_str)

    while(date_start < date_end):

        for filename, data in portfolio.get_mf_data().items():
            #print("filename :" + str(filename) + " date_start_str :" +  str(date_start_str) + "data :" + str(data))
            data.buy(amount_per_mf, date_start_str)

        if should_rebalance() is True:
            rebalance(0, date_start_str)

        date_start_str = get_next_date_weekday(date_start_str, calendar.MONDAY)
        date_start = get_datetime(date_start_str)


#print("years :" + str(get_years()))

def main():
    portfolio.init_mf_data()
    #invest_sip(6000, DATE_START, DATE_END)
    #invest_custom(0, DATE_START, DATE_CUR)

    #invest_custom(6000, DATE_START, DATE_END)
    #invest_custom(0, DATE_CUR, DATE_END)

    invest_rebalance(6000, DATE_START, DATE_END)
    #invest_rebalance(0, DATE_CUR, DATE_END)
    print_returns()

    #portfolio.init_mf_data()
    #cagr = invest_custom(6000, DATE_START)

main()

#get_date(DATE_CUR)













