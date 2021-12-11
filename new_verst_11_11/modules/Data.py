from config import *
from modules.Line import Line


class Sheet:
    def __init__(self, path):
        self.path = path
        self._wb = load_workbook(path)
        for g in self._wb:
            self.sheet = self._wb[str(g)[12:-2]]

    def get_columns(self, columns, offset=0):
        data = []
        for i in columns:
            data.append(self.get_column(i, offset))
        return [[data[j][i] for j in range(len(data))] for i in range(len(data[0]))]

    def get_column(self, column, offset=0):
        data = []
        ind = 1 + offset
        while self.get_value(column, ind):
            data.append(self.get_value(column, ind))
            ind += 1
        return data

    def get_value(self, column, line):
        val = self.sheet[f'{column}{line}'].value
        if val:
            return str(val)
        return self.sheet[f'{column}{line}'].value

    def set_value(self, column, line, val):
        self.sheet[f'{column}{line}'].value = val


class MainSheet(Sheet):
    def __init__(self):
        super().__init__(DIR_MAIN_SHEET)

    def get_special_data(self, name, line_index):
        if name == "count_line":
            return self.get_value("S", line_index)
        if name == "first_sort_key":
            return self.get_value("P", line_index)
        if name == "second_sort_key":
            return self.get_value("M", line_index)

    def get_lines(self):
        lines = []
        line_index = 2
        while self.get_value("S", line_index):
            line = Line(self, line_index)
            lines.append(line)
            line_index += line.COUNT_LINES
        return lines

    def get_sorted_lines(self, sort_keys):
        sorted_lines = []
        config_lines = self.load_config_lines()

        for line in config_lines:
            for number in range(COUNT_GROUPS):
                if line[0] in sort_keys[number]:
                    sorted_lines[number].append(line[1])

        return sorted_lines

    def load_config_lines(self):
        line_index = 2
        config_lines = []
        while self.get_special_data("count_line", line_index):
            count_lines = int(self.get_special_data("count_line", line_index))
            config_lines.append([
                [self.get_special_data("first_sort_key", line_index),
                 self.get_special_data("second_sort_key", line_index)],
                count_lines]
            )
            line_index += count_lines
        return config_lines


class FilterSheet(Sheet):
    def __init__(self):
        super().__init__(DIR_SORT_SHEET)

    def get_sort_keys(self):
        return [self.get_columns(columns) for columns in SHEET_SORT_COLUMN]


class PlansSheet(Sheet):
    def __init__(self):
        super().__init__(DIR_PLANS_SHEET)
        self.self_plans_set = self.load()

    def get_plans(self):
        return self.self_plans_set

    def load(self):
        out = []
        counter = 1
        while self.get_value(SHEET_PLANS_COLUMN[0], counter):
            line = []
            for column in SHEET_PLANS_COLUMN:
                line.append(self.get_value(column, counter))
            out.append(line)
            counter += 1
        return out


class SettingsJson:
    def __init__(self, numb):
        self.numb = numb

    def get_data(self):
        with open(SETTINGS_ACCOUNT_PATH, 'r') as file:
            return json.loads(file.read())[self.numb]

    def save(self, data):
        with open(SETTINGS_ACCOUNT_PATH, 'r') as file:
            settings = json.loads(file.read())
        settings[self.numb] = data
        with open(SETTINGS_ACCOUNT_PATH, 'w') as file:
            file.write(json.dumps(settings))


class SettingsJson:
    def __init__(self, numb):
        self.numb = numb

    def get_data(self):
        with open(SETTINGS_ACCOUNT_PATH, 'r') as file:
            return json.loads(file.read())[self.numb]

    def save(self, data):
        with open(SETTINGS_ACCOUNT_PATH, 'r') as file:
            settings = json.loads(file.read())
        settings[self.numb] = data
        with open(SETTINGS_ACCOUNT_PATH, 'w') as file:
            file.write(json.dumps(settings))



class Log:
    __path = LOG_PATH
    __base = {}
    __check = 0
    __numb = -1

    def __init__(self, numb):
        self.__numb = numb

    def write_log(self, _type, description, numb=-1):
        if self.__numb != -1:
            numb = self.__numb
        if not LOGGING: return
        self.__read()
        self.__base.append({
            'type': _type,
            'description': description,
            'numb': numb,
            'time': round(time.time())
        })
        self.__save()

    def __read(self):
        try:
            with open(self.__path, 'r') as file:
                self.__base = json.loads(file.read())
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.base = {}
            self.__save()
        except Exception as e:
            self.base = {}
            self.__save()

    def __save(self):
        with open(self.__path, 'w') as file:
            file.write(json.dumps(self.base))