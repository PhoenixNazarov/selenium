from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium
import threading

from config import *
from modules.exception.Handlers import *
from modules.Line import Line
from modules.Data import SettingsJson, Log, ErrorsSheetBase, ErrorsSheetCollect

from modules.Worker.MyWebDriver import WebDriver
from modules.Objects import WebDriverLogics
from modules.Worker.Handler import *
from modules.Worker.Scenario import *


class Worker:
    def __init__(self, Bunch, MainSheet):
        self.web_driver = WebDriver()
        self.Bunch = Bunch
        self.WebDriverLogics = WebDriverLogics(
            UI_control = UI_control(Bunch)
        )

        self.Settings = SettingsJson(numb)
        self.MainSheet = MainSheet
        self.ErrorSheet = ErrorsSheetBase()
        self.ErrorSheetCollect = ErrorsSheetCollect()

        self.type_sleep = TYPE_SLEEP
        self.current_line = None

        Status.set_status('start')

    def polling(self):
        while 1:
            Scenario(self.WebDriverLogics).play()