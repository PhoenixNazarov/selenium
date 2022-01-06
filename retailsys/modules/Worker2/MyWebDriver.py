from config import *
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions as selenium_exceptions
from modules.exception.Exceptions import *

import time


class TimeManagement:
    def __init__(self):
        self.hit = 0
        self.count = 0
        self.max_time = MAX_TIME_WAIT
        self.statistic = {}

    def have_element(self, function):
        try:
            self.hit += 1
            return function()
        except:
            self.hit -= 1
            return False

    def standard_mode(self, function, time_sleep, important):
        for i in range(CAN_MISS_WHEN_SLEEP):
            if important:
                time.sleep(time_sleep * TIME_DELAY_PERC)
            res = self.have_element(function)
            if res:
                return res

    def fast_mode(self, function):
        start_time = time.time()
        while 1:
            if time.time() - start_time > MAX_TIME_WAIT:
                raise FinderTooTime(None, MAX_TIME_WAIT)
            res = self.have_element(function)
            if res:
                return res

            time.sleep(0.01)

    # side = start(True) / end(False)
    # time_sleep = ~0.5
    # important = True/False
    def operation(self, function, side=True, time_sleep=0, important=False):
        if side:
            if important:
                self.standard_mode(function, time_sleep, important)
            elif TYPE_SLEEP == 'fast':
                self.fast_mode(function)
            else:
                self.standard_mode(function, time_sleep, important)

        res = function()

        if not side:
            if important:
                self.standard_mode(function, time_sleep, important)
            elif TYPE_SLEEP == 'fast':
                self.fast_mode(function)
            else:
                self.standard_mode(function, time_sleep, important)

        return res


class WebDriver(webdriver.Chrome):
    def __init__(self):
        options = webdriver.ChromeOptions()
        super().__init__(chrome_options = options, executable_path = PATH_WEBDRIVER)
        self.last_time = time.time()
        self.tm = TimeManagement()

    def nothing(self, **kwargs):
        return self.tm.operation(lambda: None, **kwargs)

    def get(self, url, **kwargs):
        return self.tm.operation(lambda: super().get(url), **kwargs)

    def find_elements(self, by=By.ID, value=None, **kwargs):
        return self.tm.operation(lambda: super().find_elements(by, value), **kwargs)

    def find_element(self, by=By.ID, value=None, command='', **kwargs):
        res = self.find_elements(by = by, value = value, **kwargs)[0]
        if command == 'click':
            res.click()
        return res

    def have_element(self, by=By.ID, value=None):
        try:
            return self.find_element(by = by, value = value)
        except:
            return False
