from config import *
import re


class Line:
    def getattr(self):
        def get_data(name, offset=0):
            return self.MainSheet.get_value(LINE_MATCHER[name], self.index + offset)

        return get_data

    def setattr(self):
        def set_data(name, value, offset=0):
            return self.MainSheet.set_value(LINE_MATCHER[name], self.index + offset, str(value))

        return set_data

    def __init__(self, MainSheet, index):
        # for change
        self.plans = []
        self.MainSheet = MainSheet
        ga = self.getattr()

        # lines
        self.index = index
        self.COUNT_LINES = int(ga("COUNT_LINES"))
        self.PLANS = [
            {
                'name': ga("PLANS_name", i),
                'plan': '',
                'plan_type': '',
                'options': [],
                "number": fix_number(ga("PLANS_number", i)),
            }
            for i in range(self.COUNT_LINES)
        ]

        # data
        self.PASSPORT = fix_passport(ga("PASSPORT"))
        self.NAME = ga("NAME")
        self.SURNAME = ga("SURNAME")
        self.CITY = fix_city(ga("CITY"))
        self.STREET, self.APART_NUMBER, self.HOUSE_NUMBER = fix_street(ga("STREET_APART_NUMBER_HOUSE_NUMBER"))
        self.NUMBER_USER = fix_number(ga("NUMBER_USER"))
        self.POBox = '000'
        if 'הוראת קבע' not in ga("TYPE_PAY"):
            self.TYPE_PAY = 'card'
            self.CARD = ga("CARD")
            self.SROK = fix_srok(ga("SROK"))
        else:
            self.TYPE_PAY = 'bank'

        # one use
        self.unique_symbol = ga("unique_symbol")
        self.first_sort_key = ga("first_sort_key")
        self.second_sort_key = ga("second_sort_key")

    def load_plans(self, plans):
        self.plans = plans
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

    def change_data(self, name, value):
        sa = self.setattr()
        match name:
            case "NAME":
                sa("NAME", value)
                self.NAME = value
            case "SURNAME":
                sa("SURNAME", value)
                self.SURNAME = value
            case 'PLANS_name':
                for i in range(self.COUNT_LINES):
                    sa("PLANS_name", value[i], i)
                    self.PLANS[i]["name"] = value[i]
            case "PLANS_number":
                for i in range(self.COUNT_LINES):
                    sa("PLANS_number", value[i], i)
                    self.PLANS[i]["number"] = value[i]
        self.MainSheet.save()


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
