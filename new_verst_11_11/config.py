from tkinter import *
from selenium import webdriver
from openpyxl import load_workbook
import time
import random
import re
import json
import threading
import traceback
from typing import List


TIME_DELAY_PERC = 5

COUNT_GROUPS = 4

# SHEETS DIRS
DIR_MAIN_SHEET = '123.xlsx'
DIR_SORT_SHEET = 'sort.xlsx'
DIR_PLANS_SHEET = 'plans.xlsx'

SHEET_PLANS_COLUMN = ['A', 'B', 'C', 'D', 'E']
SHEET_SORT_COLUMN = [['A', 'B'], ['C', 'D'], ['E', 'F'], ['G', 'H']]
SORTED_KEYS = [['צוות נוטשים', 'נוטשים'], ['צוות נוטשים', 'WB'], ['צוות WB', 'WB'], ['צוות WB', 'נוטשים']]

SETTINGS_ACCOUNT_PATH = 'settings.txt'
LOG_PATH = r'log.json'


TIME_DELAY = 1
MAX_TIME_WAIT = 10
TYPE_SLEEP = 'fast' # last

LOGGING = True
