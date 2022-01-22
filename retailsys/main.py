import traceback


if __name__ == '__main__':
    try:
        from modules.exception.HardCheck import test_path
        from modules.exception.Handlers import main_exceptions
        from modules.UI import UI
        from modules.Lines import load_lines_group
        from modules.Worker import Operator
        from modules.functions import start_thread
        from config import *


        @main_exceptions
        def pre_start():
            line_groups = load_lines_group()
            canvas = UI.make_root()
            for numb in range(COUNT_GROUPS):
                canvas[numb].Stack.load_lines(line_groups[numb])
                worker = Operator(*canvas[numb].create_worker_config())
                if len(line_groups[numb].get_lines()) > 0:
                    start_thread(worker.polling)
            UI.show_UI()
        pre_start()
    except Exception as e:
        print('Ошибка:\n', traceback.format_exc())
        input()
