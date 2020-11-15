
import datetime
from datetime import date



# function
def xirr(cashflows):
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


#
data = [(datetime.date(2006, 1, 24), -39967), (datetime.date(2008, 2, 6), -19866),
        (datetime.date(2010, 10, 18), 245706), (datetime.date(2013, 9, 14), 52142)]

#print(xirr(data))

DATE_CSV_FORMAT = '%d-%m-%Y'
def get_date(date_str):
    dt = datetime.datetime.strptime(date_str, DATE_CSV_FORMAT).date()

    return dt

print(get_date('14-11-2020'))
