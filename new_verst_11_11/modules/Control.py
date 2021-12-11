from config import *
from modules.Data import MainSheet, FilterSheet, PlansSheet
from modules.UI import UI
from modules.LinesGroup import LinesGroup
from modules.Worker import Worker


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
            line_groups[numb].place_on_UI(canvas[numb])
            worker = Worker(*canvas[numb].get_worker_config(), self.Sheets['Main'])

        self.UI.show_UI()
