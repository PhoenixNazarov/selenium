from tkinter import messagebox

import selenium.common.exceptions as selenium_exceptions
from modules.exception.Exceptions import *
import json


def read_json_error(path):
    def decorator(func):
        def wrapper(*args, **kwarg):
            try:
                return func(*args, **kwarg)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                base = {}
                with open(path, 'w') as file:
                    file.write(json.dumps(base))
            except Exception as e:
                base = []
                with open(path, 'w') as file:
                    file.write(json.dumps(base))

        return wrapper

    return decorator


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


def worker_exceptions(func):
    def wrapper(*args, **kwarg):
        try:
            return func(*args, **kwarg)
        except SmsExceptions as e:
            msg = e.msg
        except selenium_exceptions.SessionNotCreatedException as e:
            msg = 'Возможно старая версия Chrome' + '\n' + e.msg
        except Exception as e:
            msg = "Непредвиденная ошибка" + '\n'
            messagebox.showerror("Ошибка", msg)
            raise e
        messagebox.showerror("Ошибка", msg)

    return wrapper


def mail_exception(func):
    def wrapper(*args, **kwarg):
        password = args[0]
        numb = args[1]
        try:
            return func(*args, **kwarg)
        except Exception as e:
            match e:
                case b'[AUTHENTICATIONFAILED] Invalid credentials (Failure)':
                    raise InvalidMail(password['gmail'], numb)
                case b'[ALERT] Please log in via your web browser: https://support.google.com/mail/accounts/answer/78754 (Failure)':
                    raise NotAllowedMail(password['gmail'], numb)
                case _:
                    raise SmsLoadError(password['gmail'], numb)

    return wrapper


def elements_exception(func):
    def wrapper(*args, **kwarg):
        password = args[0]
        numb = args[1]
        try:
            return func(*args, **kwarg)
        except selenium_exceptions.NoSuchElementException as e:
            msg = "Не удалось найти элемент: " + '\n' + e.msg
            messagebox.showerror("Ошибка", msg)
        except FinderTooTime as e:
            messagebox.showerror("Ошибка", e.msg)
        except Exception as e:
            raise e

    return wrapper
