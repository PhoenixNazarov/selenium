class LinesGroup:
    def __init__(self, lines, _filter):
        self.__lines = []
        for line in lines:
            for sort_key in _filter:
                if line.first_sort_key == sort_key[0] and line.second_sort_key == sort_key[1]:
                    self.__lines.append(line)

    def get_line_from(self, index=False):
        if index:
            for line in self.__lines:
                if line.index == index:
                    return line

    def get_lines(self):
        return self.__lines
