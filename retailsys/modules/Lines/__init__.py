from modules.data import MainSheet, FilterSheet, PlansSheet
from modules.Lines.LinesGroup import LinesGroup
from modules.Lines.Line import Line


def load_lines_group():
    lines = []
    line_index = 2
    while MainSheet.get_value("S", line_index):
        line = Line(line_index)
        lines.append(line)
        line_index += line.COUNT_LINES

    for i in range(len(lines)):
        lines[i].load_plans(PlansSheet.get_plans())
    line_groups = []
    for _filter in FilterSheet.get_sort_keys():
        line_groups.append(LinesGroup(lines, _filter))
    return line_groups
