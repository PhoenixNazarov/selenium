from config import *
from modules.Line import Line
from modules.UI import CanvasUI


class LinesGroup:
    def __init__(self, lines: List[Line], filter):
        self.lines = []
        for line in lines:
            if line.first_sort_key == filter[0] and line.first_sort_key == filter[1]:
                self.lines.append(line)
        print(len(self.lines))

    def place_on_UI(self, canvas: CanvasUI):
        for line in self.lines:
            canvas.place_line(line)
