import time
import threading


def closure(command, *args, **kwargs):
    def closure_command():
        command(*args, **kwargs)

    return closure_command


def start_thread(function):
    threading.Thread(target=function).start()


def wait(func):
    while func():
        time.sleep(0.1)
