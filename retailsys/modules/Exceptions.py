import json
import tkinter
from tkinter import messagebox
import selenium.common.exceptions as selenium_exceptions

# from modules.Data import Log
from modules.Data import Log


class SmsLoadError(Exception, Log):
    def __init__(self, gmail, numb):
        self.write_log('exceptions', 'SmsLoadError', numb)
        self.gmail = gmail


class DataLoadError(Exception):
    def __init__(self, desr):
        print('this variable is undefined: ' + desr)


def main_exceptions(func):
    def wrapper(*args, **kwarg):
        try:
            return func(*args, **kwarg)
        except FileNotFoundError as e:
            msg = str(e) + '\nПроверьте файл и путь к файлу'
            messagebox.showerror("Ошибка", msg)
        except selenium_exceptions.SessionNotCreatedException as e:
            msg = str(e) + '\nВозможно старая версия Chrome'
            messagebox.showerror("Ошибка", msg)
    return wrapper



def test_path():
    exmpl = {
        'DIR_MAIN_SHEET': 'data/123.xlsx',
        'DIR_SORT_SHEET': 'data/sort.xlsx',
        'DIR_PLANS_SHEET': 'data/plans.xlsx',
        'SETTINGS_ACCOUNT_PATH': 'data/settings.txt',
        'LOG_PATH': 'data/log.json',
        'TIME_DELAY_PERC': 0.5,
        'MAX_TIME_WAIT': 10,
        'TYPE_SLEEP': 'fast',
        'LOGGING': 1
    }
    import os
    if not os.path.exists(r'.settings'):
        with open(r'.settings', 'w') as file:
            file.write(json.dumps(exmpl))
        msg = 'Не удалось найти файл с настройками\n все настройки будут сброшены'
        messagebox.showinfo("Осторожно", msg)
    try:
        import config
    except Exception as e:
        with open(r'.settings', 'w') as file:
            file.write(json.dumps(exmpl))
        msg = 'Не удалось найти файл с настройками\n все настройки будут сброшены'
        messagebox.showinfo("Осторожно", msg)
        import config

    for name, val in config.out.items():
        if val is None or val == '' or val == -1:
            raise DataLoadError(name)

    check_path = {
        'Main Sheet': config.DIR_MAIN_SHEET,
        'Sort Sheet': config.DIR_SORT_SHEET,
        'Plans Sheet': config.DIR_PLANS_SHEET,
        'Settings Account': config.SETTINGS_ACCOUNT_PATH,
        'Log': config.LOG_PATH
    }
    crash_files = ['Main Sheet', 'Sort Sheet', 'Plans Sheet']
    check_json = ['Settings Account', 'Log']

    import tkinter as tk

    root = None
    for i in check_path:
        if not os.path.exists(check_path[i]):
            root = tk.Tk()
            if i in crash_files:
                msg = 'Отсутствует файл: ' + i + '\nДобавьте его'
                messagebox.showerror("Ошибка", msg)
                raise DataLoadError(i)

            msg = 'Отсутствует файл: ' + i + '\nПопробуем создать его'
            messagebox.showerror("Осторожно", msg)

        if i in check_json:
            try:
                with open(check_path[i], 'r') as file:
                    json.loads(file.read())
            except:
                with open(check_path[i], 'w') as file:
                    file.write(json.dumps([]))
    if root:
        root.destroy()


