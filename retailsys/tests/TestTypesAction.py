from popular_import import *
from modules.data.Log import Log


class Error:
    def __init__(self):
        return

    def wait_change_position(self):
        return

    def change_position(self, _type, position):
        return


class Save:
    def __init__(self):
        return

    def wait_command(self):
        return

    def change_position(self, position, type):
        return


class Status:
    status = {
        'start': 'Открытие Chrome',
        'enter_sms': 'Ожидание смс',
        'polling': 'Ожидание старта линии',

        'open_link': 'Переход на страницу тарифов',
        'choose_plans': 'Выбор тарифа',
        'button_card': 'Кнопка карты',
        'check_on_reg': 'Проверка на регистрацию',
        'marking_options': 'Отмечение параметров',
        'enter_number': 'Ввод номера',
        'mark_last_params': 'Отмечение последних параметров',
        'end_action': 'Выбор: добавить/копировать пакет|ввод перс.данных',
        'enter_email': 'Ввод mail',
        'enter_mailing_data': 'Ввод перс. данных',
        'enter_addr': 'Ввод адреса',
        'enter_more_data': 'Ввод данных, продолжить',
        'enter_more_data2': 'Ввод данных2',
        'enter_card': 'Ввод карты',
        "end": 'Конец',
        'save': 'Сохранение данных',
    }

    def __init__(self):
        self.last_status = ''

    def set_status(self, key):
        if key not in self.status:
            self.last_status = key
        else:
            self.last_status = self.status[key]
        print(self.last_status)

    def get_status(self):
        return self.last_status


class Stack:
    # contains all __lines for Worker
    def __init__(self):
        self.__linesGroup = None

        self.__stack = []
        self.__run_index = -1
        self.__end_indexes = []

    def load_lines(self, group):
        self.__linesGroup = group

    def force_line(self, line_index):
        if line_index in self.__stack:
            self.__stack.pop(self.__stack.index(line_index))
        else:
            self.__stack.append(line_index)

    def wait_line(self):
        wait(lambda: len(self.__stack) == 0)
        line_index = self.__stack.pop(0)
        self.__run_index = line_index
        return self.__linesGroup.get_line_from(line_index)

    def end_line(self, line):
        self.__end_indexes.append(line.index)

    def get_status(self, line_index):
        if line_index == self.__run_index:
            return ['run']
        elif line_index in self.__stack:
            return ['in_stack', str(self.__stack.index(line_index) + 1)]
        else:
            return ['wait']

    def start_next(self):
        for line in self.__linesGroup.get_lines():
            if line.index not in self.__end_indexes:
                return self.force_line(line.index)
