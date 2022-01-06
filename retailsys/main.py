import traceback

if __name__ == '__main__':
    # try:
    from modules.exception.HardCheck import test_path

    test_path()

    from modules.Control import Control

    Control().pre_start()
# except Exception as e:
#     print('Ошибка:\n', traceback.format_exc())
#     input()
