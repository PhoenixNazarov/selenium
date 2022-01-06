import json
from tkinter import messagebox

from modules.exception.Exceptions import *


def test_path():
    exmpl = {
        'PATH_MAIN_SHEET': 'data/123.xlsx',
        'PATH_SORT_SHEET': 'data/sort.xlsx',
        'PATH_PLANS_SHEET': 'data/plans.xlsx',
        'SETTINGS_ACCOUNT_PATH': 'data/settings.txt',
        'PATH_WEBDRIVER': 'webDriver/chromedriver.exe',
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
        'Main Sheet': config.PATH_MAIN_SHEET,
        'Sort Sheet': config.PATH_SORT_SHEET,
        'Plans Sheet': config.PATH_PLANS_SHEET,
        'Web Driver': config.PATH_WEBDRIVER,
        'Settings Account': config.SETTINGS_ACCOUNT_PATH,
        'Log': config.LOG_PATH
    }
    crash_files = ['Main Sheet', 'Sort Sheet', 'Plans Sheet', 'Web Driver']
    check_json = ['Settings Account', 'Log']

    import tkinter as tk

    root = None
    for i in check_path:
        if not os.path.exists(check_path[i]):
            root = tk.Tk()
            if i in crash_files:
                msg = 'Отсутствует файл: ' + i + '\nДобавьте его по пути: ' + check_path[i]
                messagebox.showerror("Ошибка", msg)
            else:
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
