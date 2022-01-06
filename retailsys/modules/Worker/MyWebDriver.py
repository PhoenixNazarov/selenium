from config import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from modules.Worker.Login import *


class WebDriver(webdriver.Chrome):
    def __init__(self):
        options = webdriver.ChromeOptions()
        super().__init__(chrome_options = options, executable_path = PATH_WEBDRIVER)
        authorization(self)

    def get(self, url):
        super().get(url)

    def find_elements(self, by=By.ID, value=None):
        elements = super().find_elements(by, value)
        return elements

    def find_element(self, by=By.ID, value=None):
        return self.find_elements(by=by, value=value)[0]



