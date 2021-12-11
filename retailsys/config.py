import time
import json

with open(r'.settings', 'r') as file:
    out = json.loads(file.read())

COUNT_GROUPS = 4

# SHEETS DIRS
DIR_MAIN_SHEET = out['DIR_MAIN_SHEET']
DIR_SORT_SHEET = out['DIR_SORT_SHEET']
DIR_PLANS_SHEET = out['DIR_PLANS_SHEET']
SETTINGS_ACCOUNT_PATH = out['SETTINGS_ACCOUNT_PATH']
LOG_PATH = out['LOG_PATH']

SHEET_PLANS_COLUMN = ['A', 'B', 'C', 'D', 'E']
SHEET_SORT_COLUMN = [['A', 'B'], ['C', 'D'], ['E', 'F'], ['G', 'H']]
SORTED_KEYS = [['צוות נוטשים', 'נוטשים'], ['צוות נוטשים', 'WB'], ['צוות WB', 'WB'], ['צוות WB', 'נוטשים']]

TIME_DELAY_PERC = out['TIME_DELAY_PERC']
MAX_TIME_WAIT = out['MAX_TIME_WAIT']
TYPE_SLEEP = out['TYPE_SLEEP'] # last

LOGGING = out['LOGGING']
