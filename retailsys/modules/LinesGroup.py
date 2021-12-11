from typing import List

from config import *
from modules.Line import Line
from modules.UI import CanvasUI


class LinesGroup:
    def __init__(self, lines: List[Line], _filter):
        self.lines = []
        for line in lines:
            for sort_key in _filter:
                if line.first_sort_key == sort_key[0] and line.second_sort_key == sort_key[1]:
                    self.lines.append(line)

