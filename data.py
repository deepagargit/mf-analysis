from util import *
import csv


class MFData:
    filename = None
    nav_dict = None
    invested = None
    units = None
    last_nav = None
    last_date = None
    transaction_list = None

    def __init__(self):
        self.filename = None
        self.nav_dict = None
        self.invested = 0
        self.units = 0.0
        self.last_nav = 0.0
        self.last_date = None
        self.transaction_list = list()


    def get_nav(self, date_str):
        nav = self.nav_dict.get(date_str)

        #print("get_nav :" + str(self.filename) + " " + str(date_str) + " " + str(nav))

        if nav is None:
            for day in range(6):
                date_str = get_next_date(date_str)
                nav = self.nav_dict.get(date_str)
                if nav is not None:
                    break

        return get_norm_nav(nav)

    def get_cur_value(self, date_str):
        nav = self.get_nav(date_str)
        cur_val = round(nav * self.units, 2)

        return cur_val

    def buy(self, amount, date_str):
        nav = self.get_nav(date_str)

        units = round(float(amount/nav), 4)
        self.units += units

        self.invested += amount
        self.last_nav = nav
        self.last_date = date_str

        #print("buy :" + str(self.filename) + " date :" + str(date_str) + " transaction_list :" + str(self.transaction_list))

        trans = (get_date(date_str), -1*amount)
        self.transaction_list.append(trans)

        #print("buy :" + str(self.filename) + " date :" + str(date_str) + " amount :" + str(amount) + " invested :" + str(self.invested) + " value :" + str(round(self.units * self.last_nav, 4)) +  "units :" + str(self.units) + " last_nav :" + str(self.last_nav))
        #print("buy :" + str(self.filename) + " date :" + str(date_str) + " transaction_list :" + str(self.transaction_list))

    def sell(self, amount, date_str):
        nav = self.get_nav(date_str)

        units = round(float(amount/nav), 4)
        self.units -= units

        self.invested -= amount
        self.last_nav = nav
        self.last_date = date_str

        trans = (get_date(date_str), amount)
        self.transaction_list.append(trans)

        #print("sell :" + str(self.filename) + " date :" + str(date_str) + " transaction_list :" + str(self.transaction_list))





class MFPortfolio:

    mf_data = {}


    mf_data["sc-kotak.csv"] = None

    mf_data["mc-lt.csv"] = None
    mf_data["muc-sbi-focus.csv"] = None
    mf_data["debt-gilt-icici.csv"] = None
    mf_data["debt-dynamic-nippon.csv"] = None
    mf_data["debt-corp-franklin.csv"] = None




    def init_mf_data(self):

        try:

            for filename in self.mf_data.keys():
                data = MFData()
                data.nav_dict = read_data(filename)
                data.nav_dict = clean_data(data.nav_dict)
                data.filename = filename

                self.mf_data[filename] = data

        except Exception as e:
            print('Exception :{}'.format(e))

    def get_mf_filenames(self):
        return self.mf_data.keys()

    def get_mf_count(self):
        return len(self.mf_data)

    def get_mf_data(self):
        return self.mf_data

    def get_investment(self):
        investment = 0.0

        for data in self.mf_data.values():
            investment += data.invested

        return investment

    def get_investment_value(self):
        investment = 0.0

        for data in self.mf_data.values():
            investment += round(data.units * data.last_nav, 2)

        return investment

    def get_date_investment_value(self, date_str):
        investment = 0.0

        for data in self.mf_data.values():
            investment += round(data.get_cur_value(date_str), 2)

        return investment








