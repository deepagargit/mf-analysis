from util import *
import csv


class MFData:
    filename = None
    rebalance = None
    isBuy = None
    nav_dict = None
    dma200_dict = None
    dma20_dict = None

    invested = None
    units = None
    last_nav = None
    last_dma20 = None
    last_dma200 = None
    last_date = None
    transaction_list = None

    nav18 = None
    nav15 = None
    nav10 = None
    nav0 = None
    navall = None
    sipbuy = None
    sipsell = None

    def __init__(self):
        self.filename = None
        self.rebalance = False
        self.isBuy = True
        self.nav_dict = None
        self.dma200_dict = dict()
        self.dma20_dict = dict()

        self.invested = 0
        self.units = 0.0
        self.last_nav = 0.0
        self.last_dma20 = 0.0
        self.last_dma200 = 0.0
        self.last_date = None
        self.transaction_list = list()

        self.nav18 = 0
        self.nav15 = 0
        self.nav10 = 0
        self.nav0 = 0
        self.navall = 0
        self.sipbuy = 0
        self.sipsell = 0


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

        if nav is None:
            print('filename: {} date: {} nav :{}'.format(self.filename, date_str, nav))

        units = round(float(amount/nav), 4)
        self.units += units

        self.invested += amount
        self.last_nav = nav
        self.last_dma20 = self.dma20_dict.get(date_str)
        self.last_dma200 = self.dma200_dict.get(date_str)
        self.last_date = date_str
        self.sipbuy += 1

        #print("buy :" + str(self.filename) + " date :" + str(date_str)) # + " transaction_list :" + str(self.transaction_list))

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
        self.last_dma20 = self.dma20_dict.get(date_str)
        self.last_dma200 = self.dma200_dict.get(date_str)
        self.last_date = date_str
        self.sipsell += 1

        trans = (get_date(date_str), amount)
        self.transaction_list.append(trans)

        #print("sell :" + str(self.filename) + " date :" + str(date_str)) # + " transaction_list :" + str(self.transaction_list))





class MFPortfolio:

    mf_data = {}
    isBuy = True

    '''

    mf_data["sc-kotak.csv"] = None
    mf_data["mc-lt.csv"] = None
    mf_data["muc-sbi-focus.csv"] = None

    mf_data["sc-kotak2.csv"] = None
    mf_data["mc-lt2.csv"] = None
    mf_data["muc-sbi-focus2.csv"] = None
    
    mf_data["debt-gilt-icici.csv"] = None
    mf_data["debt-dynamic-nippon.csv"] = None
    mf_data["debt-corp-franklin.csv"] = None
    
    '''

    mf_data["canara_large_mid_cap.csv"] = None
    mf_data["invesco_contra.csv"] = None
    mf_data["kotak_mid_cap.csv"] = None
    mf_data["lt_mid_cap.csv"] = None
    mf_data["mirae_large_mid_cap.csv"] = None
    mf_data["motilal_nasdaq.csv"] = None
    mf_data["nippon_small_cap.csv"] = None
    mf_data["nippon_small_cap2.csv"] = None
    mf_data["sbi_small_cap2.csv"] = None
    mf_data["sbi_small_cap.csv"] = None

    mf_data["canara_large_mid_cap2.csv"] = None
    mf_data["invesco_contra2.csv"] = None
    mf_data["kotak_mid_cap2.csv"] = None
    mf_data["lt_mid_cap2.csv"] = None
    mf_data["mirae_large_mid_cap2.csv"] = None
    mf_data["motilal_nasdaq2.csv"] = None
    mf_data["nippon_small_cap3.csv"] = None
    mf_data["nippon_small_cap4.csv"] = None
    mf_data["sbi_small_cap3.csv"] = None
    mf_data["sbi_small_cap4.csv"] = None

    mf_data["debt_axis_dynamic.csv"] = None
    mf_data["debt_axis_psu.csv"] = None
    mf_data["debt_axis_psu2.csv"] = None
    mf_data["debt_hdfc_corporate.csv"] = None
    mf_data["debt_hdfc_corporate2.csv"] = None
    mf_data["debt_kotak_gold.csv"] = None
    mf_data["debt_nippon_gilt.csv"] = None
    mf_data["debt_sbi_dynamic.csv"] = None
    mf_data["debt_sbi_gilt.csv"] = None
    mf_data["debt_sbi_gold.csv"] = None



    def init_mf_data(self):

        try:

            for filename in self.mf_data.keys():
                data = MFData()
                data.filename = filename
                data.nav_dict = read_data(filename)
                data.nav_dict = clean_data(data)

                data.rebalance = False

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

    def get_cur_equity_value(self):
        investment = 0.0

        for data in self.mf_data.values():
            if data.filename == 'sc-kotak.csv' or data.filename == 'mc-lt.csv' or data.filename == 'muc-sbi-focus.csv':
                investment += round(data.units * data.last_nav, 2)

        return investment

    def get_cur_debt_value(self):
        investment = 0.0

        for data in self.mf_data.values():
            if data.filename == 'debt-gilt-icici.csv' or data.filename == 'debt-dynamic-nippon.csv' or data.filename == 'debt-corp-franklin.csv':
                investment += round(data.units * data.last_nav, 2)

        return investment

    def get_date_investment_value(self, date_str):
        investment = 0.0

        for data in self.mf_data.values():
            investment += round(data.get_cur_value(date_str), 2)

        return investment








