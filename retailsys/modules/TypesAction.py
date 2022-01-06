from functools import partial
from tkinter import *

from config import *
from modules.LinesGroup import LinesGroup
from modules.Data import Log


class Error(Log):
    def __init__(self, buttons, numb):
        super().__init__(numb)
        self.label_status_error, self.btn_error_next, self.btn_error_repeat, self.btn_error_cancel = buttons
        self.btn_error_next['command'] = lambda: self.change_position('next', 0)
        self.btn_error_repeat['command'] = lambda: self.change_position('repeat', 0)
        self.btn_error_cancel['command'] = lambda: self.change_position('cancel', 0)

        self.type = ''
        self.position = 1

    def wait_change_position(self):
        start_position = self.position
        while self.position == start_position:
            time.sleep(0.1)
        return self.type

    def change_position(self, _type, position):
        self.write_log('error', position)
        self.type = _type
        self.position = position

        if position == 1:
            self.label_status_error.configure(fg = 'red')
            self.btn_error_next.configure(state = NORMAL)
            self.btn_error_repeat.configure(state = NORMAL)
            self.btn_error_cancel.configure(state = NORMAL)
        else:
            self.label_status_error.configure(fg = 'white')
            self.btn_error_next.configure(state = DISABLED)
            self.btn_error_repeat.configure(state = DISABLED)
            self.btn_error_cancel.configure(state = DISABLED)


class Save:
    def __init__(self, buttons):
        self.label_status_end, self.btn_end_save, self.btn_end_next = buttons
        self.btn_end_save['command'] = lambda: self.change_position(-1, 'save')
        self.btn_end_next['command'] = lambda: self.change_position(-1, 'next')

        self.type = ''
        self.position = 1

    def wait_command(self):
        prev = self.type
        while self.type == prev:
            pass
        if self.type == 'save':
            return 1
        return 0

    def change_position(self, position, type):
        self.type = type
        self.position = position

        if position == 1:
            self.label_status_end.configure(fg = 'green')
            self.btn_end_save.configure(state = NORMAL)
            self.btn_end_next.configure(state = NORMAL)
        else:
            self.label_status_end.configure(fg = 'white')
            self.btn_end_save.configure(state = DISABLED)
            self.btn_end_next.configure(state = DISABLED)


class Status(Log):
    status = {
        'start': 'открытие Chrome',
        'enter_sms': 'Ввод смс',
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

    def __init__(self, status_label, numb):
        super().__init__(numb)
        self.status_label = status_label
        self.last_status = ''

    def set_status(self, key):
        if key not in self.status:
            print('key not in self status')
            self.status_label.config(text = key)
            self.last_status = key
        else:
            self.status_label.config(text = self.status[key])
            self.last_status = self.status[key]
        self.write_log('set_status', self.last_status)

    def get_status(self):
        return self.last_status


class Stack:
    # contains all __lines for Worker
    def __init__(self, place_line):
        self.__place_line = place_line
        self.__linesGroup: LinesGroup = None
        self.__linesUI = {}

        self.__stack = []
        self.__run_index = -1
        self.__end_indexes = []

    def load_lines(self, group: LinesGroup):
        self.__linesGroup = group
        self.__reload_lines_ui()

    def force_line(self, line_index):
        if line_index in self.__stack:
            self.__stack.pop(self.__stack.index(line_index))
        else:
            self.__stack.append(line_index)
        self.__reload_lines_ui()

    def wait_line(self):
        while len(self.__stack) == 0:
            pass
        line = self.__stack.pop(0)
        self.__run_index = line.index
        self.__reload_lines_ui()
        return line

    def end_line(self, line):
        self.__end_indexes.append(line.index)
        self.__reload_lines_ui()

    def get_status(self, line_index):
        if line_index == self.__run_index:
            return 'run'
        elif line_index in self.__stack:
            return 'in_stack', str(self.__stack.index(line_index) + 1)
        else:
            return 'wait'

    def __add_line_in_ui(self, line=None, line_index=None):
        if line_index is not None:
            line = self.__linesGroup.get_line_from(line_index)
        status = self.get_status(line.index)
        self.__linesUI.update({line.index: self.__place_line(line, closure(self.force_line, line.index), status)})

    def __reload_lines_ui(self):
        for i in self.__linesUI.values():
            i.destroy()

        self.__linesUI = {}
        # active
        if self.__run_index != -1:
            self.__place_line(None, "run")
            self.__add_line_in_ui(line_index = self.__run_index)
            self.__place_line(None, '')

        # in_stack
        self.__place_line(None, "stack")
        [self.__add_line_in_ui(line_index = index) for index in self.__stack]
        self.__place_line(None, '')

        # wait
        self.__place_line(None, "wait")
        for line in self.__linesGroup.get_lines():
            if line.index != self.__run_index and \
                    line.index not in self.__stack and \
                    line.index not in self.__end_indexes:
                self.__add_line_in_ui(line = line)
        self.__place_line(None, "")

        # end
        self.__place_line(None, "end")
        [self.__add_line_in_ui(line_index = index) for index in self.__end_indexes]
