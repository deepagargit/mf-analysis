
from data import MFData
from data import MFPortfolio
from util import *

#from dateutil.relativedelta import relativedelta

portfolio = MFPortfolio()

#DATE_START = '01-03-2005'
DATE_START = '01-03-2006'
#DATE_CUR = '25-03-2005'
DATE_CUR = '25-01-2014'
#DATE_CUR = '14-11-2020'

DATE_END = '14-11-2020'
#DATE_END = '14-03-2007'

def print_returns():
    period = None #get_years()
    total_transaction_list = list()

    nav18 = 0
    nav15 = 0
    nav10 = 0
    nav0 = 0

    for filename, data in portfolio.get_mf_data().items():
        investmemt = int(data.invested)
        value = int(data.units * data.last_nav)

        cagr = None #get_cagr(investmemt, value, period)

        total_transaction_list.extend(data.transaction_list)
        trans = (get_date(data.last_date), value)
        data.transaction_list.append(trans)

        xirr = get_xirr(data.transaction_list)

        print("filename :" + str(filename) + " investment :" + str(investmemt) + " value: " + str(int(value)) + " period :" + str(period) + " cagr :" + str(cagr) + " xirr :" + str(xirr))

        print("filename :" + str(filename) + " nav18 :" + str(round(data.nav18*100/data.navall,1)) + " nav15 :" + str(round(data.nav15*100/data.navall,1)) + " nav10 :" + str(round(data.nav10*100/data.navall,1)) + " nav0 :" + str(round(data.nav0*100/data.navall,1)) + " len: " + str(len(data.transaction_list)))



    investmemt = portfolio.get_investment()
    value = portfolio.get_investment_value()

    cagr = None #get_cagr(investmemt, value, period)

    trans = (get_date(DATE_END), value)
    total_transaction_list.append(trans)

    xirr = get_xirr(total_transaction_list)

    print(
        "total " + " investment :" + str(investmemt) + " value: " + str(value) + " period :" + str(
            period) + " cagr :" + str(cagr) + " xirr :" + str(xirr))


def get_years():
    date_start = get_datetime(DATE_START)
    date_end = get_datetime(DATE_CUR)

    delta = date_end - date_start
    return round(float(delta.days/365), 2)



def set_xirr_counter(data):

    transaction_list = list()
    transaction_list.extend(data.transaction_list)

    value = int(data.units * data.last_nav)
    trans = (get_date(data.last_date), value)
    transaction_list.append(trans)

    xirr = int(get_xirr(transaction_list))
    if xirr > 18:
        data.nav18 += 1
    elif xirr > 15:
        data.nav15 += 1
    elif xirr > 10:
        data.nav10 += 1
    else:
        data.nav0 += 1

    data.navall += 1

    #print("last_date: " + str(data.last_date) + " xirr: " + str(xirr) + " len: " + str(len(transaction_list)))

def invest_sip(amount, date_str, date_end_str):
    print("**Sip**")

    mf_count = portfolio.get_mf_count()
    amount_per_mf = int(amount / mf_count)
    #amount_per_mf = 1000

    date_start_str = get_next_date_weekday(date_str, calendar.MONDAY)

    date_start = get_datetime(date_start_str)
    date_end = get_datetime(date_end_str)

    date_xirr = date_start + timedelta(days=365)

    while(date_start < date_end):

        for filename, data in portfolio.get_mf_data().items():
            #print("filename :" + str(filename) + " date_start_str :" +  str(date_start_str) + "data :" + str(data))
            data.buy(amount_per_mf, date_start_str)

            if date_start > date_xirr:
                set_xirr_counter(data)

        date_start_str = get_next_date_weekday(date_start_str, calendar.MONDAY)
        date_start = get_datetime(date_start_str)

def invest_custom(amount, date_str, date_end_str):
    print("**Custom**")

    mf_count = portfolio.get_mf_count()

    date_start_str = get_next_date_weekday(date_str, calendar.MONDAY)

    date_start = get_datetime(date_start_str)
    date_end = get_datetime(date_end_str)

    date_xirr = date_start + timedelta(days=1)

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

        for filename, data in portfolio.get_mf_data().items():
            if date_start > date_xirr:
                set_xirr_counter(data)

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


def should_rebalance_percentage():
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

    if max > ((max+min)*65/100):
        rebalance = True

    #print("rebalance :" + str(rebalance))

    return rebalance


def should_rebalance_dma():
    rebalance = False

    for filename, data in portfolio.get_mf_data().items():
        if filename == "sc-kotak.csv" and data.last_dma20 is not None and data.last_dma200 is not None:

            if portfolio.isBuy is True and data.last_nav < data.last_dma200:
                rebalance = True
                portfolio.isBuy = False
                print('Sell {}: last_date:{} last_dma20:{} last_dma200:{} equity:{} debt:{}'.format(filename, data.last_date, data.last_dma20,
                                                                             data.last_dma200, portfolio.get_cur_equity_value(), portfolio.get_cur_debt_value()))
            elif portfolio.isBuy is False and data.last_nav > data.last_dma200:
                rebalance = True
                portfolio.isBuy = True
                print('Buy {}: last_date:{} last_dma20:{} last_dma200:{} equity:{} debt:{}'.format(filename,
                                                                                                    data.last_date,
                                                                                                    data.last_dma20,
                                                                                                    data.last_dma200,
                                                                                                    portfolio.get_cur_equity_value(),
                                                                                                    portfolio.get_cur_debt_value()))

    return rebalance


def invest_rebalance(amount, date_str, date_end_str):

    print("**Rebalance**")

    mf_count = portfolio.get_mf_count()
    amount_per_mf = int(amount / mf_count)
    #amount_per_mf = int(amount / mf_count * 2)

    date_start_str = get_next_date_weekday(date_str, calendar.MONDAY)

    date_start = get_datetime(date_start_str)
    date_end = get_datetime(date_end_str)

    date_xirr = date_start + timedelta(days=365)

    while(date_start < date_end):

        for filename, data in portfolio.get_mf_data().items():
            #print("filename :" + str(filename) + " date_start_str :" +  str(date_start_str) + "data :" + str(data))
            data.buy(amount_per_mf, date_start_str)

            '''
            if data.filename == "sc-kotak.csv" or data.filename == "mc-lt.csv" or data.filename == "muc-sbi-focus.csv":
                if portfolio.isBuy is True:
                    data.buy(amount_per_mf, date_start_str)
                else:
                    data.buy(0, date_start_str)
                    #print('{} date:{} amount:{}'.format(filename, date_start_str, amount_per_mf))

            if data.filename == "debt-gilt-icici.csv" or data.filename == "debt-dynamic-nippon.csv" or data.filename == "debt-corp-franklin.csv":
                if portfolio.isBuy is False:
                    data.buy(amount_per_mf, date_start_str)
                else:
                    data.buy(0, date_start_str)
                    #print('{} date:{} amount:{}'.format(filename, date_start_str, amount_per_mf))
            '''

        if should_rebalance_percentage() is True:
            rebalance(0, date_start_str)

        for filename, data in portfolio.get_mf_data().items():
            if date_start > date_xirr:
                set_xirr_counter(data)



        date_start_str = get_next_date_weekday(date_start_str, calendar.MONDAY)
        date_start = get_datetime(date_start_str)


#print("years :" + str(get_years()))

def main():
    portfolio.init_mf_data()
    #invest_sip(6000, DATE_START, DATE_CUR)
    #invest_custom(0, DATE_CUR, DATE_END)

    invest_custom(6000, DATE_START, DATE_CUR)
    invest_custom(0, DATE_CUR, DATE_END)

    #invest_rebalance(6000, DATE_START, DATE_CUR)
    #invest_rebalance(0, DATE_CUR, DATE_END)
    print_returns()

    #portfolio.init_mf_data()
    #cagr = invest_custom(6000, DATE_START)

main()

#get_date(DATE_CUR)













