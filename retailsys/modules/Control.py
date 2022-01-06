from modules.exception.Handlers import main_exceptions
from config import *
from modules.data.Sheets import MainSheet, FilterSheet, PlansSheet
from modules.UI.Window import UI
from modules.LinesGroup import LinesGroup
from modules.Worker import Worker


@main_exceptions
class Control:
    def __init__(self):
        self.Sheets = {
            'Main': MainSheet(),
            'Filter': FilterSheet(),
            'Plans': PlansSheet()
        }
        self.UI = UI()

    def pre_start(self):
        lines = self.Sheets['Main'].get_lines()
        for i in range(len(lines)):
            lines[i].load_plans(self.Sheets['Plans'].get_plans())

        line_groups = []
        for _filter in self.Sheets['Filter'].get_sort_keys():
            line_groups.append(LinesGroup(lines, _filter))

        # place on UI
        canvas = self.UI.make_root()
        for numb in range(COUNT_GROUPS):
            canvas[numb].Stack.load_lines(line_groups[numb])
            worker = Worker(canvas[numb].create_worker_config(), self.Sheets['Main'])
            if len(line_groups[numb].get_lines()) > 0:
                worker.polling()

        self.UI.show_UI()

