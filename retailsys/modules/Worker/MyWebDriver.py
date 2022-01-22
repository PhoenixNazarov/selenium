from config import *
from modules.exception.Exceptions import FinderTooTime
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions as selenium_exceptions
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
        except selenium_exceptions.NoSuchElementException:
            self.hit -= 1
            return False

    def __standard_mode(self, function, time_sleep, important):
        for i in range(CAN_MISS_WHEN_SLEEP):
            if important:
                time.sleep(time_sleep * TIME_DELAY_PERC)
            res = self.have_element(function)
            if res:
                return res

    def __fast_mode(self, function):
        start_time = time.time()
        while 1:
            if time.time() - start_time > MAX_TIME_WAIT:
                raise FinderTooTime(None, MAX_TIME_WAIT)
            res = self.have_element(function)
            if res:
                return res

            time.sleep(0.01)

    # def wait_mode(self, function):
    #

    # side = start(True) / end(False)
    # time_sleep = ~0.5
    # important = True/False
    def operation(self, function, time_sleep=0, important=False):

        if important:
            return self.__standard_mode(function, time_sleep, important)
        elif TYPE_SLEEP == 'fast':
            return self.__fast_mode(function)
        else:
            return self.__standard_mode(function, time_sleep, important)


class WebDriver(webdriver.Chrome):
    def __init__(self):
        options = webdriver.ChromeOptions()
        super().__init__(chrome_options = options, executable_path = PATH_WEBDRIVER)
        self.last_time = time.time()
        self.tm = TimeManagement()
        self.superclass = super()

    def nothing(self, **kwargs):
        return self.tm.operation(lambda: None, **kwargs)

    def get(self, url, **kwargs):
        self.superclass.get(url)

    def find_elements(self, by=By.ID, value=None, **kwargs):
        return self.tm.operation(lambda: self.superclass.find_elements(by, value), **kwargs)

    def find_element(self, by=By.ID, value=None, **kwargs):
        return self.find_elements(by = by, value = value, **kwargs)[0]

    def have_element(self, by=By.ID, value=None):
        try:
            return self.superclass.find_elements(by, value)
        except:
            return False

