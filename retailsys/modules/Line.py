from config import *
import re


class Line:
    def __init__(self, MainSheet, index):
        # lines
        self.index = index
        self.COUNT_LINES = int(MainSheet.get_value("S", index))
        self.PLANS = [
            {
                'name': MainSheet.get_value("V", index + i),
                'plan': '',
                'plan_type': '',
                'options': [],
                "number": fix_number(MainSheet.get_value("G", index + i)),
            }
            for i in range(self.COUNT_LINES)
        ]

        # data
        self.PASSPORT = fix_passport(MainSheet.get_value("D", index))
        self.NAME = MainSheet.get_value("E", index)
        self.SURNAME = MainSheet.get_value("Z", index)
        self.CITY = fix_city(MainSheet.get_value("AA", index))
        self.STREET, self.APART_NUMBER, self.HOUSE_NUMBER = fix_street(MainSheet.get_value("AB", index))
        self.NUMBER_USER = fix_number(MainSheet.get_value("AC", index))
        self.POBox = '000'
        if 'הוראת קבע' not in MainSheet.get_value("AF", index):
            self.TYPE_PAY = 'card'
            self.CARD = MainSheet.get_value("AO", index)
            self.SROK = fix_srok(MainSheet.get_value("AP", index))
        else:
            self.TYPE_PAY = 'bank'

        # one use
        self.unique_symbol = MainSheet.get_value("BD", index)
        self.first_sort_key = MainSheet.get_value("P", index)
        self.second_sort_key = MainSheet.get_value("M", index)

    def load_plans(self, plans):
        for i in range(self.COUNT_LINES):
            for row in plans:
                if self.PLANS[i]['name'] == row[0]:
                    self.PLANS[i]['plan_type'] = row[2]
                    # if self.numb in [0, 3]:
                    #     self.PLANS[i]['plan_type'] = row[2]
                    # else:
                    #     self.PLANS[i]['plan_type'] = row[3]

                    cur_options = row[4].split(',')
                    # unique symbol
                    if self.unique_symbol == 'כן':
                        cur_options.append('חודש ראשון ללא עלות')

                    self.PLANS[i]['plan'] = row[1]
                    self.PLANS[i]['options'] = cur_options
                    break


def fix_number(numb): return '0' + numb if len(numb) == 9 else numb


def fix_passport(numb): return '0' + numb if len(numb) == 8 else numb


def fix_srok(srok): return [i[1:] if i == '0' else i for i in srok.split('/')]


def fix_city(name):
    name_d = name
    for ww in range(1, len(name_d)):
        if name_d[-ww] == ' ':
            name = name_d[:-ww]
        else:
            break
    return name


def fix_street(name):
    addrs = name
    addr_street = ''
    for w in range(len(addrs)):
        try:
            int(addrs[w])
            addr_street = (addrs[:w - 1])
            e = addr_street
            for ww in range(1, len(e)):
                if e[-ww] == ' ':
                    addr_street = e[:-ww]
                else:
                    break
            break
        except Exception as e:
            pass
    addr_numb_hous, addr_numb_kv = re.sub(r'\D', ' ', addrs).split()
    return addr_numb_hous, addr_numb_kv, addr_street
