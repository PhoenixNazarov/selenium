import traceback

from modules.Control import Control

if __name__ == '__main__':
    try:
        Control().pre_start()
    except Exception as e:
        print('Ошибка2:\n', traceback.format_exc())
        input()