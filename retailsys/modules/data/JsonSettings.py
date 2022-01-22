from config import *
from modules.exception.Handlers import read_json_error


class SettingsJson:
    def __init__(self, numb):
        self.numb = numb

    @read_json_error(SETTINGS_ACCOUNT_PATH)
    def get_data(self):
        with open(SETTINGS_ACCOUNT_PATH, 'r') as file:
            return json.loads(file.read())[self.numb]

    def save(self, data):
        with open(SETTINGS_ACCOUNT_PATH, 'r') as file:
            settings = json.loads(file.read())
        settings[self.numb] = data
        with open(SETTINGS_ACCOUNT_PATH, 'w') as file:
            file.write(json.dumps(settings))


class SettingsMain:
    __path = r'.settings'
    exmpl = {
        'PATH_MAIN_SHEET': 'data/123.xlsx',
        'PATH_SORT_SHEET': 'data/sort.xlsx',
        'PATH_PLANS_SHEET': 'data/plans.xlsx',
        'PATH_WEBDRIVER': 'webDriver/chromedriver.exe',
        'SETTINGS_ACCOUNT_PATH': 'data/settings.txt',
        'LOG_PATH': 'data/log.json',
        'TIME_DELAY_PERC': 0.5,
        'MAX_TIME_WAIT': 10,
        'TYPE_SLEEP': 'fast',
        'LOGGING': 1
    }

    @read_json_error(__path)
    def get_keys(self):
        return self.exmpl.keys()

    def get_data(self):
        with open(self.__path, 'r') as file:
            out = json.loads(file.read())
        return out

    def save(self, data):
        with open(self.__path, 'w') as file:
            file.write(json.dumps(data))
