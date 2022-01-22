from modules.exception.Handlers import main_exceptions
from config import *
from modules.UI import UI
from modules.Lines import load_lines_group
from modules.Worker import Operator
from modules.functions import start_thread


@main_exceptions
class Control:
    def pre_start(self):
        line_groups = load_lines_group()
        canvas = UI.make_root()
        for numb in range(COUNT_GROUPS):
            canvas[numb].Stack.load_lines(line_groups[numb])
            worker = Operator(*canvas[numb].create_worker_config())
            if len(line_groups[numb].get_lines()) > 0:
                start_thread(worker.polling)
        UI.show_UI()
