import time
import json

with open(r'.settings', 'r') as file:
    out = json.loads(file.read())

COUNT_GROUPS = 4

# SHEETS DIRS
PATH_MAIN_SHEET = out['PATH_MAIN_SHEET']
PATH_SORT_SHEET = out['PATH_SORT_SHEET']
PATH_PLANS_SHEET = out['PATH_PLANS_SHEET']
PATH_ERRORS_SHEET = 'data/errors.xlsx'
PATH_COLLECT_ERRORS_SHEET = 'data/collect_errors.xlsx'
PATH_WEBDRIVER = out['PATH_WEBDRIVER']
SETTINGS_ACCOUNT_PATH = out['SETTINGS_ACCOUNT_PATH']
LOG_PATH = out['LOG_PATH']

SHEET_PLANS_COLUMN = ['A', 'B', 'C', 'D', 'E']
SHEET_SORT_COLUMN = [['A', 'B'], ['C', 'D'], ['E', 'F'], ['G', 'H']]
SORTED_KEYS = [['צוות נוטשים', 'נוטשים'], ['צוות נוטשים', 'WB'], ['צוות WB', 'WB'], ['צוות WB', 'נוטשים']]

TIME_DELAY_PERC = float(out['TIME_DELAY_PERC'])
MAX_TIME_WAIT = float(out['MAX_TIME_WAIT'])
TYPE_SLEEP = out['TYPE_SLEEP']  # standard
CAN_MISS_WHEN_SLEEP = 2

LOGGING = out['LOGGING']

LINE_MATCHER = {
    "COUNT_LINES": "S",
    "PLANS_name": "V",
    "PLANS_number" : "G",
    "PASSPORT": "D",
    "NAME": "E",
    "SURNAME": "Z",
    "CITY": "AA",
    "STREET_APART_NUMBER_HOUSE_NUMBER": "AB",
    "NUMBER_USER": "AC",
    "POBox": "000",
    "TYPE_PAY": "AF",  # ["card", "bank"] # 'הוראת קבע'
    "CARD": "AO",
    "SROK": "AP",
    "unique_symbol": "BD",
    "first_sort_key": "P",
    "second_sort_key": "M"
}


def closure(command, *args, **kwargs):
    def closure_command():
        command(*args, **kwargs)

    return closure_command
